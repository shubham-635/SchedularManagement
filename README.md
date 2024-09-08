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

## Project Structure

