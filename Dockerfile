FROM python:3.10-slim

WORKDIR /opt/todolist

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY /core .
COPY /todolist .
COPY .env .
COPY manage.py .
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


