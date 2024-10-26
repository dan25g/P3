FROM python:3.6-slim-buster

WORKDIR /app

COPY requirements.txt ./

COPY .env ./

RUN pip install -r requirements.txt

COPY  . .

EXPOSE 4000

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:4000", "-w", "4"]