
function Task({id, title, description, priority, category, completed}) {

    return(
        <>
        <li key={id}>
            <strong>{title}</strong>
                {description && <p>{description}</p>}
            <small>
                Categoria: {category || "non classificato"} | Priorità:{" "}
                {priority || "-"} | Completato:{" "}
                {completed ? "Sì" : "No"}
            </small>
        </li>
        </>
    )
}

export default Task