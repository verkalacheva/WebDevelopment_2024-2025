import socket

def get_html_response():
    with open('index.html', 'r', encoding='utf-8') as f:
        body = f.read()

    response_line = "HTTP/1.0 200 OK\r\n"
    headers = f"Content-Type: text/html; charset=utf-8\r\nContent-Length: {len(body.encode('utf-8'))}\r\n\r\n"
    return (response_line + headers + body).encode('utf-8')

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)
    print("Сервер запущен на http://localhost:5000")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Подключение от {addr}")

            request = conn.recv(1024).decode('utf-8')
            print("Получен запрос:")
            print(request)

            response = get_html_response()

            conn.sendall(response)
            conn.close()

    except KeyboardInterrupt:
        print("\nСервер остановлен.")
        server_socket.close()

if __name__ == "__main__":
    main()
