# run.py
from assistant.graph import build_assistant_graph
from dotenv import load_dotenv

# Load environment variables (e.g., GEMINI_API_KEY)
load_dotenv()

graph = build_assistant_graph()

# ---------------
# CLI ENTRYPOINT
# ---------------
def cli_loop() -> None:
    """Simple CLI loop for local testing."""
    while True:
        q = input("Ask: ")
        out = graph.invoke({"query": q})
        print("\nANSWER:\n", out["answer"])
        print("\n-----------------------------------------\n")


# ---------------
# HTTP API (FastAPI)
# ---------------
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import json
import os


app = FastAPI(title="Optibot Assistant API", version="1.0.0")


@app.on_event("startup")
async def log_swagger_url() -> None:
    """Log the Swagger UI URL when the app starts."""
    # In Docker / production, the external host will often be behind a LB,
    # but logging localhost is still useful for local/dev.
    logging.getLogger("uvicorn").info("Swagger UI available at /docs")


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str


@app.post("/ask", response_model=AskResponse, summary="Ask the assistant")
def ask_endpoint(body: AskRequest) -> AskResponse:
    """Accept a user question and return the assistant answer."""
    result = graph.invoke({"query": body.question})
    answer = result.get("answer", "")
    return AskResponse(answer=answer)


@app.get("/logs/last-run", summary="Get last scraper run log", tags=["logs"])
def get_last_run_log():
    """Return the last scraper job run log with added/updated/skipped counts."""
    log_path = "/var/log/optibot/last_run_log.json"
    
    # For local development, try current directory
    if not os.path.exists(log_path):
        log_path = "last_run_log.json"
    
    if not os.path.exists(log_path):
        raise HTTPException(
            status_code=404,
            detail="No scraper run log found. Job may not have run yet."
        )
    
    try:
        with open(log_path, "r") as f:
            log_data = json.load(f)
        return log_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading log: {str(e)}")


@app.get("/", tags=["health"])
def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Optibot Assistant API",
        "endpoints": {
            "ask": "/ask",
            "swagger": "/docs",
            "last_run_log": "/logs/last-run"
        }
    }


if __name__ == "__main__":
    # Fallback to CLI mode when run directly
    cli_loop()
