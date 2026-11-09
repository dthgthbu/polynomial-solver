# Polynomial Solver

Асинхронный сервис вычисления корней многочленов.

## Архитектура

Три контейнера:
- **web** — FastAPI, принимает задачи, отдаёт результаты.
- **worker** — вычислитель, слушает очередь Redis.
- **redis** — брокер сообщений (очередь задач) и хранилище результатов.

Запрос `POST /solve` кладёт задачу в Redis и сразу возвращает `task_id`. Воркер забирает задачу из очереди, считает корни, сохраняет результат. Клиент поллит `GET /tasks/{id}` и ждёт статус `done`.

## Запуск через Docker Compose

    docker compose up -d --build

Сервис: http://localhost:8010

## API

### POST /solve

Создать задачу.

    curl -X POST http://localhost:8010/solve \
      -H "Content-Type: application/json" \
      -d '{"coefficients": [1, -3, 2]}'

Ответ:

    {"task_id": "..."}

### GET /tasks/{task_id}

Получить результат.

    curl http://localhost:8010/tasks/<task_id>

Пока задача не обработана:

    {"status": "pending", "coefficients": "[1, -3, 2]"}

После обработки:

    {"status": "done", "roots": [[1.0, 0.0], [2.0, 0.0]], "coefficients": "[1, -3, 2]"}

`roots` — список пар `[real, imag]`.

### GET /health

Проверка живости + связь с Redis.

## Тесты

    docker compose exec web pytest -v
