import sqlite3
# from pandas import DataFrame
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.lang import Builder

con = sqlite3.connect('Hotel.db')

cur = con.cursor()


class Home(Screen):
    pass


class Guests(Screen):
    reservation = ObjectProperty(None)
    fname = ObjectProperty(None)
    lname = ObjectProperty(None)
    phone = ObjectProperty(None)
    room = ObjectProperty(None)
    email = ObjectProperty(None)
    result = ObjectProperty(None)
    col=["Reservation", "FName","LName", "phone","RoomNum", "Email"]

    def insert(self):
        cur.execute(
            f"INSERT INTO Guests values ({self.reservation.text},'{self.fname.text}','{self.lname.text}' ,'{self.phone.text}', '{self.room.text}' , '{self.email.text}')")
        con.commit()
        self.reservation.text = f"{int(self.reservation.text)+1}"
        self.fname.text=""
        self.lname.text = ""
        self.phone.text = ""
        self.room.text = ""
        self.email.text = ""
        self.result.text = "insert done"

    def delete(self):
        cur.execute(f"DELETE from Guests where reservation={self.reservation.text}")
        con.commit()
        self.result.text ='delete done'

    def update(self):
        cur.execute(f"update Guests set Phone ='{self.phone.text}' where reservation = {self.reservation.text}")
        con.commit()
        self.result.text ='update done'

    def select(self):
        if self.reservation.text == '0':
            sel = con.execute('select * from Guests').fetchall()
            # sel=DataFrame(sel, columns=self.col)
            # sel.to_string(index=False)
            print(sel)
            self.result.text = f"{sel}"
        else:
            sel = con.execute(f'select * from Guests where reservation={self.reservation.text}').fetchall()
            # sel = DataFrame(sel, columns=self.col)
            self.result.text=f"{sel}"


class Rooms(Screen):
    reservation = ObjectProperty(None)
    fname = ObjectProperty(None)
    room = ObjectProperty(None)
    price = ObjectProperty(None)
    beds = ObjectProperty(None)
    smoking = ObjectProperty(None)
    result = ObjectProperty(None)

    def insert(self):
        try:
            cur.execute(
                f"INSERT INTO Rooms values ({self.reservation.text},'{self.fname.text}','{self.room.text}' ,'{self.price.text}', '{self.beds.text}' , '{self.smoking.text}')")
            con.commit()
        except sqlite3.Error as error:
            result = f"An Error occurred : {error}"
            print(result)
            return result

        self.reservation.text = f"{int(self.reservation.text)+1}"
        self.fname.text = ""
        self.room.text = ""
        self.price.text = ""
        self.beds.text = ""
        self.smoking.text = ""
        self.result.text='insert done'

    def delete(self):
        cur.execute(f"DELETE from Rooms where reservation={self.reservation.text}")
        con.commit()
        self.result.text='delete done'

    def update(self):
        cur.execute(f"update Rooms set price ='{self.price.text}' where reservation = {self.reservation.text}")
        con.commit()
        self.result.text='update done'

    def select(self):
        if self.reservation.text == '0':
            sel = con.execute('select * from Rooms').fetchall()
            # sel=DataFrame(sel, columns=self.col)
            # sel.to_string(index=False)
            print(sel)
            self.result.text = f"{sel}"
        else:
            sel = con.execute(f'select * from Rooms where reservation={self.reservation.text}').fetchall()
            # sel = DataFrame(sel, columns=self.col)
            self.result.text=f"{sel}"


class Reservation(Screen):
    reservation = ObjectProperty(None)
    fname = ObjectProperty(None)
    checkin = ObjectProperty(None)
    checkout = ObjectProperty(None)
    room = ObjectProperty(None)
    result = ObjectProperty(None)

    def insert(self):
        cur.execute(
            f"INSERT INTO Reservation values ({self.reservation.text},'{self.fname.text}', {self.room.text},'{self.checkin.text}' ,'{self.checkout.text}')")
        con.commit()
        self.reservation.text = f"{int(self.reservation.text)+1}"
        self.fname.text = ""
        self.room.text = ""
        self.checkin.text = "2-5-2022"
        self.checkout.text = "2-5-2022"
        self.result.text = 'insert done'

    def delete(self):
        cur.execute(f"DELETE from Reservation where reservation={self.reservation.text}")
        con.commit()
        self.result.text ='delete done'

    def update(self):
        cur.execute(f"update Reservation set check_in ='{self.checkin.text}' where reservation = {self.reservation.text}")
        con.commit()
        self.result.text ='update done'

    def select(self):
        if self.reservation.text == '0':
            sel = con.execute('select * from Reservation').fetchall()
            # sel=DataFrame(sel, columns=self.col)
            # sel.to_string(index=False)
            print(sel)
            self.result.text = f"{sel}"
        else:
            sel = con.execute(f'select * from Reservation where reservation={self.reservation.text}').fetchall()
            # sel = DataFrame(sel, columns=self.col)
            self.result.text=f"{sel}"


class WindowManager(ScreenManager):
    pass


class LimitInput(TextInput):
    def keyboard_on_key_up(self, keycode, text):
        if self.readonly and text[1] == "backspace":
            self.readonly = False
            self.do_backspace()


kv= Builder.load_file('hotel.kv')


class HotelGUI(App):

    def build(self):
        return kv


if __name__ == "__main__":
    HotelGUI().run()
