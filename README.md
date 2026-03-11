## Project Overview

This repository contains the `Spam_Research.ipynb` notebook for spam detection experiments on Enron and 2021 spam email data. It includes a classical Naive Bayes baseline, logistic regression baseline, and transformer-based models (via Hugging Face `transformers`) for concept-drift analysis.

The notebook is **designed to be run on a GPU-enabled environment** due to the size of the datasets and the cost of fine‑tuning transformer models.

## Recommended Environment

- **Primary environment**: Google Colab
  - Runtime type: **GPU** (e.g., T4 or better)
  - Colab already provides most system dependencies (Python, Jupyter, CUDA drivers).
- **Alternative**: Local machine with
  - Python 3.9+  
  - CUDA‑enabled GPU and compatible PyTorch install  
  - Jupyter (Notebook or Lab) if not using Colab

## Installation

### Option 1: Google Colab (recommended)

1. **Upload or connect the project**
   - Sync this project folder to Google Drive, or open the notebook directly from GitHub in Colab.
2. **Set runtime to GPU**
   - In Colab: `Runtime → Change runtime type → Hardware accelerator → GPU`.
3. **Install Python dependencies inside Colab**
   - The notebook already contains `!pip install` cells for key libraries.  
   - To mirror the full environment, you can also run:
     ```python
     !pip install -r requirements.txt
     ```
4. **Mount Google Drive (in Colab)**
   - The first cell mounts Drive and changes into the project directory; run it as‑is or adapt the path to your Drive layout.

### Option 2: Local GPU environment

1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Ensure you have a **GPU-enabled PyTorch** build matching your CUDA version (see the official PyTorch install instructions).
4. Launch Jupyter and open `Spam_Research.ipynb`:
   ```bash
   jupyter notebook
   ```

## Hugging Face / OPENAI Token & Colab Secrets

The transformer models in this notebook rely on Hugging Face Hub. To avoid hard‑coding credentials, the notebook is intended to **use the Google Colab secrets manager** for the user’s Hugging Face token.

Additionally, to operate any OpenAi API a secret key with funding is required.
### Storing the token in Colab

1. In Colab, open the **secrets/extension UI** (e.g., via the left sidebar or the “Variables & secrets” panel).
2. Create a new secret for your Hugging Face and OpenAI token (for example, named `HF_TOKEN` | `OPANAI_API_KEY`).
3. Save the token; Colab will store it securely and make it available to the notebook at runtime.

### Using the token in the notebook

- In the relevant cell(s), the notebook should **read the token from Colab’s secrets manager or environment** (rather than embedding it in the code) and use it to authenticate with Hugging Face when loading models or datasets from the Hub.
- If you change the secret name (e.g., something other than `HF_TOKEN`), update the corresponding code in the notebook that retrieves the token so they match.

## Zipped files
Due to the size of the model weights and dataset, the following files were compressed before being pushed to GitHub. Before running the notebook, please unzip them and place the extracted folders in the same directory level as the current zip file:

spam_data_2021.zip → spam_data_2021/
bert_spam_model.zip → bert_spam_model/

## How to Run the Notebook End‑to‑End

1. Ensure you are in a **GPU runtime** (Colab or local).
2. Install dependencies (`!pip install -r requirements.txt` in Colab, or `pip install -r requirements.txt` locally).
3. Configure your **Hugging Face token** via Colab secrets (or environment variables, if running locally).
4. Run the cells from top to bottom:
   - Data loading and preprocessing (Enron dataset).
   - Naive Bayes baseline training and evaluation.
   - 2021 spam archive extraction and parsing.
   - Transformer tokenizer/model loading, tokenization, training, and evaluation.

For approximate runtimes of the major sections (on a typical Colab GPU), see `EXPECTED_RUNTIME.md`.

> **Note:** For **runtime efficiency**, you can skip certain steps in the notebook. For example:
> - If your goal is to quickly test the model or downstream tasks, **you can load the provided pretrained model checkpoint and skip the full training loop**.
> - The "Bruce Guenter Spam Archive" dataset extraction (unzipping and parsing `.7z` files) can often be skipped—simply **load the already prepared CSV version** (`bruce_spam.csv`) if it's present in your project directory or Google Drive, rather than re-processing the raw archive.
> 
> Adjust your workflow accordingly to save time, especially when re-running or experimenting!