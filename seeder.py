import socket, json

FILE = "ThumbsUpEmoji.png"
META = json.load(open(FILE + ".json", "r"))

def serve_piece(conn):
    request = conn.recv(1024).decode()
    chunk_index = int(request)

    start = chunk_index * META["chunk_size"]
    end = start + META["chunk_size"]

    with open(FILE, "rb") as f:
        f.seek(start)
        data = f.read(META["chunk_size"])

    conn.sendall(data)

def main():
    s = socket.socket()
    s.bind(("127.0.0.1", 5000))
    s.listen(5)

    print("Seeder listening on port 5000")

    conn, addr = s.accept()
    while True:
        print("connection from", addr)
        serve_piece(conn)
        conn.close()

if __name__ == "__main__":
    main()