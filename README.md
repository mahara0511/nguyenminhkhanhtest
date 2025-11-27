# RAG Assistant with Daily Scraper

AI-powered assistant using RAG (Retrieval-Augmented Generation) with Gemini embeddings and ChromaDB. Features automated daily scraper with delta detection.

## Prerequisites

- Docker
- Gemini API Key ([Get here](https://ai.google.dev/))

## Setup

```bash
git clone https://github.com/mahara0511/nguyenminhkhanhtest.git
cd nguyenminhkhanhtest
```

## Run Locally with Docker

**1. Build image:**

```bash
docker build -t optibot .
```

**2. Run API:**

```bash
docker run -d --name optibot-api -p 8000:8000 \
  -e GEMINI_API_KEY="your_key" \
  -v $(pwd)/chroma_storage:/app/chroma_storage \
  -v $(pwd)/logs:/app/logs \
  optibot
```

**3. Run Scraper (one-time):**

```bash
docker run --rm \
  -e GEMINI_API_KEY="your_key" \
  -v $(pwd)/chroma_storage:/app/chroma_storage \
  -v $(pwd)/logs:/app/logs \
  optibot python main.py
```

**4. Test API:**

- Swagger UI: http://localhost:8000/docs
- Example: `curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"query": "How to setup digital signage?"}'`

**5. Check logs:**

```bash
cat logs/last_run_log.json
# Or: curl http://localhost:8000/logs/last-run
```

## Production Deployment

**Live API:** http://4.241.170.167  
**Swagger:** http://4.241.170.167/docs  
**Daily Job Logs:** http://4.241.170.167/logs/last-run

## License

MIT

## Author

mahara0511
