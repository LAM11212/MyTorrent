import socket, json, hashlib, struct, random, string

FILENAME = "ThumbsUpEmoji.png"

META = json.load(open(FILENAME + ".json", "r"))

output = open("downloaded_" + META["file_name"], "wb")

def leecher_start():
    for i, expected_hash in enumerate(META["chunks"]):
        peer_socket = socket.socket()
        peer_socket.connect(("127.0.0.1", 5000))
    
        peer_id = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        file_hash = bytes.fromhex(META["file_hash"])[:20]
        establish_conn(peer_socket, file_hash, peer_id)

        peer_socket.send(str(i).encode())
        data = b""
        while True:
            packet = peer_socket.recv(1024)
            if not packet:
                break
            data += packet
        peer_socket.close()

        if hashlib.sha256(data).hexdigest() == expected_hash:
            print(f"Chunk {i} OK")
            output.write(data)
        else:
            print(f"Chunk {i} FAILED (ERR: Hash Mismatch)")
            break

    output.close()
    print("Download Complete")


def establish_conn(peer_socket, file_hash, peer_id):
    protocol = b'FemboyTorrent'
    pstrlen = len(protocol)
    reserved = b'\x00' * 8

    file_hash = file_hash[:20]
    peer_id = peer_id.encode()[:20]
    handshake_msg = struct.pack(f'B{pstrlen}s8s20s20s', pstrlen, protocol, reserved, file_hash, peer_id)
    peer_socket.send(handshake_msg) # initiates handshake with seeder

    # check handshake recieved from seeder (2 way handshake)
    pstrlen_data = peer_socket.recv(1)
    if not pstrlen_data:
        raise ConnectionError("No handshake recieved from seeder")
    rest_len = pstrlen + 8 + 20 + 20
    rest = peer_socket.recv(rest_len)
    protocol, reserved, resp_hash, resp_id = struct.unpack(f"{pstrlen}s8s20s20s", rest)

    if resp_hash != file_hash:
        raise ValueError("Seeder responded with wrong hash")
    print(f"Handshake sent to peer {peer_socket.getpeername()}")

if __name__ == '__main__':
    leecher_start()