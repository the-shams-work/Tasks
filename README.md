# How to run? 

All you need is docker, as it avoid "it runs on my machine" type problems.
Clone the repository and run the following commands.

```bash
docker build -t tasks-app:py3.13  .
```

```bash
docker run --rm -p 8000:8000 --name tasks-app tasks-app:py3.13
```

We are not simulating anything. It's basically a complete miniature project.

If you don't want to use docker, you can run it locally as well. Just make sure you have Python 3.13 installed.

```bash
pip install -r requirements.txt
```

```bash
python3 main.py
```

It is recommended to use a virtual environment.

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

## Tech Stack

- Python (FastAPI) for backend support
- HTML, Tailwind CSS, Axios JS for Frontend

## Technologies

- JWT for authentication and interaction with API
- Internal Caching for quick lookup
- SQLite for database
- AWS (EC2) + Docker for deployment.

## Working & API Documentation

The Idea is simple. 
1. Frontend makes API call (Backend)
2. API returns the data to the Frontend

Yet. There are 6 API endpoints. 2 for authentication and 4 for task.

### Authentication Endpoints

- `POST /api/v1/auth/login`
	- Body: `{"email": ..., "password": ...}`
	- Returns: 
        - `200 OK` with `{"success": True, "token_type": "bearer"}`
        - `200 OK` with `{"success": False, "message": "Invalid email or password"}`

- `POST /api/v1/auth/register`
    - Body: `{"email": ..., "password": ...}`
    - Returns:
        - `201 Created` with `{"success": True, "message": "User registered successfully"}`
        - `400 Bad Request` with `{"success": False, "message": "Email already exists"}`

### Task Endpoints

- `GET /api/v1/tasks/`
    - Headers: `Authorization: Bearer <token>`
    - Query Params: `status` (optional, values: `pending`, `completed`)
    - Returns:
        - `200 OK` with `[{"id": ..., "title": ..., "description": ..., "status": ...}, ...]`
        - `401 Unauthorized` with `{"detail": "Invalid authentication credentials"}`

- `POST /api/v1/tasks/`
    - Headers: `Authorization: Bearer <token>`
    - Body: `{"title": ..., "description": ...}`
    - Returns:
        - `201 Created` with `{"success": True}`
        - `401 Unauthorized` with `{"detail": "Invalid authentication credentials"}`

- `PUT /api/v1/tasks/{id}`
    - Headers: `Authorization: Bearer <token>`
    - Body: `{"title": ..., "description": ..., "status": ...}`
    - Path: `id` (task ID, integer)
    - Returns:
        - `200 OK` with `{"success": True}`
        - `401 Unauthorized` with `{"detail": "Invalid authentication credentials"}`

        > Note: If the task with the given ID does not exist, it will simply ignore the request.

- `DELETE /api/v1/tasks/{id}`
    - Headers: `Authorization: Bearer <token>`
    - Path: `id` (task ID, integer)
    - Returns:
        - `200 OK` with `{"success": True}`
        - `401 Unauthorized` with `{"detail": "Invalid authentication credentials"}`

        > Note: If the task with the given ID does not exist, it will simply ignore the request.

> You can also use Swagger UI at `http://localhost:8000/docs` for testing the API endpoints.

## Note

This is a simple project made for the purpose of the demonstration of skills. It is not meant for production use.

## Known Issues

Passwords are stored in plain text in the database. Do not use real passwords.
JWT secret key is hardcoded. Do not use this in production.
JWT stored in `localStorage`, which is vulnerable to XSS attacks.
CORS is not configured properly.

## Author

Made with ❤️ by Shams
