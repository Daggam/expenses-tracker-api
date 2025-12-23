# Expenses Tracker API
## Overview

Expenses Tracker is a robust REST API built with **FastAPI**, **SQLAlchemy**, and **Alembic**. It provides a secure and way to manage personal expenses with categorization and user management.

### Features

- **Authentication & Authorization**: Secure user access using JWT sessions.
- **Expense Management**: Users can create, read, update, and delete (CRUD) their own expenses.
- **Categorization**: Organize expenses by categories.
- **Database Management**: Automated migrations using Alembic.
- **Testing**: Comprehensive test suite using Pytest.

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [uv](https://docs.astral.sh/uv/)
- [Docker](https://docs.docker.com/)

## Getting Started

First, clone the repository to your local machine:

```Bash
git clone https://github.com/Daggam/expenses-tracker-api.git
cd expenses-tracker-api
```

You can build and run the project in two ways: [Manually (Local)](#option-1-manual-installation) or using [Docker](#option-2-docker-recommended).

### Option 1: Manual Installation

This project uses `uv` for package management.

1. **System Requirements (psycopg2)**

Since `psycopg2` is a wrapper around libpq (implemented in C), you must install specific system dependencies before installing the Python packages.
- **Linux (Debian/Ubuntu)**:
    ```Bash
    sudo apt-get update && apt-get install -y libpq-dev gcc
    ```
- **Windows**: If you encounter issues installing the standard `psycopg2`, you should use the binary version.

    - Open pyproject.toml.

    - Replace `psycopg2` with `psycopg2-binary`.

2. **Install Dependencies**

Run the following command using uv to sync dependencies:

```Bash
uv sync
```

3. **Environment Configuration**

    1. Create a `.env` file based on the example provided:

    ```Bash
    cp .env.example .env
    ```

    2. Update the `DATABASE_URL` in the `.env` file with your local PostgreSQL connection string.

    3. Generate a secure `SECRET_KEY`. You can generate one using openssl:

    ```Bash
    openssl rand --hex 32
    ```

4. **Run the Server**

Once configured, start the API:
```Bash
uv run uvicorn src.main:app
```

---
### Option 2: Docker (Recommended)

For easier deployment, the project includes a `Dockerfile` and `docker-compose.yaml`.

1. **Environment Configuration**

    Create a production environment file:
    ```Bash
    cp .env.example .env.prod
    ```
2. **Important**: Modify the `DATABASE_URL` in `.env.prod`.

    - Since the database is running inside a Docker container, you must use the service name (defined in docker-compose.yaml) as the hostname instead of localhost.

    - Example: `postgresql://user:password@db_service_name:5432/db_name`

2. **Build and Run**

    Execute the following command to build the image and start the containers:
    ```Bash
    docker compose up --build
    ```

The REST API will now be running and accessible.

## Testing

To run the tests, execute:
```Bash
uv run pytest
```