import sqlite3
import socket
from _thread import *
from component import select,divView2
con = sqlite3.connect('../Hotel.db')
cur = con.cursor()


# def select(data):
#     try:
#         sel = con.execute(f'{data}').fetchall()
#         print(sel)
#         return sel
#     except error:
#         sel = f"An Error occurred : {error}"
#         print(sel)
#         return sel


host = '127.0.0.1'
port = 1233
threadCount = 0
clients={"Room Service G1":[],"Room Service G2":[],"Reception":[]}
div={"Room Service G1":[],"Room Service G2":[],"Reception":[]}
ServerSocket = socket.socket()

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    name = connection.recv(2048).decode('utf-8')
    connection.send(str.encode(f'Welcome to Server , {name}'))
    while True:
        opp = connection.recv(2048).decode('utf-8')
        connection.sendall(str.encode(f'Operation start....'))
        if opp=='info':
            # data = connection.recv(2048).decode('utf-8')
            replyG1='\n         '.join(clients["Room Service G1"])
            replyG2 = '\n       '.join(clients["Room Service G2"])
            replyR = '\n        '.join(clients["Reception"])
            connection.sendall(str.encode(f"   Room Service G1:\n       {replyG1}\n    Room Service G2 :\n       {replyG2}\n   Reception :\n       {replyR}\n"))
        elif opp=='ReDis':
            replyG1 = ' , '.join(div["Room Service G1"])
            replyG2 = ' , '.join(div["Room Service G2"])
            result=divView2(div["Room Service G1"],div["Room Service G2"])
            connection.sendall(str.encode(f"   Room Service G1 work on IDs:\n       {replyG1}\n    Room Service G2 work on IDs:\n       {replyG2} \n{result}"))
        else:
            index = connection.recv(2048).decode('utf-8')
            div[name].append(str(index))
            data = connection.recv(2048).decode('utf-8')
            clients[name].append(f'{data}')
            reply = select(data,opp)
            reply = 'Server Says: ' + str(reply)
            if not data:
                break
            connection.sendall(str.encode(reply))
    connection.close()


while True:
    connClient, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ' : ' + str(address[1]))

    start_new_thread(threaded_client, (connClient, ))
    threadCount += 1
    print('Thread Number: ' + str(threadCount))
ServerSocket.close()
