import socket
import threading
import json
from mouse.makcu import makcu_controller

class InputServer:
    def __init__(self, host="0.0.0.0", port=5005):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = False
        self.thread = None

    def start(self):
        try:
            self.sock.bind((self.host, self.port))
            self.running = True
            self.thread = threading.Thread(target=self._listen, daemon=True)
            self.thread.start()
            print(f"[InputServer] Listening on {self.host}:{self.port}")
        except Exception as e:
            print(f"[InputServer] Failed to start: {e}")

    def _listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = data.decode('utf-8')
                
                # Expected format: "KEY:STATE" (e.g., "F1:DOWN", "A:UP")
                if ":" in message:
                    key, state = message.split(":", 1)
                    is_pressed = (state == "DOWN")
                    makcu_controller.update_key_state(key, is_pressed)
                    
            except Exception as e:
                print(f"[InputServer] Error receiving data: {e}")

    def stop(self):
        self.running = False
        if self.sock:
            self.sock.close()
