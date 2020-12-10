import socket
import os

# SERVER_HOST = "74.64.134.11"
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 80

BUFFER_SIZE = 32

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)


print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = s.accept()
print(f"[+] {address} is connected.")

with open("downloads/" + "received.jpg", "wb") as f:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            print("not read")
            break

        f.write(bytes_read)
        print("Recieved Buffer.")

client_socket.close()
s.close()
