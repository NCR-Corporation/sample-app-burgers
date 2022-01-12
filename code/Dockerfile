FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt && \
    python manage.py collectstatic --noinput && \
    chmod -R 777 /app

EXPOSE 8000/tcp

ENTRYPOINT ["build/cloudbuild/django/docker-startup.sh"]