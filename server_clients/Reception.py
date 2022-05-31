import socket
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from component import selectView

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

Builder.load_file('kivyFile/reservation.kv')


class Reservation(Widget):
    reservation = ObjectProperty(None)
    fname = ObjectProperty(None)
    checkin = ObjectProperty(None)
    checkout = ObjectProperty(None)
    room = ObjectProperty(None)
    result = ObjectProperty(None)

    print('Waiting for connection')
    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))

    ClientSocket.send(str.encode('Reception'))
    Response = ClientSocket.recv(2048).decode('utf-8')
    print(Response)

    def insert(self):
        data= f"INSERT INTO Reservation values ({self.reservation.text},'{self.fname.text}', {self.room.text},'{self.checkin.text}' ,'{self.checkout.text}')"
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
        self.checkin.text = "2-5-2022"
        self.checkout.text = "2-5-2022"
        self.result.text = f'insert {Response}'

    def delete(self):
        data = f"DELETE from Reservation where reservation={self.reservation.text}"
        ClientSocket.sendall(str.encode('opp'))
        opp = ClientSocket.recv(2048).decode('utf-8')
        print(opp)
        ClientSocket.sendall(str.encode(self.reservation.text))
        ClientSocket.sendall(str.encode(data))
        Response = ClientSocket.recv(2048).decode('utf-8')
        self.result.text = f'delete {Response} '

    def update(self):
        data = f"update Reservation set price ='{self.price.text}' where reservation = {self.reservation.text}"
        ClientSocket.sendall(str.encode('opp'))
        opp = ClientSocket.recv(2048).decode('utf-8')
        print(opp)
        ClientSocket.sendall(str.encode(self.reservation.text))
        ClientSocket.sendall(str.encode(data))
        Response = ClientSocket.recv(2048).decode('utf-8')
        self.result.text = f'update {Response}'

    def select(self):
        ClientSocket.sendall(str.encode('select'))
        opp = ClientSocket.recv(2048).decode('utf-8')
        print(opp)
        if self.reservation.text == '0':
            data = "select * from Reservation"
            ClientSocket.sendall(str.encode(self.reservation.text))
            ClientSocket.sendall(str.encode(data))
            Response = ClientSocket.recv(2048).decode('utf-8')
            print(Response)
            self.result.text = f"{Response}"
        else:
            data = f"select * from Reservation where reservation={self.reservation.text}"
            ClientSocket.sendall(str.encode(self.reservation.text))
            ClientSocket.sendall(str.encode(data))
            Response = ClientSocket.recv(2048).decode('utf-8')
            print(Response)
            self.result.text = f"{Response}"

    def info(self):
        ClientSocket.sendall(str.encode('info'))
        opp = ClientSocket.recv(2048).decode('utf-8')
        print(opp)
        Response = ClientSocket.recv(2048).decode('utf-8')
        self.result.text = f'Clients server : \n {Response}'

    def redistribution(self):
        ClientSocket.sendall(str.encode('ReDis'))
        opp = ClientSocket.recv(2048).decode('utf-8')
        print(opp)
        Response = ClientSocket.recv(2048).decode('utf-8')
        self.result.text = f'Clients server : \n {Response}'


class ReservationGUI(App):
    def build(self):
        return Reservation()


if __name__ == "__main__":
    ReservationGUI().run()
    ClientSocket.close()
