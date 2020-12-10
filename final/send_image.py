import socket
import os

SERVER_HOST = "18.222.187.211"
vermont_ip = '66.220.238.180'
SERVER_PORT = 4141

BUFFER_SIZE = 32

s = socket.socket()
s.bind((vermont_ip, 80))
s.connect((SERVER_HOST, SERVER_PORT))
#
s.listen(5)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = s.accept()
print(f"[+] {address} is connected.")

with open("image.jpg", "wb") as f:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break

        f.write(bytes_read)
        print("Recieved Buffer.")

client_socket.close()
s.close()
