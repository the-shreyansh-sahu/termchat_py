## How to Run

1.  Ensure you have the dependencies installed:
    ```powershell
    pip install textual mysql-connector-python
    ```
2.  Run the client:
    ```powershell
    python client.py
    ```

## Troubleshooting

If you encounter issues installing `textual`, try upgrading pip:
```powershell
python -m pip install --upgrade pip
python -m pip install textual
```

## Features

### Login Screen
- Enter your **Username** and **Password**.
- Click **Login** to sign in.
- Click **Register** to create a new account.
- Status messages will appear at the bottom of the form.

### Receiver Selection
- After logging in, type the username of the person you want to chat with.
- Click **Start Chat**.

### Chat Screen
- **Real-time Messaging**: Messages are polled automatically every second.
- **History**: Previous messages are loaded when you join.
- **Commands**: Type `/back` to return to the receiver selection screen.
- **Exit**: Press `Ctrl+C` to quit the application entirely (standard TUI behavior).

## Verify Functionality

Please try the following:
1.  Run the app.
2.  Register a new user (e.g., `testuser`).
3.  Login with that user.
4.  Start a chat with `shreyanshsahu` (or another existing user).
5.  Send a message.
6.  Launch a second instance of the client in another terminal, login as the other user, and verify the message appears.
