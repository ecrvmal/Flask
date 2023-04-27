FROM python:3.9.1-buster

WORKDIR /app

COPY requirements.txt requirements.txt
# RUN apt-get update
RUN pip install --no-cache -r requirements.txt

# COPY . .
COPY wsgi.py wsgi.py
COPY blog ./blog
COPY wait-for-postgres.sh wait-for-postgres.sh

EXPOSE 5000

CMD ["python3","-m","flask","run","--host=0.0.0.0"]
# CMD ["python","wsgi.py"]