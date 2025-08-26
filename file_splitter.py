import hashlib, json, os

def create_metadata(filename, chunk_size=1024):
    filesize = os.path.getsize(filename)
    chunks = []

    with open(filename, "rb") as f:
        while chunk := f.read(chunk_size):
            h = hashlib.sha256(chunk).hexdigest()
            chunks.append(h)

    
    metadata = {
        "file_name": os.path.basename(filename),
        "file_size": filesize,
        "chunk_size": chunk_size,
        "chunks": chunks
    }

    with open(filename + ".json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print("Metadata written to", filename + ".json")


if __name__ == '__main__':
    create_metadata('ThumbsUpEmoji.png')
