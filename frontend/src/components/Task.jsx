const PRIORITY_COLOR = {
  alta: 'var(--cat-urgente)',
  media: 'var(--cat-studio)',
  bassa: 'var(--text-faint)',
}

function Task({ task, classifyFunc, deleteFunc, completeFunc }) {
  const priorityColor = PRIORITY_COLOR[task.priority] || null

  return (
    <li className={`task-row${task.completed ? ' completed' : ''}`}>
      <button
        className={`task-toggle${task.completed ? ' done' : ''}`}
        onClick={() => completeFunc(task.id)}
        aria-label={task.completed ? 'Segna come da fare' : 'Segna come completato'}
      >
        {task.completed && (
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path
              d="M4 12l5 5L20 6"
              stroke="currentColor"
              strokeWidth="3"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        )}
      </button>

      <div className="task-body">
        <span className="task-title">{task.title || 'Senza titolo'}</span>
        {task.description && <p className="task-description">{task.description}</p>}

        <div className="task-meta">
          <span className={`task-tag${task.category ? ` category-${task.category}` : ''}`}>
            {task.category || 'non classificato'}
          </span>
          {task.priority && (
            <span className="task-tag" style={{ '--cat-color': priorityColor }}>
              {task.priority}
            </span>
          )}
        </div>
      </div>

      <div className="task-actions">
        <button onClick={() => classifyFunc(task.id)}>Classifica</button>
        <button className="delete-btn" onClick={() => deleteFunc(task.id)}>
          Elimina
        </button>
      </div>
    </li>
  )
}

export default Task