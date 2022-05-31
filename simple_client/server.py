import sqlite3
import socket

con = sqlite3.connect('../Hotel.db')
cur = con.cursor()

# cur.execute(''' create table if not exists Guests
# ( reservation number not null,
# FName text ,
# LName text ,
# Phone text ,
# RoomNum number ,
# Email text,
# constraint c1 primary key (reservation))
#
# ''')
#
# cur.execute('''create table if not exists Rooms (
#
# reservation number ,
# FName text ,
# roomNum number ,
# price number ,
# beds text,
# smoking text,
# constraint pr primary key (roomNum),
# constraint fr foreign key (reservation ,FName) References Guests(reservation,FName  ) )
# ''')
# cur.execute('''create table if not exists Reservation (
#
# reservation number ,
# FName text ,
# roomNum number ,
# check_in text ,
# check_out text,
# constraint pr primary key (reservation),
# constraint fr foreign key (reservation ,FName,roomNum) References Guests(reservation, FName ,roomNum ) )
# ''')
# cur.execute("INSERT INTO Reservation  values (1,'Hager',22 ,'10-3-2022' , '20-3-2022')")
# cur.execute("INSERT INTO Reservation  values (2,'Manar',23 ,'15-2-2022' , '10-3-2022')")
# cur.execute("INSERT INTO Reservation  values (3,'Hemat' ,25 ,'25-2-2022' , '15-3-2022')")
#

# insert Guests (reservation , FName ,LName , phone ,RoomNum , Email)
# cur.execute("INSERT INTO Guests  values (1,'Hager','Besar' ,'01022152513' , 22 , 'hagerbesar10@gmail.com')")
# cur.execute("INSERT INTO Guests  values (2,'Manar','Moenes' ,'01026455258' , 23 , 'manar10@gmail.com')")
# cur.execute("INSERT INTO Guests  values (3,'Hemat' ,'Shawky' ,'01013224677' , 25 , 'hemat10@gmail.com')")
# cur.execute("INSERT INTO Guests  values (4,'Mariam','Zahana' ,'01025146333' , 24 , 'mariam10@gmail.com')")
# cur.execute("INSERT INTO Guests  values (5,'omnia' ,'Ashraf' ,'01034456288' , 26 , 'omnia10@gmail.com')")
# con.commit()

# # insert rooms (reservation , FName , RoomNum, price, beds , smoking)
# cur.execute("INSERT INTO Rooms  values (1,'Hager',22, 2000 ,'single' , 'no smoking')")
# cur.execute("INSERT INTO Rooms  values (2,'Manar',23, 1000 ,'double' , 'smoking')")
# cur.execute("INSERT INTO Rooms  values (3,'mariam',24, 1500 ,'double' , 'no smoking')")
# cur.execute("INSERT INTO Rooms  values (4,'Hemat',25, 2000 ,'single' , 'smoking')")
# cur.execute("INSERT INTO Rooms  values (5,'omnia',26, 1000 ,'single' , 'smoking')")
# con.commit()
# print('done insert')

# UPDATE
# cur.execute("update Rooms set price =1300 where roomNum = 23")
# cur.execute("update Guests set Phone ='01248744938' where reservation = 4")
# con.commit()
# print('update done')

# sel = con.execute('select * from Guests').fetchall()
# print(sel)
# DELETE
# cur.execute("DELETE from Guests where reservation=5")
# con.commit()
# print('Delete done')
# sel = con.execute('select * from Guests').fetchall()
# print(sel)

# Guests (reservation , FName ,LName , phone ,RoomNum , Email)


def select(data):
    try:
        con.execute(f'{data}')
        con.commit()
        sel = con.execute(f'{data}').fetchall()
        print(sel)
        return sel
    except sqlite3.Error as error:
        sel = f"An Error occurred : {error}"
        print(sel)
        return sel


def runServer():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))

        s.listen()
        print('success connection')

        conn, addr = s.accept()
        with conn:
            print(f'Connected by {addr}')
            while True:
                dataRecv = conn.recv(2048)
                dataRecv = dataRecv.decode()
                if not dataRecv:
                    break
                print(dataRecv)
                dataSend = select(dataRecv)
                dataSend = str(dataSend)
                dataSend = dataSend.encode()
                conn.sendall(dataSend)


if __name__ == "__main__":
    runServer()
