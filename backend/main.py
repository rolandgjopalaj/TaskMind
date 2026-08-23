from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection, init_db

app = FastAPI()
init_db()

# --- Schemi per validare l'input 
class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskUpdate(BaseModel):
    completed: bool | None = None
    title: str | None = None
    description: str | None = None


# ---------------- inizio delle chiamate ------------------
@app.get("/tasks")
def get_tasks(category: str | None = None):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM tasks"
        ).fetchall()
    
    return [dict(row) for row in rows]

@app.post("/tasks")
def create_task(task: TaskCreate):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (task.title, task.description)
    )
    conn.commit()

    new_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (new_id,)).fetchone()
    conn.close()
    return dict(row)