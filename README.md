# Harbor Catalog API

Portfolio project by Shagun Sharma. A FastAPI service for a product catalog and available-to-promise stock checks. This is original sample code for review, not an employer codebase.

## Stack

Python 3.11, FastAPI, SQLAlchemy 2, Pydantic v2, SQLite, pytest, Docker.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Run with Docker

```bash
docker compose up --build
```

## Tests

```bash
pytest
```

## API

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Process check |
| GET, POST | `/api/v1/categories` | List or create a category |
| GET, POST | `/api/v1/products` | Search or create a product |
| GET, PATCH | `/api/v1/products/{sku}` | Read or update one product |
| POST | `/api/v1/inventory/{sku}/receive` | Add on-hand units |
| POST | `/api/v1/inventory/{sku}/reserve` | Hold units if stock allows |
| GET | `/api/v1/inventory/{sku}/atp?quantity=` | Available-to-promise check |

Search accepts `q`, `category`, `page`, and `page_size`.

## Layout

```
app/main.py              application factory
app/models.py            category, product, stock
app/services/catalog.py  catalog rules
app/services/inventory.py  receive, reserve, ATP
app/routers/             HTTP layer
tests/                   API tests on an in-memory database
```

Prices are stored in the smallest currency unit (`price_cents`) so the API never uses floating-point money.
