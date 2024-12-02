import socket
import threading
import time

host = "localhost"
port = 12345

cli_datas = []
ready_players = set()
player_statuses = {}
shooting_datas = []
scores = {}
usernames = {}  # Dictionary to store usernames
game_started = False  # Flag to track if the game has started
# Append zero because we look if id != 0
cli_datas.append(0)
cli_data_next_count = 1

# Track which clients have received the shooting data
clients_acknowledged = set()

def re_id(spl, cli_data_next_count):
    spl[-1] = str(cli_data_next_count)
    ret_str = "pos:"  # Ensure the prefix "pos" is included
    for i in spl[1:]:  # Skip the first element which is "pos"
        ret_str += i + ":"
    ret_str = ret_str[:-1]
    return ret_str

def re_message(cli_datas, shooting_datas):
    mesaj = ""
    for i in cli_datas:
        mesaj += str(i) + ";"
    for i in shooting_datas:
        mesaj += str(i) + ";"
    mesaj = mesaj[:-1]
    return mesaj

def reset_game_variables():
    time.sleep(3)
    global cli_datas, ready_players, player_statuses, shooting_datas, scores, game_started, cli_data_next_count, clients_acknowledged, usernames
    # Reiniciar todas las variables del juego
    cli_datas = [0]  # Reiniciar lista con el valor inicial
    ready_players.clear()  # Vaciar el conjunto de jugadores listos
    player_statuses.clear()  # Limpiar el estado de los jugadores
    shooting_datas.clear()  # Limpiar los datos de disparos
    scores.clear()  # Reiniciar los puntajes
    usernames.clear()  # Reiniciar los nombres de usuario
    game_started = False  # Marcar que el juego no ha iniciado
    cli_data_next_count = 1  # Reiniciar el contador de ID
    clients_acknowledged.clear()  # Vaciar los clientes que reconocieron los datos
    
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket created")

    s.bind((host, port))
    print("socket connecting this port: {} ".format(port))

    s.listen(5)
    print("socket listening")
except socket.error as msg:
    print("err :", msg)

while True:
    c, addr = s.accept()

    userdata = c.recv(1024).decode('utf-8')
    spl = userdata.split(":")

    if spl[0] == "join":
        mesaj = 'id:' + str(cli_data_next_count)
        player_statuses[spl[1]] = "not_ready"
        usernames[cli_data_next_count] = spl[1]  # Store the username with the assigned ID
        cli_data_next_count += 1
        c.send(mesaj.encode('utf-8'))
        print(f"Assigned ID {cli_data_next_count - 1} to player {spl[1]}")
    elif spl[0] == "ready_check":
        all_ready = len(ready_players) > 1  # Check if more than one player is ready
        c.send("all_ready".encode('utf-8') if all_ready else "not_ready".encode('utf-8'))
    elif spl[0] == "ready":
        ready_players.add(int(spl[1]))
        player_statuses[spl[1]] = "ready"
        print(f"Player {spl[1]} is ready")
    elif spl[0] == "status_check":
        status_message = ";".join([f"{name}:{status}" for name, status in player_statuses.items()])
        c.send(status_message.encode('utf-8'))
    elif spl[0] == "pos":
        if len(spl) > 1 and spl[-1].isdigit():
            index = int(spl[-1])
            # Ensure the cli_datas list is large enough
            while len(cli_datas) <= index:
                cli_datas.append("")
            cli_datas[index] = ":".join(spl)
        c.send(re_message(cli_datas, shooting_datas).encode('utf-8'))
        clients_acknowledged.add(addr)
        if len(clients_acknowledged) == len(player_statuses):
            shooting_datas.clear()
            clients_acknowledged.clear()
    elif spl[0] == "shoot":
        print(f"Shooting coordinates received: {spl[1:]}")
        shooting_datas.append(userdata)
        c.send(re_message(cli_datas, shooting_datas).encode('utf-8'))
    elif spl[0] == "start_game":
        print("Start game signal received")
        game_started = True  # Set the game started flag
    elif spl[0] == "check_start":
        if game_started:
            c.send("start_game".encode('utf-8'))
        else:
            c.send("not_ready".encode('utf-8'))
    elif spl[0] == "hit":
        shooter_id = int(spl[1])
        print(f"Player {shooter_id} hit another player")
        # Incrementa el puntaje del jugador que disparó
        if shooter_id not in scores:
            scores[shooter_id] = 0
        scores[shooter_id] += 1
        c.send((f"score_update:{shooter_id}:{scores[shooter_id]}").encode('utf-8'))
    elif spl[0] == "end_game":
        # Convert scores dictionary to a string
        scores_str = "end_game:" + ";".join([f"{usernames[player]},{score}" for player, score in scores.items()])
        
        # Send the scores string to the client
        c.send(scores_str.encode('utf-8'))  # Informar al cliente que el juego terminó
        
        # Start a thread to reset the game variables after 1 second
        reset_thread = threading.Thread(target=reset_game_variables)
        reset_thread.start()

    c.close()