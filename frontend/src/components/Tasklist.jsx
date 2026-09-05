import { useState, useEffect } from "react";
import Task from "./Task";

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
      if(!res) throw new Error()
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
      if(!res) throw new Error()
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
      if(!res) throw new Error()
      return res.json()
    })
    .then((data)=>{
      
      setTasks(tasks => tasks.map(task => task.id === data.id ? data : task))

    }).catch((err)=>{
      setError(err)
    })
  }


  if (loading) return <p>Caricamento task...</p>;
  if (error) return <p>Errore nel caricamento dei task: {error}</p>;
  if (tasks.length === 0) return <p>Nessun task presente.</p>;

  return (
    <div>
      <h2>I miei task</h2>
      <ul>
        {tasks.map((task)=>(
          <Task
            task={task}
            classifyFunc={classifyWithAI}
            deleteFunc={deleteTask}
            completeFunc={completeTask}
          />
        ))}
      </ul>
    </div>
  );
}

export default TaskList;