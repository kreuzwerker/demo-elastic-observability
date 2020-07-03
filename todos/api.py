from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import redisrepo as repo
import logger

log = logger.getLogger("api")
app = FastAPI()

class Todo(BaseModel):
    id: str
    description: str
    isDone: Optional[bool] = False

def _change_todo_status(id: str, isDone: bool):
    todo_resp = repo.find_by_id(id)
    if not isinstance(todo_resp, dict):
        return todo_resp
    todo_resp["isDone"] = isDone
    return repo.save(id, todo_resp)

## REST Endpoints ##
@app.get('/')
def hello():
    """Greetings"""
    return "So long and thanks for all the fish"

@app.get('/todos/', status_code=200)
def get_todos(showAll: bool = False):
    """Get all the todos object"""
    log.debug("Request: GET '/todos/'")
    resp = repo.find_all(showAll)
    return resp

@app.get('/todos/{id}', status_code=200)
def get_todo(id: str):
    """Get the todo object from Redis"""
    log.debug("Request: GET '/todos/{0}'".format(id))
    resp = repo.find_by_id(id)
    return resp

@app.get('/todos/{id}/done', status_code=200)
def set_as_done(id: str):
    """Set the requested todo as done"""
    log.debug("Request: GET '/todos/{0}/done'".format(id))
    resp = _change_todo_status(id, isDone=True)
    return resp

@app.get('/todos/{id}/undone', status_code=200)
def set_as_not_done(id: str):
    """Set the requested todo as not done"""
    log.debug("Request: GET '/todos/{0}/undone'".format(id))
    resp = _change_todo_status(id, isDone=False)
    return resp

@app.post('/todos/', status_code=200)
def add_todo(todo: Todo):
    """Store the request body into Redis"""
    log.debug("Request: POST '/todos/' ; Id: {0}".format(todo.id))
    resp = repo.save(todo.id, todo.__dict__)
    return resp

