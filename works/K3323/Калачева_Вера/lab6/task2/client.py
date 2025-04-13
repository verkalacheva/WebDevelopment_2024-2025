import socket

base = input("Введите длину основания параллелограмма: ")
height = input("Введите высоту параллелограмма: ")

message = f"{base} {height}"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5000))

# Отправляем сообщение серверу
client_socket.sendall(message.encode())

# Получаем ответ от сервера
data = client_socket.recv(1024).decode()
print("Ответ от сервера:", data)

client_socket.close()