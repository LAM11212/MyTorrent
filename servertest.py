import socket, json

s = socket.socket()
s.bind(("127.0.0.1", 5000))
s.listen(3)

conn, addr = s.accept()
print(f"connection from {addr}")
while True:
    msg = conn.recv(1024).decode()
    if not msg:
        break
    print(f"client says: {msg}")

    reply = f"thank you client {addr} for reaching out, i hope you are well :3"
    conn.sendall(reply.encode())
conn.close()
