import TaskList from './components/Tasklist'
import './App.css'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>TaskMind</h1>
        <p>Scrivi cosa devi fare, il resto lo capisce l'AI.</p>
      </header>

      <TaskList />
    </div>
  )
}

export default App