from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_connection, init_db
from ai_service import classify_task_AI, classify_task_MyAiModel


init_db()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
def get_tasks():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM tasks"
        ).fetchall()
    
    conn.close()
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

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()
    result = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    if result.rowcount == 0:
        print("Task da eliminare non trovato!")
        raise HTTPException(status_code=404, detail="Task non trovato!")
    return {"message": "Task eliminato"}

@app.put("/tasks/{task_id}")
def update_tasks(task_id: int):
    conn = get_connection()
    my_task = conn.execute("SELECT description FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not my_task:
        conn.close()
        raise HTTPException(status_code=404, detail="Task non trovato!")

    #estrare la desrizione
    description = dict(my_task)["description"]
    #classificare con AI 
    classification = classify_task_MyAiModel(description)   #classify_task_AI(description) # llama

    conn.execute(
        "UPDATE tasks SET category = ?, priority = ? WHERE id = ?",
        (classification["category"], classification["priority"], task_id)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return dict(row)

@app.patch("/tasks/{task_id}")
def update_task_status(task_id: int):
    conn = get_connection()
    my_task = conn.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not my_task:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    completed = 1 if dict(my_task)["completed"] == 0 else 0

    conn.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
    conn.commit()

    my_task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return(dict(my_task))