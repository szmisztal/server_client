# Server-Client Application

This is a server-client application using Python and PostgreSQL, with Docker for containerization and Docker Compose for orchestration.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Features

- Client-server communication over a network
- User registration and authentication
- Sending and receiving messages
- Persistent data storage with PostgreSQL
- Containerization with Docker
- Orchestration with Docker Compose

## Installation

### Prerequisites
- Docker
- Docker Compose

### Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/szmisztal/server_client.git
    cd server_client
    ```

2. Build and run the Docker containers:
    ```sh
    docker-compose up --build
    ```

   This command will build the Docker images, start the services defined in `docker-compose.yml`, and set up the environment.

## Usage

The server will automatically start when the Docker container is run. It listens on port `65432`.

### Running the Client

You can interact with the client by running the `client.py` script. The client can send commands to the server and receive responses.

```sh
python client.py
```

### Available Commands

- register - Register a new user
- login - Log in with an existing user
- change data - Change user data
- send message - Send a message to another user
- delete - Delete user account
- help - List available commands
- stop - Shut down the server

## Configuration

### Environment Variables

The following environment variables are used in the docker-compose.yml:

- DATABASE_HOST: The hostname for the PostgreSQL database (default: db).
- DATABASE_PORT: The port for the PostgreSQL database (default: 5432).

### Docker Compose Services

#### app

- Builds from the current directory.
- Ports: Maps 65432 on the host to 65432 in the container.
- Depends on: db service.
- Environment Variables: DATABASE_HOST, DATABASE_PORT.

#### db

- Image: postgres:13.
- Environment Variables: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD.
- Volumes: Mounts pgdata volume for data persistence.
