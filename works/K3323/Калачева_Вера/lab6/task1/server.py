import socket

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем его к localhost и порту 5000
server_socket.bind(('localhost', 5000))

server_socket.listen(1)
print("Сервер запущен и ожидает подключение...")

# Принимаем подключение
conn, addr = server_socket.accept()
print(f"Подключился клиент: {addr}")

# Получаем данные от клиента
data = conn.recv(1024)
print("Получено от клиента:", data.decode())

# Отправляем ответ клиенту
conn.sendall("Hello, client".encode())

# Закрываем соединение
conn.close()
server_socket.close()