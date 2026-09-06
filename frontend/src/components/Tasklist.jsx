import { useState, useEffect } from "react";
import Task from "./Task";
import AddTaskForm from "./AddTaskForm"

const API_URL = "http://127.0.0.1:8000";

function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  function fetchTasks() {
    setLoading(true)
    setError(null)
    
    fetch(`${API_URL}/tasks`)
    .then((res) => {
      if(!res) throw new Error(`Errore HTTP: ${res.status}`)
      return res.json()
    }).then((data) => {
        setTasks(data)
        setLoading(false)
    }).catch((err) => {
      setError(err)
      console.log(err.message)
      setLoading(false)
    })
  }

  function deleteTask(id){
    setError(null)

    fetch(`${API_URL}/tasks/${id}`, {"method": "DELETE"})
    .then((res)=>{
      if(!res) throw new Error(`Errore HTTP: ${res.status}`)
      return res.json()
    })
    .then((data)=>{
      
      console.log(data)

      setTasks(tasks => tasks.filter(task => task.id !== id))
    }).catch((err)=>{
      setError(err)
    })
  }

  function classifyWithAI(id){
    setError(null)

    fetch(`${API_URL}/tasks/${id}`, {"method": "PUT"})
    .then((res)=>{
      if(!res) throw new Error(`Errore HTTP: ${res.status}`)
      return res.json()
    })
    .then((data)=>{
      
      setTasks(tasks => tasks.map(task => task.id === data.id ? data : task))
      
    }).catch((err)=>{
      setError(err)
    })
  }

  function completeTask(id){
    setError(null)

    fetch(`${API_URL}/tasks/${id}`, {"method": "PATCH"})
    .then((res)=>{
      if(!res) throw new Error(`Errore HTTP: ${res.status}`)
      return res.json()
    })
    .then((data)=>{
      
      setTasks(tasks => tasks.map(task => task.id === data.id ? data : task))

    }).catch((err)=>{
      setError(err)
    })
  }

  function addTask({ title, description }) {
    setError(null)

    fetch(`${API_URL}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, description })
    })
    .then((res) => {
      if(!res.ok) throw new Error(`Errore HTTP: ${res.status}`)
      return res.json()
    })
    .then((data) => {
      setTasks(tasks => [...tasks, data])
    })
    .catch((err) => {
      setError(err)
    })
  }

  return (
    <>
      <AddTaskForm addFunc={addTask} />
 
      {loading && <p className="task-status">Caricamento task…</p>}
 
      {!loading && error && (
        <p className="task-status">Errore nel caricamento dei task: {error.message}</p>
      )}
 
      {!loading && !error && tasks.length === 0 && (
        <p className="task-empty">Nessun task presente. Aggiungine uno per iniziare.</p>
      )}
 
      {!loading && !error && tasks.length > 0 && (
        <ul className="task-list">
          {tasks.map((task) => (
            <Task
              key={task.id}
              task={task}
              classifyFunc={classifyWithAI}
              deleteFunc={deleteTask}
              completeFunc={completeTask}
            />
          ))}
        </ul>
      )}
    </>
  );
}

export default TaskList;