# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "lunch_decision.wsgi:application"]

#CMD ["python", "mamanage.py", "makemigrations", "python", "manage.py", "migrate", "0.0.0.0:8000"]