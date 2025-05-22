import json
import pytest
from src.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_tasks_empty(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert json.loads(response.data) == []


def test_create_task(client):
    response = client.post(
        '/tasks',
        data=json.dumps({'title': 'Test Task', 'description': 'Test Description'}),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Test Task'
    assert data['description'] == 'Test Description'
    assert data['status'] == 'todo'
    assert 'id' in data


def test_update_task(client):
    # First create a task
    response = client.post(
        '/tasks',
        data=json.dumps({'title': 'Original Title'}),
        content_type='application/json'
    )
    task_id = json.loads(response.data)['id']

    # Now update it
    response = client.put(
        f'/tasks/{task_id}',
        data=json.dumps({'status': 'done'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'done'


def test_delete_task(client):
    # First create a task
    response = client.post(
        '/tasks',
        data=json.dumps({'title': 'Task to Delete'}),
        content_type='application/json'
    )
    task_id = json.loads(response.data)['id']

    # Now delete it
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 204

    # Verify it's gone
    response = client.get('/tasks')
    tasks = json.loads(response.data)
    assert not any(task['id'] == task_id for task in tasks)
