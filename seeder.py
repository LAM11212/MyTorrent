import socket, json, struct, hashlib

FILE = "ThumbsUpEmoji.png"
META = json.load(open(FILE + ".json", "r"))
ensure_protocol = b'FemboyTorrent'
ensure_hash = hashlib.sha256(open(FILE, "rb").read()).digest()
ensure_hash = ensure_hash[:20]

def serve_piece(conn):
    request = conn.recv(1024).decode()
    chunk_index = int(request)

    start = chunk_index * META["chunk_size"]
    end = start + META["chunk_size"]

    with open(FILE, "rb") as f:
        f.seek(start)
        data = f.read(META["chunk_size"])

    conn.sendall(data)

def connect_with_tracker():
    s = socket.socket()
    s.connect(("127.0.0.1", 8000))
    peer_info = {
        "peer_id": "abcd123",
        "ip": "127.0.0.1",
        "port": 5000,
        "is_seeder": True
    }
    msg = {"action": "register",
           "peer": peer_info}
    s.sendall(json.dumps(msg).encode())
    s.close()

def main():
    s = socket.socket()
    s.bind(("127.0.0.1", 5000))
    s.listen(5)

    print("Seeder listening on port 5000")
    connect_with_tracker()

    
    while True:
        conn, addr = s.accept()
        print("connection from", addr)
        if handle_handshake(conn):
            serve_piece(conn)
        conn.close()

def handle_handshake(conn) -> bool:
        pstrlen_data = conn.recv(1)
        if not pstrlen_data:
            return None
        pstrlen = struct.unpack("B", pstrlen_data)[0]
        rest_len = pstrlen + 8 + 20 + 20
        rest = conn.recv(rest_len)

        if len(rest) < rest_len:
            print("invalid handshake")
            return False
        fmt = f"{pstrlen}s8s20s20s"
        protocol, reserved, file_hash, peer_id = struct.unpack(fmt, rest)

        if protocol != ensure_protocol:
            print(f"invalid protocol: {protocol}")
            return False
        
        if file_hash != ensure_hash:
            print("incorrect file hash")
            return False
        
        print(f"Handshake OK from peer {peer_id}")
        return True
if __name__ == "__main__":
    main()