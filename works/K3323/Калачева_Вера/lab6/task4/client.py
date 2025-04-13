import socket
import threading
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.factory import Factory

class ChatClient(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Гость"
        self.sock = None
        self.user_color = self.generate_random_color()
        Window.size = (380, 600)
        Clock.schedule_once(lambda dt: self.ask_name_popup())

    def generate_random_color(self):
        """Генерация случайного цвета в формате RGB"""
        min_brightness = 0.5

        r = random.uniform(min_brightness, 1.0)
        g = random.uniform(min_brightness, 1.0)
        b = random.uniform(min_brightness, 1.0)

        return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))

    def rgb_to_hex(self, rgb):
        """Преобразует RGB цвет в HEX"""
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

    def add_message(self, msg, user_color):
        bubble = Factory.MessageBubble()

        bubble.ids.msg_label.text = f"[color={user_color}]{msg}[/color]"

        self.ids.messages_container.add_widget(bubble)
        self.ids.messages_container.height += bubble.height

    def ask_name_popup(self):
        """Запрашиваем имя пользователя при старте приложения"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        name_input = TextInput(hint_text="Введите ваше имя", multiline=False)
        ok_button = Button(text="OK", size_hint=(1, 0.3))
        content.add_widget(name_input)
        content.add_widget(ok_button)
        popup = Popup(title="Ваше имя", content=content, size_hint=(0.7, 0.3), auto_dismiss=False)

        def on_ok(instance):
            self.name = name_input.text.strip() or "Гость"
            popup.dismiss()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(('127.0.0.1', 9090))
            self.sock.send(f"{self.name}".encode('utf-8'))
            threading.Thread(target=self.receive_messages, daemon=True).start()

        ok_button.bind(on_press=on_ok)
        popup.open()

    def send_message(self, instance):
        """Отправка сообщения на сервер"""
        if not self.sock:
            return
        msg = self.ids.input_field.text.strip()
        if msg:
            self.add_message(f"[b]{self.name}:[/b] {msg}", self.user_color)
            self.sock.send(f"{msg}".encode('utf-8'))
            self.ids.input_field.text = ''

    def receive_messages(self):
        """Получение сообщений с сервера"""
        while True:
            try:
                msg = self.sock.recv(1024).decode('utf-8')
                if msg:
                    color, name, message = msg.split(":", 2)
                    Clock.schedule_once(lambda dt: self.add_message(message, color))
                else:
                    break
            except Exception as e:
                print(f"Ошибка получения сообщения: {e}")
                break

class ChatApp(App):
    def build(self):
        return ChatClient()


if __name__ == '__main__':
    ChatApp().run()
