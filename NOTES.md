```sh
docker compose up -d \
 && : # docker compose -f docker-compose-with-kafka.yml up -d

# OR

(
  cd backend;
  python -m venv .venv
  source .venv/bin/activate

  python -m pip install -r requirements.txt

  python manage.py runserver
)

(
  cd frontend;
  npm install
  npm run dev
)


```

- open http://localhost:8000
- open http://localhost:3000

```bash
docker compose exec backend python manage.py test
```

```bash
docker compose exec frontend npm test
```

```bash
docker compose down -v --remove-orphans
```
