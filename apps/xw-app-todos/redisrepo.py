import json
import redis
import logger

# --- init
log = logger.getLogger("redisrepo")
redis_conn = redis.Redis(host='xw-redis', port=6379, db=0)

# --- cru(d) ops
def find_by_id(id: str):
    todo = redis_conn.get("todo:{0}".format(id))
    if todo:
        log.info("Fetched the todo with id {0}".format(id))
        return json.loads(todo)
    else:
        log.warning("Todo with id {0} not found".format(id))
        return None

def find_all(show_also_completed: bool = False):
    cursor, keys = redis_conn.scan(match="todo:*")
    values = redis_conn.mget(keys)
    todos = []
    for value in values:
        todo = json.loads(value)
        if show_also_completed or not todo["isDone"]:
            todos.append(todo)
    log.info("Fetched a set of {0} todos".format(len(todos)))
    return todos

def save(id: str, todo):
    if redis_conn.set("todo:{0}".format(id), json.dumps(todo)):
        log.info("Saved the todo with id {0}".format(id))
        return todo
    else:
        log.error("Error while saving the todo: {0}".format(json.dumps(todo)))
        return None