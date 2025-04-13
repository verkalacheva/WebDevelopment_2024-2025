import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 5000))

# Отправляем сообщение серверу
client_socket.sendall("Hello, server".encode())

# Получаем ответ от сервера
data = client_socket.recv(1024)
print("Получено от сервера:", data.decode())

# Закрываем соединение
client_socket.close()