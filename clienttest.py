import socket

s = socket.socket()
s.connect(("127.0.0.1", 5000))

while True:
    msg = input("msg: ")
    s.sendall(msg.encode())

    reply = s.recv(1024).decode()
    if not reply:
        break
    print(f"server: {reply}")