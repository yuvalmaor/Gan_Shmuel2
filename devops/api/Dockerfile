# -v /var/run/docker.sock:/var/run/docker.sock 
FROM python:3.11.8-alpine

WORKDIR /ci
COPY requirements.txt .
RUN pip install --upgrade pip==24.0
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY ./swagger ./swagger
COPY gunicorn_conf.py .

CMD ["gunicorn", "--config", "gunicorn_conf.py"]