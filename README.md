# Project: User-Post-Vote API

## Overview
User-Post-Vote API is a backend service built using FastAPI that enables user management, post creation, and voting functionality. This system is designed to serve as the backbone for applications that require community interactions, such as forums, social platforms, or voting systems.

## Features
- **User Management**: Register and manage users with secure authentication.
- **Post Management**: Create, read, update, and delete posts.
- **Voting System**: Allow users to cast votes on posts.

## Technologies Used
- **FastAPI**: Framework for building APIs.
- **PostgreSQL**: Relational database for data storage.
- **Alembic**: Data Migration tool for SQLAlchemy
- **SQLAlchemy**: ORM for database interaction.
- **Pydantic**: Data validation and settings management.
- **Poetry**: Dependency management and project packaging.

## Setup
### Prerequisites
- Python 3.10+
- PostgreSQL
- Poetry

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/detayotella/user-post-vote-api.git
   cd user-post-vote-api
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Create a `.env` file:
   ```env
   DB_HOST=<database-host>
   DB_NAME=<database-name>
   DB_USER=<database-user>
   DB_PORT=<database-port>
   DB_PASSWORD=<database-password>
   SECRET_KEY=<your-secret-key>
   ALGORITHM=<algorithm>
   ACCESS_TOKEN_EXPIRE_MINUTES=<expiration-time>
   ```

4. Run database migrations (if applicable).

5. Start the development server:
   ```bash
   fastapi dev app/main.py
   ```

## Usage
Visit `http://127.0.0.1:8000/docs` for interactive API documentation and testing.

## License
This project is open-source and available under the [MIT License](LICENSE).



