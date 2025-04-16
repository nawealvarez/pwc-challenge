# PWC Challenge

A FastAPI-based course management system with Docker Compose deployment.

## Project Overview

This project is a course management system that allows:

- Managing teachers, students, courses, and enrollments
- RESTful API with proper versioning
- PostgreSQL database with Supabase integration
- Alembic migrations for database schema management

## Architecture

The application follows a clean architecture pattern:

- **Models**: SQLAlchemy ORM models
- **Schemas**: Pydantic models for request/response validation
- **Repositories**: Data access layer
- **Services**: Business logic layer
- **Routes**: API endpoints

## Getting Started with Docker Compose

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/pwc-challenge.git
   cd pwc-challenge
   ```

2. Create a `.env` file with your database connection string if you want to use other database, otherwise it will use the default one:

   ```
   DATABASE_URL=postgresql://username:password@host:port/database
   ```

3. Start the application using Docker Compose:

   ```bash
   docker compose up -d
   ```

4. Run database migrations:

   ```bash
   docker compose exec api alembic upgrade head
   ```

5. Access the API at http://localhost:8000

### Development Workflow

1. Make changes to your code
2. The changes will be automatically reflected in the running container due to the volume mount
3. Restart the container if needed:
   ```bash
   docker compose restart api
   ```

### Running Migrations

To create a new migration:

```bash
docker compose exec api alembic revision --autogenerate -m "description of changes"
```

To apply migrations:

```bash
docker compose exec api alembic upgrade head
```

To rollback migrations:

```bash
docker compose exec api alembic downgrade -1
```

### Stopping the Application

```bash
docker compose down
```

### Running Test

```bash
docker-compose run --rm -e PYTHONPATH=/app api pytest
```

## API Documentation

Once the application is running, you can access:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Schema

For detailed information about the database schema and relationships, see [Database Diagrams](docs/diagrams.md).

## License

[MIT License](LICENSE)
