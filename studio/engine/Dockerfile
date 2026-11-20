FROM python:3.12.16-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DJANGO_SETTINGS_MODULE=cmengine.settings
WORKDIR /app
COPY requirements.txt .
RUN pip install --disable-pip-version-check --no-cache-dir --require-hashes --only-binary=:all: -r requirements.txt
COPY cmengine/ cmengine/
COPY reference/ reference/
COPY manage.py .
RUN mkdir /app/media && chown 10001:10001 /app/media
USER 10001:10001
CMD ["sh","-ec","python manage.py migrate --noinput && python manage.py seed_reference && exec gunicorn cmengine.wsgi:application --bind 0.0.0.0:8000 --workers 2"]
