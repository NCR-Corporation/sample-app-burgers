FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app
COPY . /app
RUN chmod +x /app

RUN pip install -r requirements.txt && \
    python manage.py collectstatic --noinput

RUN apt-get update && \
    apt-get install -y sqlite3

RUN cd ..
RUN chmod -R 777 /app
EXPOSE 8000/tcp

CMD ["/bin/sh", "build/cloudbuild/django/docker-startup.sh"]
