# News Aggregator

This is a Django-based news aggregator application that fetches news from an RSS feed, matches them with current trends from Google Trends, and analyzes the sentiment of the news headlines using the OpenAI API. The application uses Celery for asynchronous task processing and RabbitMQ as the message broker. The app is containerized using Docker.

## Features

- Fetches news from the tsn.ua RSS feed every minute.
- Fetches trending topics from Google Trends daily.
- Matches news headlines with trending topics.
- Analyzes sentiment of the matched news headlines using OpenAI API.
- Provides an API endpoint to view the trending news, with pagination and filtering.

## Prerequisites

- Docker
- Docker Compose
- OpenAI API Key

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
POSTGRES_DB=newsdb
POSTGRES_USER=newsuser
POSTGRES_PASSWORD=newspassword
POSTGRES_HOST=db
POSTGRES_PORT=5432

CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=rpc://

OPENAI_API_KEY=your_openai_api_key

DJANGO_SECRET_KEY=your_django_secret_key
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YuraYarmola/NewsTestTask.git
cd NewsTestTask
```

### 2. Build and run the Docker containers

```bash
docker-compose up --build
```

This command will build the Docker images and start the containers for the Django app, PostgreSQL database, RabbitMQ, Celery worker, and Celery beat scheduler.

### 3. Run database migrations

After the containers are up and running, open a new terminal and run:

```bash
docker-compose exec web python manage.py migrate
```

### 4. Access the application

- The Django app will be running at: `http://localhost:8000`
- RabbitMQ management interface will be available at: `http://localhost:15672` 

### 5. API Endpoint

The API endpoint to view the trending news is available at:

```
GET /api/trending-news/
```

You can use query parameters for pagination and filtering:
- `?page=2` for pagination.
- `?trend__name=some_trend` for filtering by trend name.
- `?ordering=sentiment` to order by sentiment.

## Docker Compose Services

- **db**: PostgreSQL database.
- **rabbitmq**: RabbitMQ message broker.
- **web**: Django application.
- **celery**: Celery worker for asynchronous tasks.
- **celery-beat**: Celery beat scheduler for periodic tasks.

## Additional Commands

### 1. To access the Django shell

```bash
docker-compose exec web python manage.py shell
```

### 2. To create a superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### 3. To collect static files

```bash
docker-compose exec web python manage.py collectstatic
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

