import socket
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from component import selectView

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

Builder.load_file('kivyFile/room.kv')


class Rooms(Widget):
    reservation = ObjectProperty(None)
    fname = ObjectProperty(None)
    room = ObjectProperty(None)
    price = ObjectProperty(None)
    beds = ObjectProperty(None)
    smoking = ObjectProperty(None)
    result = ObjectProperty(None)
    client = ObjectProperty(None)
    local=[]

    print('Waiting for connection')
    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))

    ClientSocket.send(str.encode('Room Service G1'))
    Response = ClientSocket.recv(2048).decode('utf-8')
    print(Response)

    def insert(self):
        data=f"INSERT INTO Rooms values ({self.reservation.text},'{self.fname.text}','{self.room.text}','{self.price.text}','{self.beds.text}','{self.smoking.text}')"
        ClientSocket.sendall(str.encode('opp'))
        opp = ClientSocket.recv(2048).decode('utf-8')
        print(opp)
        ClientSocket.sendall(str.encode(self.reservation.text))
        ClientSocket.sendall(str.encode(data))
        Response = ClientSocket.recv(2048).decode('utf-8')
        print(Response)
        self.reservation.text = f"{int(self.reservation.text)+1}"
        self.fname.text = ""
        self.room.text = ""
        self.price.text = ""
        self.beds.text = ""
        self.smoking.text = ""
        self.result.text=f'insert {Response}'

    def delete(self):
        data=f"DELETE from Rooms where reservation={self.reservation.text}"
        ClientSocket.sendall(str.encode('opp'))
        opp = ClientSocket.recv(2048).decode('utf-8')
        print(opp)
        ClientSocket.sendall(str.encode(self.reservation.text))
        ClientSocket.sendall(str.encode(data))
        Response = ClientSocket.recv(2048).decode('utf-8')
        self.result.text=f'delete {Response} '

    def update(self):
        data=f"update Rooms set price ='{self.price.text}' where reservation = {self.reservation.text}"
        ClientSocket.sendall(str.encode('opp'))
        opp = ClientSocket.recv(2048).decode('utf-8')
        print(opp)
        ClientSocket.sendall(str.encode(self.reservation.text))
        ClientSocket.sendall(str.encode(data))
        Response = ClientSocket.recv(2048).decode('utf-8')
        self.result.text=f'update {Response}'

    def select(self):
        if int(self.reservation.text) <= 50 and int(self.reservation.text)!= 0:
            data= f"select * from roomG1 where reservation={self.reservation.text}"
            self.result.text = f"{selectView(data)}"
            self.local.append(f"{data}")
        else:
            print(int(self.reservation.text))
            ClientSocket.sendall(str.encode('select'))
            opp = ClientSocket.recv(2048).decode('utf-8')
            print(opp)
            if self.reservation.text == '0':
                data="select * from Rooms"
                ClientSocket.sendall(str.encode(self.reservation.text))
                ClientSocket.sendall(str.encode(data))
                Response = ClientSocket.recv(2048).decode('utf-8')
                print(Response)
                self.result.text = f"{Response}"
            else:
                data = f"select * from Rooms where reservation= {self.reservation.text}"
                ClientSocket.sendall(str.encode(self.reservation.text))
                ClientSocket.sendall(str.encode(data))
                Response = ClientSocket.recv(2048).decode('utf-8')
                print(Response)
                self.result.text = f"{Response}"

    def info(self):
        self.client.text = 'Room Service G1'
        ClientSocket.sendall(str.encode('info'))
        opp = ClientSocket.recv(2048).decode('utf-8')
        print(opp)
        Response = ClientSocket.recv(2048).decode('utf-8')
        local ='\n  '.join(self.local)
        self.result.text = f'Clients server : \n{Response} \n\nLocal Query :\n  {local}'

    def redistribution(self):
        ClientSocket.sendall(str.encode('ReDis'))
        opp = ClientSocket.recv(2048).decode('utf-8')
        print(opp)
        Response = ClientSocket.recv(2048).decode('utf-8')
        self.result.text = f'Clients server : \n{Response}'


class RoomGUI(App):
    def build(self):
        return Rooms()


if __name__ == "__main__":
    RoomGUI().run()
    ClientSocket.close()

# print('Waiting for connection')
# try:
#     ClientSocket.connect((host, port))
# except socket.error as e:
#     print(str(e))
#
# ClientSocket.send(str.encode('room'))
# Response = ClientSocket.recv(2048).decode('utf-8')
# print(Response)
#
# while True:
#     Input = input('Say Something: ')
#     ClientSocket.sendall(str.encode(Input))
#     Response = ClientSocket.recv(2048)
#     print(Response.decode('utf-8'))

# ClientSocket.close()

