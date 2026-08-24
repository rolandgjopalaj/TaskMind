import { useState, useEffect } from "react";

const API_URL = "http://127.0.0.1:8000";

function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  function fetchTasks() {
    setLoading(true);
    setError(null);

    fetch(`${API_URL}/tasks`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Errore HTTP: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        setTasks(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }

  if (loading) return <p>Caricamento task...</p>;
  if (error) return <p>Errore nel caricamento dei task: {error}</p>;
  if (tasks.length === 0) return <p>Nessun task presente.</p>;

  return (
    <div>
      <h2>I miei task</h2>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            <strong>{task.title}</strong>
            {task.description && <p>{task.description}</p>}
            <small>
              Categoria: {task.category || "non classificato"} | Priorità:{" "}
              {task.priority || "-"} | Completato:{" "}
              {task.completed ? "Sì" : "No"}
            </small>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TaskList;