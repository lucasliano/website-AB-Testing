# Stage 1: Build Tailwind CSS
FROM node:22-alpine AS frontend-build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY tailwind.config.cjs postcss.config.cjs ./
COPY app/static/css ./app/static/css
COPY app/templates ./app/templates
COPY app/static/js ./app/static/js
RUN npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/main.css --minify

# Stage 2: Python app
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY --from=frontend-build /app/app/static/css/main.css ./app/static/css/main.css

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
