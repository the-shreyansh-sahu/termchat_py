from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Center
from textual.widgets import Header, Footer, Input, Button, Label, RichLog, Static
from textual.screen import Screen
from textual import work
from datetime import datetime
import db

class LoginScreen(Screen):
    CSS = """
    LoginScreen {
        align: center middle;
    }
    #login-container {
        width: 60;
        height: auto;
        border: solid green;
        padding: 1 2;
        background: $surface;
    }
    #login-label {
        width: 100%;
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    Input {
        margin: 1 0;
    }
    Button {
        margin: 1 1;
        width: 45%;
    }
    #btn-container {
        align: center middle;
        margin-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="login-container"):
            yield Label("TermChat Login", id="login-label")
            yield Input(placeholder="Username", id="username")
            yield Input(placeholder="Password", password=True, id="password")
            with Horizontal(id="btn-container"):
                yield Button("Login", id="login", variant="primary")
                yield Button("Register", id="register", variant="warning")
            yield Label("", id="status")

    @work(exclusive=True, thread=True)
    def check_login(self, username, password):
        self.query_one("#status", Label).update("Checking...")
        if db.check_user(username, password):
            self.app.user = username
            # push_screen must be called from the main thread
            self.app.call_from_thread(self.app.push_screen, ReceiverScreen())
        else:
            self.query_one("#status", Label).update("Invalid Credentials")

    @work(exclusive=True, thread=True)
    def do_register(self, username, password):
        self.query_one("#status", Label).update("Registering...")
        if db.register_user(username, password):
            self.query_one("#status", Label).update("Registered! Please Log In.")
        else:
            self.query_one("#status", Label).update("Registration Failed (Username taken?)")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        username = self.query_one("#username", Input).value
        password = self.query_one("#password", Input).value
        
        if not username or not password:
            self.query_one("#status", Label).update("Please enter both fields")
            return

        if event.button.id == "login":
            self.check_login(username, password)
        elif event.button.id == "register":
            self.do_register(username, password)


class ReceiverScreen(Screen):
    CSS = """
    ReceiverScreen {
        align: center middle;
    }
    #recv-container {
        width: 60;
        height: auto;
        border: solid blue;
        padding: 1 2;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Vertical(id="recv-container"):
            yield Label("Who do you want to chat with?")
            yield Input(placeholder="Enter username", id="receiver")
            yield Button("Start Chat", id="start", variant="success")
            yield Button("Logout", id="logout", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            receiver = self.query_one("#receiver", Input).value
            if receiver:
                self.app.push_screen(ChatScreen(receiver))
        elif event.button.id == "logout":
            self.app.pop_screen()

class ChatScreen(Screen):
    CSS = """
    ChatScreen {
        layout: vertical;
    }
    RichLog {
        height: 1fr;
        border: solid white;
        background: $background;
    }
    Input {
        dock: bottom;
    }
    #header-label {
        text-align: center;
        background: $primary;
        color: white;
        padding: 1;
    }
    """

    def __init__(self, receiver: str):
        super().__init__()
        self.receiver = receiver
        self.last_msg_id = 0

    def compose(self) -> ComposeResult:
        yield Label(f"Chatting with {self.receiver}", id="header-label")
        yield RichLog(markup=True, highlight=True)
        yield Input(placeholder="Type a message...", id="message_input")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(RichLog).write(f"[bold yellow]Connected to {self.receiver}[/]")
        self.set_interval(1.0, self.poll_messages)
        self.poll_messages()

    @work(exclusive=True, thread=True)
    def poll_messages(self):
        try:
            msgs = db.get_messages(self.app.user, self.receiver, self.last_msg_id)
            if msgs:
                self.app.call_from_thread(self.add_messages, msgs)
        except Exception as e:
            self.app.call_from_thread(self.app.notify, f"Error polling: {e}", severity="error")

    def add_messages(self, msgs):
        log = self.query_one(RichLog)
        for msg in msgs:
            # msg structure: (id, sender, receiver, message, timestamp)
            msg_id, sender, _, content, _ = msg
            
            # Debug: print to console (user won't see this in TUI easily but we can infer)
            # Actually, let's use notify for debug if it happens
            if msg_id <= self.last_msg_id:
                continue
                
            self.last_msg_id = max(self.last_msg_id, msg_id)
            
            if sender == self.app.user:
                log.write(f"[bold green]Me:[/bold green] {content}")
            else:
                log.write(f"[bold cyan]{sender}:[/] {content}")

    @work(exclusive=True, thread=True)
    def send_message(self, text):
        db.save_message(self.app.user, self.receiver, text)
        # We don't manually add it here; polling will pick it up, 
        # or we could optimistically add it. Polling is safer for consistency.
        # But for better UX, let's trigger a poll immediately after send
        self.poll_messages()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        if text:
            if text.lower() == "/back":
                self.app.pop_screen()
                return
            
            self.send_message(text)
            self.query_one("#message_input", Input).value = ""

class TermChatApp(App):
    CSS = """
    Screen {
        background: $surface-darken-1;
    }
    """
    
    user: str = None

    def on_mount(self) -> None:
        self.push_screen(LoginScreen())

if __name__ == "__main__":
    app = TermChatApp()
    app.run()
