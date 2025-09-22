# Todos FastAPI

API sederhana untuk manajemen todo list dengan JWT authentication.

## Setup

### 1. Buat Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi
```bash
uvicorn main:app --reload
```

Aplikasi berjalan di: `http://localhost:8000`

## API Endpoints

**Login:**
```
POST /login
Body: {"username": "admin", "password": "admin"}
```

**Todos:** (butuh Authorization header)
```
GET /todos
POST /todos
PUT /todos/{id}
DELETE /todos/{id}
```

## Testing
- Postman collection: `Todos FastAPI.postman_collection.json`
