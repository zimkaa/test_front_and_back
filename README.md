# Simple backend and frontend

## 1. Clone project

```sh
git clone git@github.com:zimkaa/test_front_and_back.git && cd test_front_and_back
```

## 2. Start project

```sh
docker compose -f compose.yaml up --build
```

## 3. Query from console

### Success query

```sh
curl -sv -XPOST -H 'Content-Type: application/json' -d '{"first_name": "Ivan", "last_name": "Ivanov", "date": "2025-01-02"}' http://localhost:8000/api/submit
```

### Fail queries

```sh
curl -sv -XPOST -H 'Content-Type: application/json' -d '{"first_name": "Ivan Ivanov", "last_name": "Ivanov", "date": "2025-01-02"}' http://localhost:8000/api/submit
```

```sh
curl -sv -XPOST -H 'Content-Type: application/json' -d '{"first_name": "Ivan", "last_name": "Ivanov", "date": "2025-55-02"}' http://localhost:8000/api/submit
```

### 4. Query from browser

Open your browser

[http://localhost:8000/](http://localhost:8000/)
