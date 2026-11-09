import json
import os

import redis

from app.solver import find_roots

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
)


def process_task(task_id: str) -> None:
    raw = r.hget(f"task:{task_id}", "coefficients")
    if not raw:
        return

    r.hset(f"task:{task_id}", "status", "running")

    try:
        coefficients = json.loads(raw)
        roots = find_roots(coefficients)
        r.hset(
            f"task:{task_id}",
            mapping={"status": "done", "roots": json.dumps(roots)},
        )
    except Exception as e:
        r.hset(
            f"task:{task_id}",
            mapping={"status": "failed", "error": str(e)},
        )


if __name__ == "__main__":
    print("Worker started, waiting for tasks...", flush=True)
    while True:
        item = r.blpop("tasks_queue", timeout=5)
        if item:
            _, task_id = item
            print(f"Processing task {task_id}", flush=True)
            process_task(task_id)
