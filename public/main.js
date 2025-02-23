// main.js

// Function to check if username exists
async function checkUsername() {
    const username = document.getElementById('username').value;
    if (username.length < 5) {
        alert('Username must be at least 5 characters long.');
        return;
    }
    const response = await fetch(`/api/check_username?username=${username}`);
    const data = await response.json();
    if (data.exists) {
        // Username exists, show food input and logs
        document.getElementById('food-input').style.display = 'block';
        document.getElementById('logs').style.display = 'block';
        // Load logs for the user
        loadLogs(username);
    } else {
        // Username does not exist, ask to create new profile
        const create = confirm('Username does not exist. Create a new profile?');
        if (create) {
            createUser(username);
        }
    }
}

// Function to create a new user
async function createUser(username) {
    const response = await fetch('/api/create_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username }),
    });
    const data = await response.json();
    if (data.success) {
        alert('User created successfully!');
        // Show food input and logs
        document.getElementById('food-input').style.display = 'block';
        document.getElementById('logs').style.display = 'block';
    } else {
        alert('Failed to create user.');
    }
}

// Function to analyze food
async function analyzeFood() {
    const images = document.getElementById('food-images').files;
    const description = document.getElementById('food-description').value;
    const formData = new FormData();
    for (let image of images) {
        formData.append('images', image);
    }
    formData.append('description', description);
    const response = await fetch('/api/analyze_food', {
        method: 'POST',
        body: formData,
    });
    const data = await response.json();
    // Display analysis results
    document.getElementById('summary').innerText = data.summary;
    const table = document.getElementById('macros-table').querySelector('tbody tr');
    table.children[0].innerText = description || 'N/A';
    table.children[1].innerText = data.protein;
    table.children[2].innerText = data.carbs;
    table.children[3].innerText = data.fat;
    table.children[4].innerText = data.calories;
    document.getElementById('analysis-results').style.display = 'block';
}

// Function to approve and log the entry
async function approveLog() {
    const username = document.getElementById('username').value;
    const table = document.getElementById('macros-table').querySelector('tbody tr');
    const description = table.children[0].innerText;
    const protein = table.children[1].innerText;
    const carbs = table.children[2].innerText;
    const fat = table.children[3].innerText;
    const calories = table.children[4].innerText;
    const response = await fetch('/api/add_log', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, description, protein, carbs, fat, calories }),
    });
    const data = await response.json();
    if (data.success) {
        alert('Log added successfully!');
        // Reload logs
        loadLogs(username);
    } else {
        alert('Failed to add log.');
    }
}

// Function to load logs
async function loadLogs(username) {
    const response = await fetch(`/api/get_logs?username=${username}`);
    const data = await response.json();
    const logsTable = document.getElementById('logs-table').querySelector('tbody');
    logsTable.innerHTML = '';
    data.logs.forEach(log => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${log.timestamp}</td>
            <td>${log.description}</td>
            <td>${log.protein}</td>
            <td>${log.carbs}</td>
            <td>${log.fat}</td>
            <td>${log.calories}</td>
        `;
        logsTable.appendChild(row);
    });
}

// Event listeners
document.getElementById('check-username').addEventListener('click', checkUsername);
document.getElementById('analyze-food').addEventListener('click', analyzeFood);
document.getElementById('approve-log').addEventListener('click', approveLog);