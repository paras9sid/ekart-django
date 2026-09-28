FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /ekart

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD python manage.py runserver 0.0.0.0:8000