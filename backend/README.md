# Backend (FastAPI) - RAG Walks Astana

## Requirements
- Python 3.10+

## Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Run (dev)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints
- GET `/api/health`
- GET `/api/poi`
- POST `/api/poi/import`
- POST `/api/recommend`

## Notes
- Vector store: FAISS (in-memory, persisted to `./data/faiss_index` if present)
- Embeddings: `sentence-transformers` small model for demo
- LLM: mock by default; set `OPENAI_API_KEY` to enable OpenAI if desired (optional, not required)

## Sample POI Import
```bash
curl -X POST http://localhost:8000/api/poi/import \
  -H 'Content-Type: application/json' \
  --data @./sample_poi.json
```


