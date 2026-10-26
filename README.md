# Measuring Logical Reasoning in Turkish Offline Language Models via Fallacy Detection

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://img.shields.io/badge/DOI-10.13140%2FRG.2.2.35904.60162-blue.svg)](https://doi.org/10.13140/RG.2.2.35904.60162)

This repository contains the dataset, scripts, and results for evaluating the logical reasoning capabilities of offline Turkish Language Models by detecting fallacies.


## Folder Structure

The repository is organized as follows to streamline reproducible research:

- **`data/`**: Contains the raw and processed datasets.
  - `ai-safsata.xlsx`: The input dataset containing statements tailored for AI evaluation.
  - `human-safsata.xlsx`: The input dataset containing statements tailored for Human evaluation.
  - **`results/`**: Subfolders containing model outputs and derived evaluation datasets for each distinct experiment setup.
    - `ai_blind/`: Results for the scenario where models analyze statements without fallacy definitions.
    - `ai_informed/`: Results for the scenario where models are provided with definitions of fallacies in the prompt.
    - `human_blind/`: Corresponding human-evaluated results without provided definitions.
    - `human_informed/`: Corresponding human-evaluated results with provided definitions.
- **`docs/`**: Documentation and research reports.
  - `Article_Measuring_Logical_Reasoning.pdf`: The full PDF of the research article detailing methodologies and findings.
  - **`reports/`**: PDF classification reports generated from the Jupyter notebook detailing evaluation metrics across various experiment sets (e.g., `ai_blind`, `ai_informed`, `human_blind`...).
- **`src/`**: The core source code for conducting the evaluations.
  - `safsata_analiz_blind.py`: Script to call the language models *without* providing fallacy definitions in the prompt.
  - `safsata_analiz_informed.py`: Script to call the language models *with* provided fallacy definitions in the prompt.
  - `evaluation.ipynb`: Jupyter Notebook for converting raw results into comprehensive classification metrics (Accuracy, F1, ROC-AUC) and generating PDF reports.
  - `llms.txt`: A simple text file that sets the model name used by the scripts.

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kahramankostas/TRfallacy.git
   cd TRfallacy
   ```

2. **Run an OpenAI-compatible Local LLM Server:**
   The scripts are configured to communicate with a local LLM API (e.g., using LM Studio). Ensure your local server is running and accessible at:
   `http://127.0.0.1:1234/v1/chat/completions`

3. **Install Dependencies:**
   Install required Python packages (Pandas, Requests, Tqdm, Scikit-learn, etc.).
   ```bash
   pip install pandas requests tqdm matplotlib seaborn scikit-learn
   ```

4. **Select a language model:**
   Edit the `src/llms.txt` file and enter the identifier for the specific local language model you are evaluating.
   For example: `zai-org/glm-4.7-flash`

## Usage Instructions

To run the fallacy analysis, you should navigate to the root directory of the project and run the analyzer scripts pointing to the `src` folder. The Python scripts now accept `--input` and `--output` arguments so you can explicitly pass the different data files (`ai-safsata.xlsx` vs `human-safsata.xlsx`).

**Evaluating AI Models - Blind Analysis (No definitions provided):**
```bash
python src/safsata_analiz_blind.py --input data/ai-safsata.xlsx --output data/results/ai_blind/safsata_sonuclar.xlsx
```

**Evaluating AI Models - Informed Analysis (Definitions provided):**
```bash
python src/safsata_analiz_informed.py --input data/ai-safsata.xlsx --output data/results/ai_informed/safsata_sonuclar.xlsx
```

*(You can replace the `--input` with `data/human-safsata.xlsx` and target the `results/human_...` output directories if you plan to use an LLM to evaluate the Human dataset as a comparative baseline)*

**Evaluating Metrics:**
To generate the metrics and graphs, use the `src/evaluation.ipynb` notebook. Make sure to specify the correct input `.csv` and output `.pdf` paths according to whether you are analyzing the "blind" or "informed" results.

## Citation

If you use this dataset, codebase, or findings in your research, please cite our paper:

**Text Citation:**
> Çancı, İ. F., Shahbazov, G., Yılmaz, E., & Kostas, K. (2026). Measuring Logical Reasoning in Turkish Offline Language Models via Fallacy Detection. In A. Alaybeyoğlu, E. Kaya, & Ü. Sarp (Eds.), *6th International Artificial Intelligence and Data Science Congress (ICADA 2026): Proceedings Book, Full Papers*. Duvar Yayınları. https://doi.org/10.13140/RG.2.2.35904.60162

**BibTeX:**
```bibtex
@inproceedings{canci2026measuring,
  author    = {Çancı, Inanç Feridun and Shahbazov, Gizem and Yılmaz, Edibe and Kostas, Kahraman},
  title     = {Measuring Logical Reasoning in Turkish Offline Language Models via Fallacy Detection},
  booktitle = {6th International Artificial Intelligence and Data Science Congress (ICADA 2026): Proceedings Book, Full Papers},
  editor    = {Alaybeyoğlu, Ayşegül and Kaya, Ebubekir and Sarp, Ümit},
  year      = {2026},
  month     = apr,
  address   = {Nevşehir, Türkiye},
  publisher = {Duvar Yayınları},
  isbn      = {978-625-8756-91-3},
  doi       = {10.13140/RG.2.2.35904.60162},
  url       = {https://doi.org/10.13140/RG.2.2.35904.60162},
  note      = {Licensed under CC BY 4.0}
}
```

## License

- **Source Code:** Distributed under the [MIT License](LICENSE).
- **Data & Research Paper:** Licensed under Creative Commons Attribution 4.0 International ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)).


