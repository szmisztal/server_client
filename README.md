# Server-Client Application

This is a server-client application using Python and PostgreSQL, with Docker for containerization and Docker Compose for orchestration.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [License](#license)

## Installation

### Prerequisites
- Docker
- Docker Compose

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
Build and run the Docker containers:

bash
Skopiuj kod
docker-compose up --build
This command will build the Docker images, start the services defined in docker-compose.yml, and set up the environment.

Usage
Running the Server
The server will automatically start when the Docker container is run. It listens on port 65432.

Interacting with the Client
You can interact with the client by running the client.py script. The client can send commands to the server and receive responses.

Configuration
Environment Variables
The following environment variables are used in the docker-compose.yml:

DATABASE_HOST: The hostname for the PostgreSQL database (default: db).
DATABASE_PORT: The port for the PostgreSQL database (default: 5432).
Docker Compose Services
app
Builds from the current directory.
Ports: Maps 65432 on the host to 65432 in the container.
Depends on: db service.
Environment Variables: DATABASE_HOST, DATABASE_PORT.
db
Image: postgres:13.
Environment Variables: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD.
Volumes: Mounts pgdata volume for data persistence.
