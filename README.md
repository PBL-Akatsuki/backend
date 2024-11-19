# Backend: FastAPI + PostgreSQL

## Prerequisites

- **Python 3.12 or newer** (required for development)

  - Install it from the [Python official website](https://www.python.org/downloads/).
  - Verify installation:
    ```bash
    python --version
    ```
    Ensure the version is `3.12.x`.

- **Docker & Docker Compose** (required for database and production setup)
  - Install Docker from the [Docker official website](https://www.docker.com/).
  - Install Docker Compose by following the instructions on the [Docker Compose installation page](https://docs.docker.com/compose/install/).
  - Verify installation:
    ```bash
    docker --version
    docker-compose --version
    ```

---

## How to set up and run the application:

### Development Setup (With Hot Reload)

1. **Clone the repository**:

   ```bash
   git clone https://github.com/PBL-Akatsuki/backend.git
   ```

2. **Navigate to the project root directory**:

   ```bash
   cd backend
   ```

3. **Start PostgreSQL and pgAdmin (via Docker Compose)**:

   ```bash
   docker-compose up -d postgres pgadmin
   ```

   - This starts the database and pgAdmin services. You can access pgAdmin at [http://localhost:8080](http://localhost:8080).
   - Use these credentials to log in:
     - **Email**: `admin@example.com`
     - **Password**: `admin`

4. **Set up a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install dependencies**:

   ```bash
   pip install -r app/requirements.txt
   ```

6. **Run the FastAPI application with hot reload**:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   - The API will be available at [http://localhost:8000](http://localhost:8000).
   - The Swagger UI (API documentation) is available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

### Production Setup (Dockerized Deployment)

1. **Clone the repository**:

   ```bash
   git clone https://github.com/PBL-Akatsuki/backend.git
   ```

2. **Navigate to the project root directory**:

   ```bash
   cd backend
   ```

3. **Build the Docker image**:

   ```bash
   docker-compose up --build -d
   ```

4. **Access the FastAPI application**:

   - The API will be available at [http://localhost:8000](http://localhost:8000).
   - The Swagger UI (API documentation) is available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## How it works:

### Development:

- During development:
  - **Hot Reload**: FastAPI runs with `uvicorn --reload` for automatic code reload on changes.
  - **Database & pgAdmin**: PostgreSQL and pgAdmin run via Docker Compose to avoid local installation.

### Production:

- For production:
  - **Dockerized Deployment**: FastAPI, PostgreSQL, and pgAdmin run inside containers.
