FROM python:alpine3.19

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir logs

COPY main.py .

COPY src/ ./src

COPY in/ ./in

ENTRYPOINT [ "python3", "main.py" ]