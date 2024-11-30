# FILE: src/controllers/serverController.py

import socket

host = "localhost"
port = 12345

cli_datas = []
ready_players = set()
player_statuses = {}
shooting_datas = []
game_started = False  # Flag to track if the game has started
# Append zero because we look if id != 0
cli_datas.append(0)
cli_data_next_count = 1

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
        cli_data_next_count += 1
        c.send(mesaj.encode('utf-8'))
        print(f"Assigned ID {cli_data_next_count - 1} to player {spl[1]}")
    elif spl[0] == "ready_check":
        all_ready = len(ready_players) > 1  # Check if more than one player is ready
        c.send("all_ready".encode('utf-8') if all_ready else "not_ready".encode('utf-8'))
        #print(f"Ready check: {'all_ready' if all_ready else 'not_ready'}")
    elif spl[0] == "ready":
        ready_players.add(int(spl[1]))
        player_statuses[spl[1]] = "ready"
        print(f"Player {spl[1]} is ready")
    elif spl[0] == "status_check":
        status_message = ";".join([f"{name}:{status}" for name, status in player_statuses.items()])
        c.send(status_message.encode('utf-8'))
        #print(f"Status check: {status_message}")
    elif spl[0] == "pos":
        if len(spl) > 1 and spl[-1].isdigit():
            index = int(spl[-1])
            # Ensure the cli_datas list is large enough
            while len(cli_datas) <= index:
                cli_datas.append("")
            cli_datas[index] = ":".join(spl)
        #print("position data received:", str(cli_datas))
        c.send(re_message(cli_datas, shooting_datas).encode('utf-8'))
        # Clear shooting data after sending it
        shooting_datas.clear()
    elif spl[0] == "shoot":
        print(f"Shooting coordinates received: {spl[1:]}")
        # Add shooting coordinates to shooting_datas
        shooting_datas.append(userdata)
        c.send(re_message(cli_datas, shooting_datas).encode('utf-8'))
    elif spl[0] == "start_game":
        print("Start game signal received")
        game_started = True  # Set the game started flag
    elif spl[0] == "check_start":
        # Check if the game should start
        if game_started:
            c.send("start_game".encode('utf-8'))
        else:
            c.send("not_ready".encode('utf-8'))

    #print("cli_datas:", str(cli_datas))
    #print("ready_players:", str(ready_players))
    #print("player_statuses:", str(player_statuses))
    #print("shooting_datas:", str(shooting_datas))
    c.close()