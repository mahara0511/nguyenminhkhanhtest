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
from fastapi import FastAPI
from pydantic import BaseModel
import logging


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


if __name__ == "__main__":
    # Fallback to CLI mode when run directly
    cli_loop()
