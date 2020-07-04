FROM python:3.8.0-slim-buster

RUN adduser --home /home/reports --disabled-password reports
WORKDIR /home/reports

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY api.py logger.py DejaVuSansCondensed.ttf ./
RUN chown -R reports:reports ./
RUN chown -R reports:reports /var/log/

USER reports
CMD uvicorn api:app --host 0.0.0.0 --port 5058