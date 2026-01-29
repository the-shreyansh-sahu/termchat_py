# TermChat

A simple terminal-based chat application using Python and MySQL.

## Prerequisites

- Python 3.x
- MySQL Database (Remote or Local)

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Database Configuration:**
    - The database connection details are currently hardcoded in `db.py`.
    - Ensure your MySQL server is running and accessible.
    - The application expects a database named `chatapp` (or as configured in `db.py`) with `users` and `messages` tables.

## Usage

1.  **Run the Client:**
    ```bash
    python client.py
    ```

2.  **Interact:**
    - **Register:** Choose option `1` to create a new account.
    - **Login:** Choose option `2` to log in.
    - **Chat:** Enter the username of the person you want to chat with.
    - **Back:** Type `/back` during a chat to return to the user selection menu.
    - **Exit:** Type `exit` in the user selection menu to close the application.
