import socket
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class ClintGUI(App):

    def build(self):
        self.root = GridLayout(cols=1, padding=20,spacing=10)
        hotel = Label(text='BIO Hotel', size_hint=(1, 0.5), font_size='40sp', color='#00FFCE')
        guest = Label(text='Enter Query', size_hint=(1, 0.3))
        self.query = TextInput(multiline=True, input_type='text')
        select_btn = Button(text='Select', size_hint=(0.2, 0.7), width=100, bold=True, font_size='30sp',
                            background_color='#00FFCE', on_press=self.runClint)
        self.result = Label(text='Query Result', size_hint=(1.0, 1.0), halign="left", valign="middle", font_size='20sp', color='#00FFCE')
        self.result.bind(size=self.result.setter('text_size'))

        self.root.add_widget(hotel)
        self.root.add_widget(guest)
        self.root.add_widget(self.query)
        self.root.add_widget(select_btn)
        self.root.add_widget(self.result)
        return self.root

    def runClint(self, i):
        host = '127.0.0.1'
        port = 65432
        dataQuery = self.query.text
        dataQuery = dataQuery.encode()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print('Sending....')
            s.sendall(dataQuery)
            print('Send')
            dataRecv = s.recv(1024)
            print('receiving from Server....')
        print(f"Receiving : {dataRecv}")
        self.result.text=dataRecv.decode()


if __name__ == "__main__":
    ClintGUI().run()
    # runClint()
