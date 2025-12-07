from fastapi.testclient import TestClient
from app.main import app  # <--- CHANGED: Points to app folder to work from root

# Create a test client
client = TestClient(app)

def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Simple Todo API!"}

def test_get_all_todos():
    """Test retrieving all todos."""
    response = client.get("/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2  # We added 2 in the "db"

def test_create_todo():
    """Test creating a new todo."""
    new_todo = {
        "title": "Test Todo",
        "description": "This is a test",
        "completed": False
    }
    response = client.post("/todos/", json=new_todo)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == new_todo["title"]
    assert data["id"] is not None

def test_get_todo_by_id():
    """Test retrieving a single todo by ID."""
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_todo_not_found():
    """Test retrieving a non-existent todo."""
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}

def test_update_todo():
    """Test updating an existing todo."""
    updated_todo = {
        "title": "Updated Title",
        "description": "Updated Description",
        "completed": True
    }
    response = client.put("/todos/1", json=updated_todo)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_todo["title"]
    assert data["completed"] == True
    
    # Reset it for other tests so we don't break future runs
    client.put("/todos/1", json={"title": "Learn DevOps", "description": "Complete the project", "completed": False})

def test_delete_todo():
    """Test deleting a todo."""
    # First, create a todo to delete
    new_todo = {"title": "To be deleted", "description": "Delete me"}
    response = client.post("/todos/", json=new_todo)
    new_id = response.json()["id"]

    # Now, delete it
    response = client.delete(f"/todos/{new_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/todos/{new_id}")
    assert response.status_code == 404