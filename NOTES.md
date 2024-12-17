```sh
docker compose up -d \
 && docker compose -f docker-compose-with-kafka.yml up -d
```

```bash
docker compose exec backend python manage.py test
```

```bash
docker compose exec frontend npm test
```
