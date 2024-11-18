import socket

host = "localhost"
port = 12345

cli_datas = []
#append zero because we look if id != 0
cli_datas.append(0)
cli_data_next_count = 1

def re_id(spl,cli_data_next_count):
    spl[-1] = str(cli_data_next_count)
    ret_str = ""
    for i in spl:
        ret_str += i+":"
    ret_str = ret_str[:-1]
    return ret_str

def re_message(cli_datas):
    mesaj = ""
    for i in cli_datas:
        mesaj += str(i)+";"
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
    print("err :",msg)


while True: 
    c, addr = s.accept()      
    print('connection :', addr)

    userdata = c.recv(1024).decode('utf-8')
    spl = userdata.split(":")

    if(spl[-1] == "0"):
        mesaj = 'id:'+str(cli_data_next_count)
        
        userdata = re_id(spl,cli_data_next_count)

        cli_datas.append(userdata)
        cli_data_next_count += 1
        c.send(mesaj.encode('utf-8')) 
    else:
        cli_datas[int(spl[-1])] = userdata
        
        c.send(re_message(cli_datas).encode('utf-8')) 
 
    print(str(cli_datas))

    c.close()

