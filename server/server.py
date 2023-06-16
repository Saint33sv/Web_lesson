import socket


server = socket.create_server(("127.0.0.1", 8000)) # создается соккет (пара ip, порт)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # освобождает порт после остановки скрипта

server.listen(10) # длина очереди (сколько соединений слушает сервер)
try:
    while True:
        client_socket, address = server.accept() # получаем соккет клиента и его адрес
        received_data = client_socket.recv(1024).decode("utf-8") # читаем с клиенского соккета и декодируем в utf-8

        print("Получили данные по соккету", received_data)


        path = received_data.split(" ")[1] # Получаем путь для отправки ответа клиенту
        response = f"""HTTP/1.1 200 OK\nContent-type: text/html; charset=utf-8\n\nПривеет! <br/>Path: {path}""" # Ответ который отправим в браузер
        # два переноса строки в ответе означают что http-заголовки закончились и дальше идет тело ответа-html
        client_socket.send(response.encode("utf-8")) # отправка ответа в клиенский соккет в бинарном виде
        client_socket.shutdown(socket.SHUT_RDWR) # выключить клиентский соккет
except KeyboardInterrupt:
    server.shutdown(socket.SHUT_RDWR) # выключить сервер
    server.close() # закрыть сервер
