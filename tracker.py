import socket, json


tracker = {}

def connect_peers(ip, port):
    peer_socket = socket.socket()

    try:
        peer_socket.connect((ip, port))
        return peer_socket
    except socket.error as e:
        print(f"Err connecting to peer {ip}:{port} - {e}")
        return None
    
def add_peer(info_hash, peer):
    if info_hash not in tracker:
        tracker[info_hash] = []
    tracker[info_hash].append(peer)

    return tracker

def tracker_server():
    s = socket.socket()
    s.bind(("127.0.0.1", 8000))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        data = conn.recv(4096).decode()
        if not data:
            conn.close()
            continue
        
        msg = json.loads(data)
        if msg.get("action") == "register":
            peer = msg["peer"]
            add_peer("xyz789", peer)
            print(f"Registered peer: {peer}")
            conn.sendall(b"OK")

        elif msg.get("action") == "get_peers":
            peers = tracker.get("xyz789", [])
            conn.sendall(json.dumps(peers).encode())
        conn.close()

if __name__ == '__main__':
    tracker_server()