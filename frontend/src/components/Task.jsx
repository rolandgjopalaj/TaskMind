
function Task({task, classifyFunc, deleteFunc, completeFunc}) {

    return(
        <>
        <li key={task.id}>
            <button onClick={()=>completeFunc(task.id)}>{task.completed ? "✓" : "X"}</button>
            <strong>{task.title}</strong>
                {task.description && <p>{task.description}</p>}
            <small>
                Categoria: {task.category || "non classificato"} | Priorità:{" "}
                {task.priority || "-"} | Completato:{" "}
                {task.completed ? "Sì" : "No"}
            </small>
            <button onClick={()=>classifyFunc(task.id)}>AI</button>
            <button onClick={()=>deleteFunc(task.id)}>Delete</button>
        </li>
        </>
    )
}

export default Task