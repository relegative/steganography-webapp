

def write_data(img_filename, message):
    msg_bytes = bytes(message, 'utf-8')
    with open(img_filename, 'ab') as f:
        f.write(msg_bytes)

def read_text(img_filename):
    with open(img_filename, 'rb') as f:
        content = f.read()
        offset = content.index(bytes.fromhex("FFD9"))

        f.seek(offset + 2)
        message = str(f.read(), 'utf-8')

    return message


