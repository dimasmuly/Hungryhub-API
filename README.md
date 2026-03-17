# HungryHub Take-Home: Restaurant Menu Management API

REST API untuk mengelola restoran dan menu item, dibangun dengan FastAPI, SQLAlchemy, dan MySQL.

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy 2.x
- MySQL 8
- PyMySQL (DB driver)
- Docker & Docker Compose
- Pytest

## Fitur Utama

- CRUD Restaurant
- CRUD Menu Item (per restaurant)
- Relasi one-to-many antara Restaurant dan Menu Item
- Validasi input dengan error message yang jelas
- Status code HTTP yang sesuai (200, 201, 400, 404, 401, 204)
- Seed data awal:
  - 2 restoran
  - Masing-masing minimal 5 menu item
- Autentikasi sederhana dengan API key (header `X-API-Key`)
- Paginasi untuk list endpoint
- Filter dan search menu item:
  - Filter by `category`
  - Search by `name` (parameter `search`)

## Struktur Proyek

- `app/config.py` – konfigurasi aplikasi (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, API_KEY)
- `app/database.py` – koneksi database dan session
- `app/models.py` – model SQLAlchemy (Restaurant, MenuItem)
- `app/schemas.py` – Pydantic schema untuk request/response
- `app/main.py` – definisi FastAPI app dan semua endpoint
- `tests/` – basic integration tests dengan Pytest
- `Dockerfile`, `docker-compose.yml` – setup Docker

## Menjalankan Secara Lokal (Tanpa Docker)

1. Buat dan aktifkan virtualenv (opsional tapi direkomendasikan).

2. Instal dependency:

   ```bash
   pip install -r requirements.txt
   ```

3. Pastikan MySQL berjalan dan sudah ada database:

   - Nama database: `takehometest-hungryhub`
   - Contoh SQL:

     ```sql
     CREATE DATABASE `takehometest-hungryhub` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
     CREATE USER 'hungryhub'@'%' IDENTIFIED BY 'hungryhub';
     GRANT ALL PRIVILEGES ON `takehometest-hungryhub`.* TO 'hungryhub'@'%';
     FLUSH PRIVILEGES;
     ```

4. Buat file `.env` di root (wajib untuk konfigurasi MySQL dan API key):

   ```env
   DB_USER=hungryhub
   DB_PASSWORD=hungryhub
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=takehometest-hungryhub
   API_KEY=supersecretapikey
   ```

5. Jalankan aplikasi:

   ```bash
   uvicorn app.main:app --reload
   ```

6. API akan tersedia di:

   - `http://localhost:8000`
   - Dokumentasi Swagger otomatis: `http://localhost:8000/docs`

## Menjalankan dengan Docker

Pastikan Docker dan Docker Compose terinstal.

1. Jalankan:

   ```bash
   docker-compose up --build
   ```

2. Service:

   - API: `http://localhost:8000`
   - MySQL: `localhost:3306`

3. Variable penting di `docker-compose.yml`:

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

Pada event startup, aplikasi akan:

- Membuat tabel jika belum ada
- Mengecek jumlah restoran
- Jika 0, otomatis insert:
  - Restoran `Bangkok Spice` dengan 5 menu item
  - Restoran `Chiang Mai Garden` dengan 5 menu item

Seed terdapat di `app/main.py` dalam fungsi `init_db_and_seed`.

## Autentikasi

Semua endpoint membutuhkan API key sederhana via header:

- Header: `X-API-Key: supersecretapikey`

Jika header tidak ada atau value salah, API akan mengembalikan:

- `401 Unauthorized` dengan pesan `Invalid API key`

## Endpoint API

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
