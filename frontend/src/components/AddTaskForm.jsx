import { useState } from "react";

function AddTaskForm({ addFunc }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!description.trim()) return;

    addFunc({ title, description });

    setTitle("");
    setDescription("");
  }

  return (
    <form className="add-task-form" onSubmit={handleSubmit}>
      <input
        type="text"
        className="field-title"
        placeholder="Titolo (opzionale)"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <div className="divider" />
      <input
        type="text"
        placeholder="Cosa devi fare?"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <div className="add-task-form-actions">
        <button type="submit" disabled={!description.trim()}>
          Aggiungi task
        </button>
      </div>
    </form>
  );
}

export default AddTaskForm;