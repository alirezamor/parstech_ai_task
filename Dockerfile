FROM python:3.9


RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
COPY requirements.txt /code/

RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "parstech_ai_task.asgi", "-w", "4", "--worker-class", "uvicorn.workers.UvicornWorker"]