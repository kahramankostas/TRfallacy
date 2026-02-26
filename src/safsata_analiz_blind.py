import pandas as pd
import requests
import json
import time
from tqdm import tqdm
import os

# Configuration
API_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_NAME = "zai-org/glm-4.7-flash"
import argparse

VALID_DURUM = ["Safsata", "Geçerli"]
FALLACY_TYPES = [
    'Appeal to Authority',
    'False Cause',
    'False Dilemma',
    'Hasty Generalization',
    'Slippery Slope'
]

def load_first_model_name():
    try:
        with open("llms.txt", "r") as f:
            line = f.readline().strip()
            if line:
                return line
    except:
        pass
    return MODEL_NAME

def build_prompt(text, row_id):
    return f"""Aşağıdaki metni analiz et ve SADECE aşağıdaki JSON formatında yanıt ver.

Metin: "{text}"

KURALLAR (İSTİSNASIZ UYULMASI ZORUNLU):
1. "durum" alanı YALNIZCA şu iki değerden biri olabilir: "Safsata" veya "Geçerli"
2. "tur" alanı YALNIZCA şu beş değerden biri olabilir:
   - "Appeal to Authority"
   - "False Cause"
   - "False Dilemma"
   - "Hasty Generalization"
   - "Slippery Slope"
3. Bu listelerin DIŞINDA HİÇBİR değer kabul edilmez. Türkçe yazma, açıklama ekleme, başka kategori uydurma.
4. Yanıtın tamamı yalnızca şu JSON olsun, başında/sonunda hiçbir şey olmasın:

{{
  "id": {row_id},
  "durum": "Safsata veya Geçerli",
  "tur": "Beş seçenekten biri"
}}"""

def validate_result(result):
    """Dönen sonucun izin verilen değerlere sahip olup olmadığını kontrol eder."""
    if not isinstance(result, dict):
        return False
    if result.get("durum") not in VALID_DURUM:
        return False
    if result.get("tur") not in FALLACY_TYPES:
        return False
    return True

def parse_response(content, row_id):
    """Model çıktısını temizleyip JSON olarak parse eder."""
    content = content.strip()

    # Markdown code block temizliği
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    # Sadece JSON kısmını al (başında/sonunda fazladan metin varsa)
    start = content.find("{")
    end = content.rfind("}") + 1
    if start != -1 and end > start:
        content = content[start:end]

    return json.loads(content)

def analyze_text(text, model_name, row_id, max_retries=3):
    for attempt in range(max_retries):
        payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Sen yalnızca geçerli JSON döndüren bir analiz asistanısın. "
                        "Yanıtında JSON dışında HİÇBİR metin bulunmamalıdır. "
                        "Verilen seçeneklerin dışına ASLA çıkmazsın."
                    )
                },
                {"role": "user", "content": build_prompt(text, row_id)}
            ],
            "temperature": 0.0,  # Deterministik çıktı için 0
            "stream": False
        }

        try:
            response = requests.post(
                API_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=300
            )

            if response.status_code != 200:
                print(f"  [Deneme {attempt+1}] API Hatası (ID: {row_id}): HTTP {response.status_code}")
                continue

            content = response.json()['choices'][0]['message']['content']

            try:
                result = parse_response(content, row_id)
            except json.JSONDecodeError:
                print(f"  [Deneme {attempt+1}] JSON Parse Hatası (ID: {row_id}): {content[:100]}")
                continue

            if validate_result(result):
                return result
            else:
                print(
                    f"  [Deneme {attempt+1}] Geçersiz değer (ID: {row_id}): "
                    f"durum='{result.get('durum')}', tur='{result.get('tur')}'"
                )
                # Bir sonraki denemede modele hatayı da bildir
                continue

        except Exception as e:
            print(f"  [Deneme {attempt+1}] İstek Hatası (ID: {row_id}): {e}")

    # Tüm denemeler başarısız
    print(f"  UYARI: ID {row_id} için {max_retries} deneme sonunda geçerli sonuç alınamadı.")
    return {"id": row_id, "durum": "Hata", "tur": "Hata"}

def main():
    parser = argparse.ArgumentParser(description="Safsata Analysis CLI")
    parser.add_argument("--input", required=True, help="Path to input Excel file.")
    parser.add_argument("--output", required=True, help="Path to output Excel file.")
    args = parser.parse_args()

    print(f"Excel dosyası okunuyor: {args.input}...")
    try:
        df = pd.read_excel(args.input)
    except Exception as e:
        print(f"Dosya okuma hatası: {e}")
        return

    if 'Metin' not in df.columns:
        print("HATA: Excel dosyasında 'Metin' sütunu bulunamadı.")
        return

    model_name = load_first_model_name()
    print(f"Kullanılan Model: {model_name}")
    print(f"Toplam {len(df)} satır işlenecek.")

    results = []

    for index, row in tqdm(df.iterrows(), total=len(df)):
        text = row['Metin']
        row_id = row.get('ID', index)

        result = analyze_text(text, model_name, row_id)

        results.append({
            "Index": index,
            "Model_Durum": result.get("durum"),
            "Model_Tur": result.get("tur")
        })

    results_df = pd.DataFrame(results)
    results_df.set_index("Index", inplace=True)
    final_df = df.join(results_df)

    print("Sonuçlar kaydediliyor...")
    final_df.to_excel(args.output, index=False)
    print(f"İşlem tamamlandı! Dosya: {args.output}")

if __name__ == "__main__":
    main()