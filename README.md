# The Void

## Overview
The Void is a full-stack web application built with FastAPI that allows users to "yell" messages into the void and "peek" to retrieve a random message from the abyss. The project is designed as a demonstration of modern backend development practices with Python, API creation, database integration, testing, and containerized deployment using Docker. Continuous integration is set up via GitHub Actions, and the project is structured for eventual deployment on AWS with PostgreSQL.

## Table of Contents
- [Overview](#overview)
- [Table of Contents](#table-of-contents)
- [Getting Started](#getting-started)
  - [Installation Prerequisites](#installation-prerequisites)
  - [How to Run Locally](#how-to-run-locally)
- [Technologies Used](#technologies-used)

## Getting Started

### Installation Prerequisites
Before you begin, ensure you have the following installed on your local machine:
- **Python 3.8 or higher** – Required for backend services.
- **Docker & Docker Compose** – For containerizing the application.
- **Git** – For version control and cloning the repository.
- (Optional) **PostgreSQL Client** – For testing database connectivity (using `psql`), if needed.
  
The project dependencies are listed in the `requirements.txt` file and include:
- FastAPI
- SQLAlchemy
- Uvicorn
- psycopg2-binary
- python-dotenv
- pytest

### How to Run Locally

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/KenB7891/the-void.git
   cd the-void
   ```

2. **Set Up Environment Variables:**
    - Create a ```.env``` file in the root directory and ensure it contains the following parameters
    ```dotenv
    DB_HOST=
    DB_PORT=
    DB_NAME=
    DB_USER=
    DB_PASSWORD=
    ```
    ### Note: During local development, if you’re not using an RDS instance, update the variables to match your local PostgreSQL or SQLite settings.

3. **Run the Application Locally Without Docker (optional):**
    - Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
    - Ensure that your PYTHONPATH includes the project root (if needed, run):
    ```bash
    export PYTHONPATH=.
    ```
    - Start the application with Uvicorn:
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    - Visit http://localhost:8000 in your browser.

4. **Run Using Docker Compose:**
    - Build and start containers
    ```bash
    docker-compose up --build
    ```
    - Docker Compose will use your Dockerfile and .env file to build the container and start the application on port 8000.
    - Access the application at http://localhost:8000.

5. **Running Tests:**
    - To run the test suite, execute:
    ```bash
    PYTHONPATH=. pytest tests
    ```
    - This ensures that the project’s root directory is included in the PYTHONPATH so that the tests can find your application modules.

## Technologies Used
- Python 3.8+ – Programming language for backend development.
- FastAPI – High-performance web framework for building APIs.
- SQLAlchemy – ORM for database interactions.
- Uvicorn – ASGI server for running FastAPI applications.
- Docker & Docker Compose – Containerization and orchestration tools.
- GitHub Actions – For continuous integration and automated testing.
- PostgreSQL – Production-grade relational database via AWS RDS.
- pytest – Testing framework used for unit and integration tests.