# RAG Desk

RAG Desk helps you find answers in your documents. Upload a PDF or text file, ask a question, and check the passages it finds. Each passage keeps its file name and page number.

With a language model connected, the app can use those passages to write an answer. You can also search the documents without a model.

## Run the app

Use Python 3.12. On Windows, run `CAI_DAT.bat`, then open `CHAY_DEMO.bat`.

From a terminal:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The app includes a short sample handbook. Turn it off when you want to search only your own files. PDF files need readable text; scanned pages need to be converted first.

## Add answers from a model

Install [Ollama](https://ollama.com/download) and run `ollama pull llama3.2:3b`. Copy `.env.example` to `.env`, restart the app, and select **Hỏi đáp bằng LLM**.

The settings can also point to another service that supports JSON schema responses. Its API address should end in `/v1`; use `LLM_PROVIDER=compatible` and keep the API key in `.env`.

## How the search works

The app splits a document into short passages and looks for the closest matches to your question. The default search uses TF-IDF, a lightweight way to compare text without downloading a model.

A second search option uses Sentence Transformers to compare meaning. Install `requirements-semantic.txt` before selecting it; the first run downloads the model. This optional path has not yet been checked in the supplied run.

On ten sample questions, the default search put the correct source file first every time. The set is small. This result measures the search step, not the accuracy of answers written by a model.

Sources help you review an answer, but a model can still misunderstand them. When the documents do not contain enough information, it is asked to say so.

## Check the project

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python evaluate.py
```

`ragdesk/documents.py` reads and splits files. `retrieval.py` finds passages, and `generation.py` prepares an answer with source references. Results from the sample search are saved in `reports/`.

Built with Python, Streamlit, scikit-learn and pypdf. The sample handbook is fictional and was written for this project. Project code uses the MIT license.
