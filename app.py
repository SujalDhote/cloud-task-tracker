import os
import logging
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("cloud-task-tracker")

# Demo-only in-memory storage. Tasks reset when the service restarts.
tasks = [
    {"id": 1, "title": "Review cloud architecture", "done": False},
    {"id": 2, "title": "Test application endpoint", "done": True},
]
next_id = 3

@app.get("/")
def home():
    logger.info("Home page requested")
    return render_template("index.html")

@app.get("/health")
def health():
    """Lightweight health endpoint for uptime checks."""
    return jsonify(status="ok", service="cloud-task-tracker"), 200

@app.get("/api/tasks")
def list_tasks():
    logger.info("Task list requested; count=%d", len(tasks))
    return jsonify(tasks), 200

@app.post("/api/tasks")
def create_task():
    global next_id
    payload = request.get_json(silent=True) or {}
    title = str(payload.get("title", "")).strip()
    if not title:
        logger.warning("Rejected task creation: empty title")
        return jsonify(error="title is required"), 400
    if len(title) > 120:
        logger.warning("Rejected task creation: title too long")
        return jsonify(error="title must be 120 characters or fewer"), 400
    task = {"id": next_id, "title": title, "done": False}
    next_id += 1
    tasks.append(task)
    logger.info("Task created; task_id=%d", task["id"])
    return jsonify(task), 201

@app.patch("/api/tasks/<int:task_id>")
def update_task(task_id):
    payload = request.get_json(silent=True) or {}
    for task in tasks:
        if task["id"] == task_id:
            if "done" not in payload or not isinstance(payload["done"], bool):
                return jsonify(error="done must be a boolean"), 400
            task["done"] = payload["done"]
            logger.info("Task updated; task_id=%d done=%s", task_id, task["done"])
            return jsonify(task), 200
    logger.warning("Task update failed; task_id=%d not found", task_id)
    return jsonify(error="task not found"), 404

@app.errorhandler(404)
def not_found(_error):
    return jsonify(error="not found"), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
