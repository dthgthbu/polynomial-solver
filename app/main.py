import json
import os
import uuid

import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Polynomial Solver")

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
)


class SolveRequest(BaseModel):
    coefficients: list[float]


@app.post("/solve")
def create_task(req: SolveRequest):
    if not req.coefficients:
        raise HTTPException(400, "coefficients не может быть пустым")

    task_id = str(uuid.uuid4())
    r.hset(
        f"task:{task_id}",
        mapping={
            "status": "pending",
            "coefficients": json.dumps(req.coefficients),
        },
    )
    r.rpush("tasks_queue", task_id)
    return {"task_id": task_id}


@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    data = r.hgetall(f"task:{task_id}")
    if not data:
        raise HTTPException(404, "Task not found")

    if data.get("status") == "done":
        data["roots"] = json.loads(data["roots"])
    return data


@app.get("/health")
def health():
    try:
        r.ping()
        return {"status": "ok", "redis": "ok"}
    except Exception:
        raise HTTPException(503, "redis unavailable")
