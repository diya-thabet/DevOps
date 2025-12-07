import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# --- Pydantic Models ---
# These models define the shape of your data and handle validation.

class TodoBase(BaseModel):
    """Base model for a Todo item (used for creation)."""
    title: str
    description: Optional[str] = None
    completed: bool = False

class Todo(TodoBase):
    """Full Todo item model, including its ID."""
    id: int

# --- In-Memory "Database" ---
# A simple list to store our todo items.
db_todos: List[Todo] = [
    Todo(id=1, title="Learn DevOps", description="Complete the project", completed=False),
    Todo(id=2, title="Go to gym", description="Leg day", completed=True),
]
# A counter to simulate auto-incrementing IDs
next_id = 3

# --- FastAPI Application ---
app = FastAPI(
    title="Simple Todo API",
    description="A simple API for the DevOps project.",
    version="1.0.0"
)

# --- API Endpoints ---

@app.get("/", tags=["Root"])
async def read_root():
    """Welcome endpoint."""
    return {"message": "Welcome to the Simple Todo API!"}

@app.post("/todos/", response_model=Todo, status_code=201, tags=["Todos"])
async def create_todo(todo: TodoBase):
    """Create a new todo item."""
    global next_id
    new_todo = Todo(id=next_id, **todo.model_dump())
    db_todos.append(new_todo)
    next_id += 1
    return new_todo

@app.get("/todos/", response_model=List[Todo], tags=["Todos"])
async def get_all_todos():
    """Retrieve all todo items."""
    return db_todos

@app.get("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
async def get_todo_by_id(todo_id: int):
    """Retrieve a single todo item by its ID."""
    todo = next((t for t in db_todos if t.id == todo_id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
async def update_todo(todo_id: int, todo_update: TodoBase):
    """Update an existing todo item."""
    todo = next((t for t in db_todos if t.id == todo_id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update the fields
    todo.title = todo_update.title
    todo.description = todo_update.description
    todo.completed = todo_update.completed
    return todo

@app.delete("/todos/{todo_id}", status_code=204, tags=["Todos"])
async def delete_todo(todo_id: int):
    """Delete a todo item."""
    todo = next((t for t in db_todos if t.id == todo_id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db_todos.remove(todo)
    return  # No content response for 204

# --- Main block to run the app locally ---
if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)