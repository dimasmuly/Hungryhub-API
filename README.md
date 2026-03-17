# HungryHub Take-Home: Restaurant Menu Management API

REST API for managing restaurants and menu items, built with FastAPI, SQLAlchemy, and MySQL.

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy 2.x
- MySQL 8
- PyMySQL (DB driver)
- Docker & Docker Compose
- Pytest

## Main Features

- CRUD for Restaurant
- CRUD for Menu Item (per restaurant)
- One-to-many relationship between Restaurant and Menu Item
- Input validation with clear error messages
- Proper HTTP status codes (200, 201, 400, 404, 401, 204)
- Seed data:
  - 2 restaurants
  - Each with at least 5 menu items
- Simple authentication using an API key (header `X-API-Key`)
- Pagination for list endpoints
- Filter and search on menu items:
  - Filter by `category`
  - Search by `name` (query parameter `search`)

## Project Structure

- `app/config.py` – application configuration (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, API_KEY)
- `app/database.py` – database connection and session
- `app/models.py` – SQLAlchemy models (Restaurant, MenuItem)
- `app/schemas.py` – Pydantic schemas for request/response
- `app/main.py` – FastAPI application and router registration
- `app/routers/` – route definitions (restaurants, menu items)
- `app/services/` – service layer / business logic
- `app/initial_data.py` – database seeding on startup
- `tests/` – basic integration tests with Pytest
- `Dockerfile`, `docker-compose.yml` – Docker setup

## Running Locally (Without Docker)

1. Create and activate a virtualenv (optional but recommended).

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Make sure MySQL is running and the database exists:

- Database name: `takehometest-hungryhub`
- Example SQL:

     ```sql
     CREATE DATABASE `takehometest-hungryhub` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
     CREATE USER 'hungryhub'@'%' IDENTIFIED BY 'hungryhub';
     GRANT ALL PRIVILEGES ON `takehometest-hungryhub`.* TO 'hungryhub'@'%';
     FLUSH PRIVILEGES;
     ```

4. Create a `.env` file in the project root (required for MySQL and API key configuration):

   ```env
   DB_USER=hungryhub
   DB_PASSWORD=hungryhub
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=takehometest-hungryhub
   API_KEY=supersecretapikey
   ```

5. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

6. The API will be available at:

- `http://localhost:8000`
- Automatic Swagger documentation: `http://localhost:8000/docs`

## Running with Docker

Make sure Docker and Docker Compose are installed.

1. Run:

   ```bash
   docker-compose up --build
   ```

2. Services:

- API: `http://localhost:8000`
- MySQL: `localhost:3306`

3. Important environment variables in `docker-compose.yml`:

- Database:
  - `MYSQL_DATABASE=takehometest-hungryhub`
  - `MYSQL_USER=hungryhub`
  - `MYSQL_PASSWORD=hungryhub`
- API:
  - `DB_USER=hungryhub`
  - `DB_PASSWORD=hungryhub`
  - `DB_HOST=db`
  - `DB_PORT=3306`
  - `DB_NAME=takehometest-hungryhub`
  - `API_KEY=supersecretapikey`

## Seed Data

On application startup:

- Create tables if they do not exist
- Check the number of restaurants
- If 0, automatically insert:
  - Restaurant `Bangkok Spice` with 5 menu items
  - Restaurant `Chiang Mai Garden` with 5 menu items

Seeding logic is in `app/initial_data.py` inside `seed_data()`.

## Authentication

All endpoints require a simple API key via header:

- Header: `X-API-Key: supersecretapikey`

If the header is missing or the value is incorrect, the API returns:

- `401 Unauthorized` with message `Invalid API key`

## API Endpoints

### Restaurant

- `POST /restaurants`
  - Create restaurant
  - Body:

    ```json
    {
      "name": "string",
      "address": "string",
      "phone": "string (optional)",
      "opening_hours": "string (optional)"
    }
    ```

  - Response: `201 Created`, body `RestaurantRead`

- `GET /restaurants`
  - List restaurant dengan paginasi
  - Query params:
    - `page` (default 1)
    - `page_size` (default 10, max 100)
  - Response: `PaginatedRestaurants`

- `GET /restaurants/{id}`
  - Detail restaurant beserta menu items
  - Response: `RestaurantWithMenuItems`

- `PUT /restaurants/{id}`
  - Update restaurant (semua field optional)
  - Body: `RestaurantUpdate`

- `DELETE /restaurants/{id}`
  - Delete restaurant
  - Response: `204 No Content`

### Menu Item

- `POST /restaurants/{id}/menu_items`
  - Tambah menu item ke restaurant tertentu
  - Body:

    ```json
    {
      "name": "string",
      "description": "string (optional)",
      "price": "decimal string, > 0",
      "category": "appetizer|main|dessert|drink|... (optional)",
      "is_available": true
    }
    ```

  - Response: `201 Created`, body `MenuItemRead`

- `GET /restaurants/{id}/menu_items`
  - List menu item milik restaurant tertentu, dengan paginasi dan filter
  - Query params:
    - `category` (optional, exact match string)
    - `search` (optional, substring match pada `name`)
    - `page` (default 1)
    - `page_size` (default 10, max 100)
  - Response: `PaginatedMenuItems`

- `PUT /menu_items/{id}`
  - Update menu item (semua field optional)
  - Body: `MenuItemUpdate`

- `DELETE /menu_items/{id}`
  - Delete menu item
  - Response: `204 No Content`

## Validasi & Error Handling

- Field required (misalnya `name`, `address`, `price`) divalidasi oleh Pydantic.
- Contoh error:
  - `422 Unprocessable Entity` jika input tidak valid (misalnya field hilang atau tipe salah).
  - `404 Not Found` jika resource tidak ada (restaurant/menu item).
  - `401 Unauthorized` jika API key salah atau tidak dikirim.

## Menjalankan Test

1. Pastikan dependency sudah terinstal:

   ```bash
   pip install -r requirements.txt
   ```

2. Jalankan test dengan:

   ```bash
   pytest
   ```

Test akan menggunakan SQLite lokal (`test.db`) sehingga tidak bergantung pada MySQL.
