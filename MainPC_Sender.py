import socket
import keyboard
import time
import json

# ==============================================================================
# CONFIGURATION
# ==============================================================================
LAPTOP_IP = "192.168.1.X"  # <--- REPLACE THIS WITH YOUR LAPTOP'S LOCAL IP ADDRESS
PORT = 5005
# ==============================================================================

print(f"Starting Key Sender to {LAPTOP_IP}:{PORT}...")
print("Press CTRL+C to stop.")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Keys we want to track (Common toggles)
# You can add more keys here if you need them.
WATCHED_KEYS = [
    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
    'insert', 'delete', 'home', 'end', 'page up', 'page down',
    'num 0', 'num 1', 'num 2', 'num 3', 'num 4', 'num 5', 'num 6', 'num 7', 'num 8', 'num 9',
    'caps lock', 'tab', 'v', 'b', 'n', 'm'
]

key_states = {k: False for k in WATCHED_KEYS}

def send_update(key, state):
    try:
        msg = f"{key}:{state}"
        sock.sendto(msg.encode('utf-8'), (LAPTOP_IP, PORT))
        # print(f"Sent: {msg}") # Uncomment for debug
    except Exception as e:
        print(f"Error sending: {e}")

def check_keys():
    while True:
        for key in WATCHED_KEYS:
            try:
                is_pressed = keyboard.is_pressed(key)
                if is_pressed != key_states[key]:
                    key_states[key] = is_pressed
                    state_str = "DOWN" if is_pressed else "UP"
                    
                    # Normalize key names for the laptop receiver if needed
                    # For now we send raw keyboard module names
                    send_update(key, state_str)
            except Exception:
                pass
        time.sleep(0.01) # Poll rate

if __name__ == "__main__":
    try:
        check_keys()
    except KeyboardInterrupt:
        print("Stopping...")
