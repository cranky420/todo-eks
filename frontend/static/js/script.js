// Fetch the task list container and input field
const taskList = document.getElementById('task-list');
const taskInput = document.getElementById('task-input');

// Fetch tasks and populate the task list
function fetchTasks() {
    fetch('http://localhost:5000/tasks')
        .then(response => response.json())
        .then(tasks => {
            taskList.innerHTML = ''; // Clear the current list
            tasks.forEach(task => {
                const li = document.createElement('li');
                li.id = task._id.toString(); // Ensure task ID is a string
                li.innerHTML = `${task.task} <button onclick="deleteTask('${task._id}')">Delete</button>`;
                taskList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error fetching tasks:', error);
            alert("Failed to fetch tasks. Please try again.");
        });
}

// Function to add a task
function addTask() {
    const taskText = taskInput.value.trim();
    if (taskText) {
        fetch('http://localhost:5000/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task: taskText })
        })
        .then(response => response.json())
        .then(task => {
            const li = document.createElement('li');
            li.id = task._id.toString(); // Ensure task ID is a string
            li.innerHTML = `${task.task} <button onclick="deleteTask('${task._id}')">Delete</button>`;
            taskList.appendChild(li);
            taskInput.value = ''; // Clear the input field
        })
        .catch(error => {
            console.error('Error adding task:', error);
            alert("Failed to add task. Please try again.");
        });
    } else {
        alert("Task cannot be empty!");
    }
}

// Function to delete a task
function deleteTask(taskId) {
    fetch(`http://localhost:5000/tasks/${taskId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "Task deleted successfully") {
            const taskElement = document.getElementById(taskId);
            if (taskElement) {
                taskElement.remove(); // Remove the task from the DOM
            }
        } else {
            alert("Failed to delete task. Please try again.");
        }
    })
    .catch(error => {
        console.error('Error deleting task:', error);
        alert("Error deleting task. Please try again.");
    });
}

// Load tasks on page load
document.addEventListener("DOMContentLoaded", function() {
    fetchTasks();
});

// Add event listener for the task input form
document.getElementById('add-task-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    addTask();
});

