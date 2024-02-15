import socket
import threading

# constants
# HOST = socket.gethostbyname(socket.gethostname())
HOST = "127.0.0.1"
PORT = 8081
SRV_ADDR = HOST, PORT
FORMAT = "utf-8"

# global veriables
client_list = []
nickname_list = []

stop_thread = False


# Broadcast messages to all clients
def broadcast(message, sender):
    for client in client_list:
        if client == sender:
            continue
        else:
            client.send(message.encode(FORMAT))


# Receive and send messages from clients to other clients
def client_handler(client):
    index = client_list.index(client)
    nickname = nickname_list[index]
    
    client.send("Welcome to the server!".encode(FORMAT))
    
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == "!dc":
                broadcast(f"[SERVER]: {nickname} left the server.", client)
                print(f"[SERVER]: {nickname} left the server.")
                client_list.remove(client)
                nickname_list.remove(nickname)
                client.close()
                break
            else:
                print(f"{nickname}: {message}")
                broadcast(f"{nickname}: {message}", client)

        except Exception as e:
            print(f"[ERROR]: {e}")
            client_list.remove(client)
            nickname_list.remove(nickname)
            client.close()
            break
    print(
        f"[INFO]:Remaining Connections: {len(client_list)}")


# set up server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SRV_ADDR)
server.listen()
print(f"[INFO]: Server listening on {HOST}:{PORT}")

while True:
    try:
        client, address = server.accept()

        client.send("nick?".encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)

        if nickname == "admin":
            client.send("pass?".encode(FORMAT))
            password = client.recv(1024).decode(FORMAT)
            if password != "admin":
                client.send("refused?".encode(FORMAT))
                client.close()
                continue

        print(
            f"[INFO]: New connection form {str(address)}, with nickname: {nickname}")

        client_list.append(client)
        nickname_list.append(nickname)

        broadcast(f"[SERVER]: {nickname} joined the server.", client)

        print(
            f"Active connections: {len(client_list)}")

        t1 = threading.Thread(target=client_handler, args=(client,))
        t1.start()
    except KeyboardInterrupt:
        server.close()
        stop_thread = True
        break
    except Exception as e:
        print(f"[ERROR]: {e}")
        server.close()
        stop_thread = True
        break
