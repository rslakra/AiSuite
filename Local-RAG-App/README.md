# Local RAG App

Upload a PDF, Markdown, or text file and ask questions about it — entirely on your machine using [Ollama](https://ollama.com) and [ChromaDB](https://www.trychroma.com).

Nothing is sent to the cloud. Your document stays local, embeddings are stored under `APP_DATA_DIR`, and answers come from a local LLM.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/download) running locally

Install Ollama and pull the default models:

```bash
make ollama-install
```

Or manually on macOS:

```bash
brew install ollama
brew services start ollama
ollama pull llama3:8b
ollama pull nomic-embed-text
```



## Quick start

```bash
make setup
make ollama-install
make start
```

Open [http://localhost:8080](http://localhost:8080), upload a file, then ask questions.

## Project layout

```
Local-RAG-App/
├── Makefile              # setup, install, start, clean
├── requirements.txt
├── README.md
├── .env                  # PORT, APP_DATA_DIR, ALLOWED_EXTENSIONS, RAG_PROMPT
├── app_data/             # runtime data (created on start; gitignored)
│   ├── uploads/          # uploaded documents
│   └── chroma_store/     # ChromaDB index
└── app/
    ├── main.py           # entry point (uvicorn target)
    ├── application.py    # FastAPI app factory (LocalRAGApplication)
    ├── container.py      # wires AI services together
    ├── config.py         # Settings class and paths
    ├── webapp/           # templates and HTTP routes
    │   ├── routes/       # BaseRouter + AppRouter
    │   ├── static/
    │   │   ├── css/
    │   │   │   └── styles.css
    │   │   └── js/
    │   │       └── actions.js
    │   └── templates/
    │       └── index.html
    ├── ai/               # AI / LLM service classes
    │   ├── text.py       # TextProcessor — parse and chunk documents
    │   ├── embeddings.py # EmbeddingService — Ollama embeddings
    │   ├── vector_store.py # VectorStore — ChromaDB index + retrieval
    │   ├── llm.py        # LLMService — Ollama chat + model listing
    │   └── rag.py        # RAGService — index, retrieve, answer pipeline
```



## Makefile targets


| Command        | Description                                     |
| -------------- | ----------------------------------------------- |
| `make help`    | Show available commands                         |
| `make setup`   | Create `venv/` and install dependencies         |
| `make install` | Upgrade pip and install from `requirements.txt` |
| `make start`   | Run the app with uvicorn on port 8080           |
| `make stop`    | Stop whatever is listening on the dev port      |
| `make restart`       | Stop then start the app                         |
| `make ollama-install`| Install Ollama, start service, pull models      |
| `make ollama-clean`  | Remove all downloaded Ollama models             |
| `make clean`         | Remove venv and Python cache files              |


Override the port: `make start PORT=9000`

On macOS, port 5000 is often taken by AirPlay Receiver. The default is 8080 to avoid that conflict.

If `make start` fails with **Address already in use**, run `make restart` (or `make stop` then `make start`). `make start` now stops any existing server on the port first.

## How it works

1. **Upload** — the file is saved to `app_data/uploads/` and parsed (PDF via pypdf, plain text as UTF-8).
2. **Chunk & embed** — text is split into overlapping chunks; each chunk is embedded with `nomic-embed-text` via Ollama.
3. **Store** — embeddings and chunk text go into `app_data/chroma_store/`.
4. **Ask** — your question is embedded, the top matching chunks are retrieved, and `llama3:8b` answers using only that context.



## API


| Method | Path          | Description                                                 |
| ------ | ------------- | ----------------------------------------------------------- |
| `GET`  | `/`           | Web UI                                                      |
| `GET`  | `/api/models` | List Ollama chat models                                     |
| `POST` | `/upload`     | Upload a document (`multipart/form-data`, field `file`)     |
| `POST` | `/chat`       | Ask a question (`{"question": "...", "model": "llama3:8b"}`) |




## Configuration

Copy `.env.sample` to `.env` (or run `make setup`). Defaults live in `app/config.py`:


| Setting              | Default            | Purpose                                                               |
| -------------------- | ------------------ | --------------------------------------------------------------------- |
| `APP_DATA_DIR`       | `./app_data`       | Root folder for `uploads/` and `chroma_store/`                        |
| `ALLOWED_EXTENSIONS` | `.pdf,.md,.txt`    | Comma-separated upload file types                                     |
| `RAG_PROMPT`         | built-in template  | Prompt sent to the LLM; use `{context}` and `{question}` placeholders |
| `PORT`               | `8080`             | Dev server port                                                       |
| `CHAT_MODEL`         | `llama3:8b`        | Ollama model for answers (`.env` or `config.py`)                      |
| `embed_model`        | `nomic-embed-text` | Ollama model for embeddings (in `config.py`)                          |
| `chunk_size`         | `500`              | Characters per chunk (in `config.py`)                                 |
| `chunk_overlap`      | `100`              | Overlap between chunks (in `config.py`)                               |
| `top_k`              | `3`                | Chunks retrieved per question (in `config.py`)                        |


Example `.env`:

```bash
APP_DATA_DIR=./app_data
ALLOWED_EXTENSIONS=.pdf,.md,.txt
PORT=8080
RAG_PROMPT="Answer briefly using only this context.\n\nContext:\n{context}\n\nQuestion: {question}"
```

To reset indexed documents and uploads:

```bash
rm -rf app_data
```



## Manual run (without Make)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```



## Notes

- Scanned PDFs (image-only) have no selectable text and cannot be indexed.
- Uploading a new file replaces the previous index.
- Supported formats: `.pdf`, `.txt`, `.md` (max 25 MB).
- Ollama models live in `~/.ollama/models/`. Remove them with `make ollama-clean` (does not delete app `app_data/`).

## Reference
- [Meta Llama 3](https://ollama.com/library/llama3)

