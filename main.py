from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import json
import os

app = Flask(__name__)

TODOS_FILE = 'todos.json'

def load_todos():
    if os.path.exists(TODOS_FILE):
        with open(TODOS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(TODOS_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Todo App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .add-form {
            display: flex;
            margin-bottom: 30px;
            gap: 10px;
        }
        .add-form input {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        .add-form button {
            padding: 12px 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .add-form button:hover {
            background: #0056b3;
        }
        .todo-item {
            display: flex;
            align-items: center;
            padding: 15px;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-radius: 5px;
            border: 1px solid #e9ecef;
        }
        .todo-item input[type="checkbox"] {
            margin-right: 15px;
            transform: scale(1.2);
        }
        .todo-text {
            flex: 1;
            font-size: 16px;
        }
        .todo-text.completed {
            text-decoration: line-through;
            color: #6c757d;
        }
        .delete-btn {
            background: #dc3545;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 14px;
        }
        .delete-btn:hover {
            background: #c82333;
        }
        .empty-state {
            text-align: center;
            color: #6c757d;
            font-style: italic;
            padding: 40px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>My Todo App</h1>

        <form class="add-form" method="POST" action="/add">
            <input type="text" name="task" placeholder="Add a new todo..." required>
            <button type="submit">Add</button>
        </form>

        {% if todos %}
            {% for todo in todos %}
            <div class="todo-item">
                <form method="POST" action="/toggle/{{ loop.index0 }}" style="display: inline;">
                    <input type="checkbox" {% if todo.done %}checked{% endif %} onchange="this.form.submit()">
                </form>
                <span class="todo-text {% if todo.done %}completed{% endif %}">{{ todo.task }}</span>
                <form method="POST" action="/delete/{{ loop.index0 }}" style="display: inline;">
                    <button type="submit" class="delete-btn">Delete</button>
                </form>
            </div>
            {% endfor %}
        {% else %}
            <div class="empty-state">
                No todos yet. Add one above to get started!
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    todos = load_todos()
    return render_template_string(HTML_TEMPLATE, todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    if task:
        todos = load_todos()
        todos.append({'task': task, 'done': False})
        save_todos(todos)
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle_todo(todo_id):
    todos = load_todos()
    if 0 <= todo_id < len(todos):
        todos[todo_id]['done'] = not todos[todo_id]['done']
        save_todos(todos)
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todos = load_todos()
    if 0 <= todo_id < len(todos):
        todos.pop(todo_id)
        save_todos(todos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)