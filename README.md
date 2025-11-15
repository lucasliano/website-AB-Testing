# RF Analyzer Marketing Site

FastAPI-based marketing site for a high-end open-source RF network analyzer, with:

- A/B testing (hero variants)
- First-party interaction tracking (no external analytics)
- Pages for product, applications, universities, docs, about
- Dockerized deployment
- Tailwind CSS styling

## Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

npm install
npm run build:css

uvicorn app.main:app --reload
```

Open http://localhost:8000

## Docker

```bash
docker build -t rf-site .
docker run -p 80:8000 rf-site
```

Or with Postgres via docker-compose:

```bash
docker-compose up --build
```

Replace placeholder images and PDFs in `app/static/images` and `app/static/docs`.
