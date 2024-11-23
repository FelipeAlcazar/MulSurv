import socket

host = "localhost"
port = 12345

cli_datas = []
shooting_datas = []
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

    if spl[0] == "pos":
        if spl[-1] == "0":
            mesaj = 'id:' + str(cli_data_next_count)
            userdata = re_id(spl, cli_data_next_count)
            cli_datas.append(userdata)
            cli_data_next_count += 1
            c.send(mesaj.encode('utf-8'))
        else:
            if len(spl) > 1 and spl[-1].isdigit():
                cli_datas[int(spl[-1])] = ":".join(spl)
            print("position data received:", str(cli_datas))
            c.send(re_message(cli_datas, shooting_datas).encode('utf-8'))
            # Clear shooting data after sending it
            shooting_datas.clear()
    elif spl[0] == "shoot":
        print(f"Shooting coordinates received: {spl[1:]}")
        # Add shooting coordinates to shooting_datas
        shooting_datas.append(userdata)
        c.send(re_message(cli_datas, shooting_datas).encode('utf-8'))

    print("cli_datas:", str(cli_datas))
    print("shooting_datas:", str(shooting_datas))
    c.close()