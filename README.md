# Server-Client Communication Application

This is an example of a simple server-client communication application written in Python. The application allows users to register, log in, send messages, view messages, change user data, and many other functionalities.

## Requirements

1. **Python 3.x**
2. **sqlite3** library (for SQLite database handling)

## How to Use

### Server Setup
- Run the `server.py` file to start the server.
- The server will listen for incoming connections on the specified host and port.

### Client Setup
- Run the `client.py` file to start the client application.
- You will be prompted to enter commands to interact with the server.

## Functionality
- **Register**: Register a new user with a username and password.
- **Login**: Log in to the application with your registered username and password.
- **Change Data**: Change your user data, including username and password.
- **Send Message**: Send a message to another user by specifying the recipient and message content.
- **Mailbox**: Read new messages received in your mailbox.
- **Archives**: View archived messages.
- **Logout**: Log out of the application.
- **Delete**: Delete your user data from the database.
- **Help**: Get a list of available commands.

## Database
The application uses a SQLite database to store user information and messages. The database tables are created automatically when you run the server for the first time.
