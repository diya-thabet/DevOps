import uvicorn
import logging
import time
import uuid
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from prometheus_fastapi_instrumentator import Instrumentator # New import

# --- 1. Logging Setup (Structured Logs) ---
# We configure logs to look like JSON for better parsing
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Pydantic Models ---
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class Todo(TodoBase):
    id: int

# --- In-Memory Database ---
db_todos: List[Todo] = [
    Todo(id=1, title="Learn DevOps", description="Complete the project", completed=False),
    Todo(id=2, title="Go to gym", description="Leg day", completed=True),
]
next_id = 3

# --- FastAPI Application ---
app = FastAPI(
    title="Simple Todo API",
    description="A simple API for the DevOps project.",
    version="1.0.0"
)

# --- 2. Tracing Middleware ---
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # Generate a unique ID for this request (Tracing)
    request_id = str(uuid.uuid4())
    logger.info(f"Request started - ID: {request_id} - Path: {request.url.path}")
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Add custom headers for observability
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    logger.info(f"Request completed - ID: {request_id} - Duration: {process_time:.4f}s")
    return response

# --- 3. Prometheus Metrics ---
# This automatically creates a /metrics endpoint
Instrumentator().instrument(app).expose(app)

# --- API Endpoints ---
@app.get("/", tags=["Root"])
async def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Simple Todo API!"}

@app.post("/todos/", response_model=Todo, status_code=201, tags=["Todos"])
async def create_todo(todo: TodoBase):
    global next_id
    new_todo = Todo(id=next_id, **todo.model_dump())
    db_todos.append(new_todo)
    next_id += 1
    logger.info(f"Created new todo: {new_todo.id}")
    return new_todo

@app.get("/todos/", response_model=List[Todo], tags=["Todos"])
async def get_all_todos():
    return db_todos

@app.get("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
async def get_todo_by_id(todo_id: int):
    todo = next((t for t in db_todos if t.id == todo_id), None)
    if todo is None:
        logger.warning(f"Todo not found: {todo_id}")
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
async def update_todo(todo_id: int, todo_update: TodoBase):
    todo = next((t for t in db_todos if t.id == todo_id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.title = todo_update.title
    todo.description = todo_update.description
    todo.completed = todo_update.completed
    logger.info(f"Updated todo: {todo_id}")
    return todo

@app.delete("/todos/{todo_id}", status_code=204, tags=["Todos"])
async def delete_todo(todo_id: int):
    todo = next((t for t in db_todos if t.id == todo_id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db_todos.remove(todo)
    logger.info(f"Deleted todo: {todo_id}")
    return

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) # nosec