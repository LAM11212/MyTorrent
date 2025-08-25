import socket

def connect_peers(ip, port):
    peer_socket = socket.socket()

    try:
        peer_socket.connect((ip, port))
        return peer_socket
    except socket.error as e:
        print(f"Err connecting to peer {ip}:{port} - {e}")
        return None