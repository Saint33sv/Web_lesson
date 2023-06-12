import socket


server = socket.create_server(("127.0.0.1", 8000)) # создается соккет (пара ip, порт)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # освобождает порт после остановки скрипта

server.listen(10) # длина очереди (сколько соединений слушает сервер)

client_socket, address = server.accept() # получаем соккет клиента и его адрес
received_data = client_socket.recv(1024).decode("utf-8") # читаем с клиенского соккета и декодируем в utf-8

print("Получили данные по соккету", received_data)
