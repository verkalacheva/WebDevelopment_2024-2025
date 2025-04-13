import socket

def calculate_area(base, height):
    return base * height

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5000))
server_socket.listen(1)
print("Сервер запущен и ожидает подключение...")


conn, addr = server_socket.accept()
print(f"Подключился клиент: {addr}")

data = conn.recv(1024).decode()

print("Получено от клиента:", data)

try:
    base, height = map(float, data.split())
    area = calculate_area(base, height)
    response = f"Площадь параллелограмма: {area}"
except ValueError:
    response = "Ошибка: введите два числа через пробел."

conn.sendall(response.encode())
conn.close()

server_socket.close()