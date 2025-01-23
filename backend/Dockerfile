  GNU nano 7.2                                                                        Dockerfile
FROM python:3.11

WORKDIR /app

COPY app.py /app

RUN pip install flask flask-cors paramiko

CMD ["python", "app.py"]
