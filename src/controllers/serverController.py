import socket
import threading
import json

class Server:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.client_connected = threading.Event()
        self.game_state = {
            "players": {},
            "enemies": [],
            "rocks": [],
            "trees": [],
            "game_started": False
        }

    def handle_client(self, client, client_id):
        client.send(json.dumps({"client_id": client_id}).encode('utf-8'))
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message:
                    data = json.loads(message)
                    self.update_game_state(client_id, data)
                    self.broadcast(json.dumps(self.game_state), client)
            except:
                self.clients.remove(client)
                client.close()
                break

    def broadcast(self, message, client):
        for c in self.clients:
            if c != client:
                c.send(message.encode('utf-8'))

    def update_game_state(self, client_id, data):
        if "input" in data:
            self.game_state["players"][client_id] = data["input"]
        else:
            self.game_state["players"][client_id] = data["player"]
            self.game_state["enemies"] = data["enemies"]
            self.game_state["rocks"] = data["rocks"]
            self.game_state["trees"] = data["trees"]

    def run(self):
        print("Server running...")
        while True:
            client, addr = self.server.accept()
            print(f"Connected with {addr}")
            client_id = len(self.clients)
            self.clients.append(client)
            self.client_connected.set()
            thread = threading.Thread(target=self.handle_client, args=(client, client_id))
            thread.start()
            if len(self.clients) > 1:
                self.game_state["game_started"] = True
                self.broadcast(json.dumps(self.game_state), None)