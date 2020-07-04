from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
import json
import redisrepo as repo
import logger

# --- init
log = logger.getLogger("api")
elasticapm = make_apm_client({})
app = FastAPI()
app.add_middleware(ElasticAPM, client=elasticapm)

class Todo(BaseModel):
    id: str
    description: str
    isDone: Optional[bool] = False

# --- requests mapping
@app.get('/')
def hello():
    """Greetings"""
    return "So long and thanks for all the fish"

@app.get('/todos/', status_code=200)
def get_todos(showAll: bool = False):
    """Get all the todos object"""
    log.debug("Request: GET '/todos/'")
    return repo.find_all(showAll)

@app.get('/todos/{id}', status_code=200)
def get_todo(id: str):
    """Get the todo object from Redis"""
    log.debug("Request: GET '/todos/{0}'".format(id))
    return _find_todo_by_id(id)

@app.get('/todos/{id}/done', status_code=200)
def set_as_done(id: str):
    """Set the requested todo as done"""
    log.debug("Request: GET '/todos/{0}/done'".format(id))
    return _update_todo_status(id, isDone=True)

@app.get('/todos/{id}/undone', status_code=200)
def set_as_not_done(id: str):
    """Set the requested todo as not done"""
    log.debug("Request: GET '/todos/{0}/undone'".format(id))
    return _update_todo_status(id, isDone=False)

@app.post('/todos/', status_code=200)
def add_todo(todo: Todo):
    """Store the request body into Redis"""
    log.debug("Request: POST '/todos/' ; Id: {0}".format(todo.id))
    return _save_todo(todo.__dict__)

# ---
def _find_todo_by_id(id: str):
    resp = repo.find_by_id(id)
    if not resp:
        raise HTTPException(status_code=404, detail="Todo with id {0} not found".format(id))
    return resp

def _update_todo_status(id: str, isDone: bool):
    todo = _find_todo_by_id(id)
    todo["isDone"] = isDone
    return _save_todo(todo)

def _save_todo(todo):
    resp = repo.save(todo["id"], todo)
    if not resp:
        raise HTTPException(status_code=500, detail="Error while saving the todo: {0}".format(json.dumps(todo)))
    return resp