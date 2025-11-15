# Easy A/B Testing website

FastAPI-based marketing site, with:

- A/B testing
- First-party interaction tracking (no external analytics)
- Dockerized deployment
- Tailwind CSS styling

# How to use it?
## Running Docker

```bash
docker-compose up --build -d
```

Open [website](localhost:80) -> localhost:80

## Statistics

Open a terminal in the container

```bash
docker exec -it web-server bash
```

And run the python script
```bash
python analytics_cli.py summary
```

Look inside the script. There are various examples of usage there.
