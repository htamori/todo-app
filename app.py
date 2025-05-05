from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# In-memory storage for todos
todos = []

# HTML template for the frontend
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Todo App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .todo-container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .todo-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
        .todo-item:last-child {
            border-bottom: none;
        }
        .todo-form {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        input[type="text"] {
            flex-grow: 1;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            padding: 8px 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .delete-btn {
            background-color: #f44336;
        }
        .delete-btn:hover {
            background-color: #da190b;
        }
    </style>
</head>
<body>
    <div class="todo-container">
        <h1>Todo List</h1>
        <div class="todo-form">
            <input type="text" id="todoInput" placeholder="Enter a new todo">
            <button onclick="addTodo()">Add Todo</button>
        </div>
        <div id="todoList"></div>
    </div>

    <script>
        function fetchTodos() {
            fetch('/todos')
                .then(response => response.json())
                .then(todos => {
                    const todoList = document.getElementById('todoList');
                    todoList.innerHTML = '';
                    todos.forEach((todo, index) => {
                        const todoItem = document.createElement('div');
                        todoItem.className = 'todo-item';
                        todoItem.innerHTML = `
                            <span>${todo.text} <small>(${todo.date})</small></span>
                            <button class="delete-btn" onclick="deleteTodo(${index})">Delete</button>
                        `;
                        todoList.appendChild(todoItem);
                    });
                });
        }

        function addTodo() {
            const input = document.getElementById('todoInput');
            const text = input.value.trim();
            if (text) {
                fetch('/todos', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: text }),
                })
                .then(response => response.json())
                .then(() => {
                    input.value = '';
                    fetchTodos();
                });
            }
        }

        function deleteTodo(index) {
            fetch(`/todos/${index}`, {
                method: 'DELETE',
            })
            .then(() => fetchTodos());
        }

        // Initial load
        fetchTodos();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    if 'text' in data:
        todo = {
            'text': data['text'],
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        todos.append(todo)
        return jsonify({'message': 'Todo added successfully'}), 201
    return jsonify({'error': 'Text is required'}), 400

@app.route('/todos/<int:index>', methods=['DELETE'])
def delete_todo(index):
    if 0 <= index < len(todos):
        todos.pop(index)
        return jsonify({'message': 'Todo deleted successfully'})
    return jsonify({'error': 'Todo not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=57305, debug=True)