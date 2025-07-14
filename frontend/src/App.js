import React, { useEffect, useState } from "react";

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTaskName, setNewTaskName] = useState("");// 👈 state for input

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = () => {
    fetch("http://localhost:8000/tasks")
      .then((res) => res.json())
      .then((data) => setTasks(data))
      .catch((err) => console.error("Failed to fetch tasks:", err));
  };

  const handleAddTask = () => {
    if (!newTaskName.trim()) return; // prevent empty tasks

    fetch("http://localhost:8000/task", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        taskName: newTaskName,
        isCompleted: false,
      }),
    })
      .then((res) => res.json())
      .then(() => {
        setNewTaskName("");    // clear the input
        fetchTasks();          // refresh the list
      })
      .catch((err) => console.error("Failed to add task:", err));
  };

  const handleToggleComplete = (id, taskName, newStatus) => {
  fetch(`http://localhost:8000/tasks/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ taskName: taskName, isCompleted: newStatus }),
  })
    .then((res) => {
      if (!res.ok) throw new Error("Request failed");
      return res.json();
    })
    .then(() => fetchTasks())
    .catch((err) => console.error("❌ Failed to update task:", err));
  };

  const handleDeleteTask = (id) => {
  if (!window.confirm("Are you sure you want to delete this task?")) return;

  fetch(`http://localhost:8000/tasks/${id}`, {
    method: "DELETE",
  })
    .then((res) => {
      if (!res.ok) throw new Error("Delete failed");
      return res.text();  // or `.json()` if you return JSON
    })
    .then(() => fetchTasks())  // reload list
    .catch((err) => console.error("❌ Failed to delete task:", err));
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>📝 Task Manager</h1>

      {/* 🔹 Add Task Form */}
      <div>
        <input
          type="text"
          value={newTaskName}
          onChange={(e) => setNewTaskName(e.target.value)}
          placeholder="Enter new task"
        />
        <button onClick={handleAddTask}>Add</button>
      </div>

      {/* 🔹 Task List */}
      <ul>
        {tasks.map((task) => (
          <li
            key={task.id}
            onClick={() =>
              handleToggleComplete(task.id, task.taskName, !task.isCompleted)
            }
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              padding: "0.5rem",
              borderBottom: "1px solid #ddd",
              cursor: "pointer",
            }}
          >
            {/* ✅ Task Text (click to toggle) */}
            <span>
              {task.taskName} — {task.isCompleted ? "✅" : "❌"}
            </span>

            {/* 🗑 Delete Button (does NOT trigger toggle) */}
            <button
              onClick={(e) => {
                e.stopPropagation(); // ❗ prevent toggle when deleting
                handleDeleteTask(task.id);
              }}
            >
              🗑
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;