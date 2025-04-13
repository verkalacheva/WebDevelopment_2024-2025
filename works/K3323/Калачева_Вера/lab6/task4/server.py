import socket
import threading
import random

clients = {}  # conn: (name, color)

def generate_random_color():
    """Генерация случайного цвета в формате RGB"""
    min_brightness = 0.5

    r = random.uniform(min_brightness, 1.0)
    g = random.uniform(min_brightness, 1.0)
    b = random.uniform(min_brightness, 1.0)

    return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))


def handle_client(conn, addr):
    try:
        name = conn.recv(1024).decode('utf-8')
        if not name:
            print(f"Ошибка: имя не получено от клиента {addr}")
            conn.close()
            return

        color = generate_random_color()

        clients[conn] = (name, color)
        print(f"{name} подключился с {addr}, цвет: {color}")

        broadcast(f"{name} вошел в чат.", conn, color)

        while True:
            msg = conn.recv(1024).decode('utf-8')
            if not msg:
                print(f"Сообщение от {name} пустое, клиент отключается.")
                break
            print(f"Получено сообщение от {name}: {msg}")

            broadcast(f"{name}: {msg}", conn, color)
    except Exception as e:
        print(f"Ошибка при обработке клиента {addr}: {e}")
    finally:
        conn.close()
        if conn in clients:
            print(f"{clients[conn][0]} отключился.")
            broadcast(f"{clients[conn][0]} покинул чат.", conn, clients[conn][1])
            del clients[conn]

def broadcast(msg, sender_conn=None, color=None):
    """Отправить сообщение всем клиентам, кроме отправителя"""
    print(f"Рассылаем сообщение: {msg}")
    for client in clients:
        if client != sender_conn:  # не отправляем сообщение обратно отправителю
            try:
                message = f"{color}:{clients[client][0]}: {msg}"
                client.send(message.encode('utf-8'))
                print(f"Отправлено сообщение клиенту {clients[client][0]}")
            except Exception as e:
                print(f"Ошибка при отправке сообщения клиенту {clients[client][0]}: {e}")

def main():
    host = '127.0.0.1'
    port = 9090

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print("Сервер запущен... Нажмите Ctrl+C для остановки.")

    while True:
        try:
            conn, addr = server.accept()
            print(f"Новое подключение от {addr}")
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        except Exception as e:
            print(f"Ошибка при подключении: {e}")

if __name__ == '__main__':
    main()
