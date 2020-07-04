FROM python:3.8.0-slim-buster

RUN adduser --home /home/todos --disabled-password todos
WORKDIR /home/todos

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY api.py redisrepo.py logger.py ./
RUN chown -R todos:todos ./
RUN chown -R todos:todos /var/log/

USER todos
CMD uvicorn api:app --host 0.0.0.0 --port 5057