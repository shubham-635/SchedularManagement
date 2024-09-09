# Scheduler Microservice

This project is a FastAPI-based microservice for scheduling and managing jobs. The service includes API endpoints for creating, listing, and retrieving job details, with jobs stored in a MongoDB database. The service also includes JWT-based authentication and Redis caching for improved performance.

## Features

1. **Job Scheduling**: 
   - The service allows scheduling customized jobs with flexible configuration.
   - Example: Schedule a job to be executed at regular intervals, such as every Monday.

2. **API Endpoints**:
   - `GET /jobs`: List all available jobs, providing a comprehensive overview of the scheduled tasks.
   - `GET /jobs/{id}`: Retrieve detailed information about a specific job by ID, including scheduling details.
   - `POST /jobs`: Create a new job. The API validates input data and adds the job to the scheduling table.

3. **Database Integration**:
   - The service uses MongoDB to store job-related information.
   - Fields in the database include `name`, `interval`, `next_run`, and other relevant details.

4. **JWT-Based Authentication**:
   - The service includes a middleware that requires JWT authentication for accessing the endpoints.
   - Tokens are valid for 1 hour and are used to verify users against a `users` collection in MongoDB.

5. **Redis Caching**:
   - Redis is used for caching frequently accessed data, such as job listings, to improve performance.

6. **Scalability**:
   - The application is designed to scale, capable of handling increased traffic and complexity.
   - The service is optimized to handle ~10,000 users, ~1,000 services, and ~6,000 API requests per minute.

7. **Job Execution Scheduler**:
   - The service includes a background scheduler that regularly fetches jobs from the database and executes them based on their schedule.


### Explanation

- **app/main.py**: The main entry point of the FastAPI application where the app is initialized and all routers are included.

- **app/Utils/config.py**: Handles configuration settings, including environment variables and settings for database and authentication.

- **app/Utils/authentication.py**: Contains the logic for user authentication using JWT tokens and OAuth2.

- **app/Utils/database.py**: Manages the MongoDB connection using Motor (an async MongoDB driver). It handles connection pooling to support high concurrency.

- **app/v1/jobs.py**: Defines the API endpoints related to job scheduling, creation, and retrieval.

- **app//Utils/scheduler.py**: Contains the logic to handle the scheduling and execution of jobs. This might include fetching jobs from the database that need to be executed at regular intervals.

- **Dockerfile & docker-compose.yml**: Used for containerizing the application and managing multi-container Docker environments.


## Environment Variables (.env file)

The `.env` file is used to store environment-specific variables that configure the application. These variables are loaded into the application through the `config.py` file.

Create a `.env` file in the project root with the following content:


`MONGODB_URI`
`MONGODB_NAME`
`SECRET_KEY`
`ALGORITHM`
`ACCESS_TOKEN_EXPIRE_MINUTES`

## Prerequisites

- Python 3.11
- MongoDB
- Docker (for containerization)

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shubham-635/SchedularManagement.git
   cd SchedularManagement


2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the project root with the environment variables as described above.

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Run with Docker**:
   If you're using Docker, you can build and run the service using Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Usage

- Access the API at `http://localhost:8000`.
- Use the `/token` endpoint to obtain a JWT token for authentication.
- Schedule and manage jobs using the provided endpoints.
- Use a tool like Postman or cURL to interact with the API.

## Scaling the Application

To scale this application:
- **Database**: Use a sharded cluster for MongoDB to handle large datasets and high throughput.
- **API**: Deploy multiple instances of the FastAPI service behind a load balancer.
- **Caching**: Use Redis to cache frequently accessed data and reduce the load on MongoDB.
- **Queue System**: Integrate a message broker like RabbitMQ or Kafka to handle job processing asynchronously.

## Future Enhancements

### Redis Queuing for Job Execution

While the current implementation includes basic job scheduling logic, a future enhancement could involve integrating Redis with a queuing mechanism such as **Redis Queue (RQ)** or **Celery**. This would allow the actual execution of scheduled jobs in a distributed and scalable manner, ensuring that jobs are processed reliably, even under high load.

---
