import threading
import time
from db import register_user, check_user, save_message, get_messages

username = None
receiver = None
last_msg_id = 0

def receive_messages(stop_event, initial_load_done_event):
    global last_msg_id, username, receiver
    
    try:
        # Initial fetch for history
        msgs = get_messages(username, receiver, last_msg_id)
        for msg in msgs:
            print(f"{msg[1]}: {msg[3]}")
            last_msg_id = msg[0]
    finally:
        initial_load_done_event.set()
    
    while not stop_event.wait(1):
        msgs = get_messages(username, receiver, last_msg_id)
        
        other_msgs = [m for m in msgs if m[1] != username]
        for msg in msgs:
            last_msg_id = msg[0]

        if other_msgs:
            print(f"\r{' ' * 80}\r", end='')
            for msg in other_msgs:
                print(f"{msg[1]}: {msg[3]}")
            print(f"{username}: ", end="", flush=True)

def login():
    global username
    print("1. Register\n2. Login")
    choice = input("Choose: ")
    uname = input("Username: ")
    pwd = input("Password: ")
    if choice == "1":
        if register_user(uname, pwd):
            print("Registered! Now login.")
        else:
            print("Username exists.")
            return login()
    if check_user(uname, pwd):
        username = uname
        print(f"Welcome, {username}")
    else:
        print("Invalid credentials")
        return login()

def main():
    global receiver, last_msg_id, username
    login()

    while True:
        receiver = input("Enter the username you want to chat with (or 'exit' to quit): ")
        if receiver.strip().lower() == 'exit':
            break
        
        print(f"\n--- Chat with {receiver} ---")
        print("Type '/back' to return to user selection.\n")

        last_msg_id = 0
        stop_event = threading.Event()
        initial_load_done_event = threading.Event()

        thread = threading.Thread(target=receive_messages, args=(stop_event, initial_load_done_event), daemon=True)
        thread.start()
        
        initial_load_done_event.wait()

        while True:
            msg = input(f"{username}: ")
            if msg.strip().lower() == '/back':
                stop_event.set()
                time.sleep(0.1) # Allow thread to process stop_event
                break

            if not save_message(username, receiver, msg):
                print("Error: Message not sent.")
        
        print(f"\n--- End of chat with {receiver} ---\n")

if __name__ == "__main__":
    main()
