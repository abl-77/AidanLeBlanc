def decode(encoded_message, decoded_message, key):
    msg = ""
    with open(encoded_message, "r") as m:
        for line in m:
            msg += decodeLine(line, key)
        m.close()
    with open(decoded_message, "w") as d:
        d.write(msg)
        d.close()

def decodeLine(line, key):
    str = ""
    for ltr in line:
        if ord(ltr) >= 32 and ord(ltr) <= 126:
            if (ord(ltr) + key <= 126):
                str += (chr((ord(ltr) + key)))
            else:
                str += (chr(32 + (ord(ltr) + key) % 127))
    str += "\n"
    return str

def encode(message, result, key):
    key = 95 - key
    msg = ""
    with open(message, "r") as m:
        for line in m:
            msg += encodeLine(line, key)
        m.close()
    with open(result, "w") as r:
        r.write(msg)
        r.close()

def encodeLine(line, key):
    str = ""
    for ltr in line:
        if ord(ltr) >= 32 and ord(ltr) <= 126:
            if (ord(ltr) + key <= 126):
                str += (chr((ord(ltr) + key)))
            else:
                str += (chr(32 + (ord(ltr) + key) % 127))
    str += "\n"
    return str

    
encode("sent_decoded.txt", "received_encoded.txt", 85)

decode("received_encoded.txt", "received_decoded.txt", 85)