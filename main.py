from fasthtml.common import *

todos = []

css = Style("""
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: monospace; background: #fff; color: #000; padding: 2rem; max-width: 600px; margin: 0 auto; }
    h1 { border-bottom: 1px solid #000; padding-bottom: 1rem; margin-bottom: 2rem; font-weight: normal; }
    .add-form { margin-bottom: 2rem; }
    input[type="text"] { width: 100%; padding: 0.5rem; border: 1px solid #000; background: #fff; color: #000; font-family: monospace; }
    button { padding: 0.5rem 1rem; border: 1px solid #000; background: #fff; color: #000; cursor: pointer; font-family: monospace; margin-top: 0.5rem; }
    button:hover { background: #000; color: #fff; }
    .todo-item { border-bottom: 1px solid #ccc; padding: 1rem 0; display: flex; justify-content: space-between; align-items: center; }
    .todo-text.completed { text-decoration: line-through; color: #666; }
    .todo-actions { display: flex; gap: 0.5rem; }
    .todo-actions button { padding: 0.25rem 0.5rem; margin: 0; }
    .empty { color: #666; font-style: italic; text-align: center; padding: 2rem 0; }
""")

app, rt = fast_app(hdrs=(css,))

@rt("/")
def get():
    return (
        Title("Todo App"),
        H1("Todo"),
        Div(
            Form(
                Input(type="text", name="todo", placeholder="Add a new todo...", autofocus=True),
                Button("Add", type="submit"),
                hx_post="/add",
                hx_target="#todo-list",
                hx_swap="innerHTML"
            ),
            cls="add-form"
        ),
        Div(id="todo-list", hx_get="/todos", hx_trigger="load"),
    )

@rt("/todos")
def get_todos():
    if not todos:
        return P("No todos yet. Add one above.", cls="empty")
    return [
        Div(
            Span(todo["text"], cls=f"todo-text {'completed' if todo['completed'] else ''}"),
            Div(
                Button("✓" if not todo["completed"] else "↶",
                      hx_post=f"/toggle/{i}", hx_target="#todo-list", hx_swap="innerHTML"),
                Button("×", hx_post=f"/delete/{i}", hx_target="#todo-list", hx_swap="innerHTML"),
                cls="todo-actions"
            ),
            cls="todo-item"
        )
        for i, todo in enumerate(todos)
    ]

@rt("/add", methods=["POST"])
def add_todo(todo: str):
    if todo.strip():
        todos.append({"text": todo.strip(), "completed": False})
    return RedirectResponse("/todos", status_code=200)

@rt("/toggle/{todo_id}")
def toggle_todo(todo_id: int):
    if 0 <= todo_id < len(todos):
        todos[todo_id]["completed"] = not todos[todo_id]["completed"]
    return RedirectResponse("/todos", status_code=200)

@rt("/delete/{todo_id}")
def delete_todo(todo_id: int):
    if 0 <= todo_id < len(todos):
        todos.pop(todo_id)
    return RedirectResponse("/todos", status_code=200)


serve()
