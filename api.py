from fastapi import FastAPI
from pydantic import BaseModel
from engine import SentinelRAGEngine
import datetime
import json
from middleware.error_handler import global_exception_handler

app = FastAPI(title="SentinelRAG Compliance API")

app.add_exception_handler(
    Exception,
    global_exception_handler
)

engine = SentinelRAGEngine()


class QueryRequest(BaseModel):
    query: str


def log_decision(query, result):
    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "query": query,
        "result": result
    }

    with open("audit_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")


@app.post("/screen")
async def screen_entity(request: QueryRequest):
    result = engine.screen(request.query)
    log_decision(request.query, result)
    return result

class BatchRequest(BaseModel):
    queries: list[str]


@app.post("/batch_screen")
async def batch_screen(request: BatchRequest):
    results = []

    for q in request.queries:
        result = engine.screen(q)
        log_decision(q, result)
        results.append(result)

    return {"results": results}

@app.get("/health")
async def health_check():

    return {
        "status": "healthy",
        "service": "SentinelRAG"
    }