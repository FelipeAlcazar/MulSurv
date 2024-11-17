import socket
import threading
import json

class Client:
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.game_state = {}
        self.connected = True

    def receive_messages(self):
        while self.connected:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    data = json.loads(message)
                    if "client_id" in data:
                        self.client_id = data["client_id"]
                    else:
                        self.game_state = data
            except Exception as e:
                print(f"An error occurred: {e}")
                self.connected = False
                self.client.close()
                break

    def send_message(self, data):
        if self.connected:
            try:
                message = json.dumps(data)
                self.client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"An error occurred while sending message: {e}")
                self.connected = False
                self.client.close()

    def run(self):
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()