import matplotlib.pyplot as plt

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

def decodeWord(word, key):
    code = []
    for ltr in word:
        if ord(ltr) >= 32 and ord(ltr) <= 126:
            if (ord(ltr) + key <= 126):
                code.append(chr((ord(ltr) + key)))
            else:
                code.append(chr(32 + (ord(ltr) + key) % 127))
    decoded = ""
    for char in code:
        decoded += char
    
    return decoded + " "

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

def encodeWord(word, key):
    key = 95 - key
    code = []
    for ltr in word:
        if ord(ltr) >= 32 and ord(ltr) <= 126:
            if (ord(ltr) + key <= 126):
                code.append(chr((ord(ltr) + key)))
            else:
                code.append(chr(32 + (ord(ltr) + key) % 127))
    
    encoded = ""
    for char in code:
        encoded += char
    
    return encoded + " "

def frequencyAnalysis(encoded_message, decoded_message):
    frequency = {}
    with open(encoded_message, "r") as m:
        for line in m:
            for ltr in line:
                if (ord(ltr) >= 32 and ord(ltr) < 127):
                    if (ord(ltr) in frequency):
                        frequency[ord(ltr)] += 1
                    else:
                        frequency[ord(ltr)] = 1
        m.close()
    ltrs = list(frequency.keys())
    freq = list(frequency.values())

    # plt.bar(range(len(ltrs)), freq, tick_label=ltrs)
    key = estimatedKey(frequency)
    decode(encoded_message, decoded_message, key)

def estimatedKey(frequency):
    keyFreq = 0
    key = 0
    for ltr in frequency:
        if (frequency[ltr] > keyFreq):
            key = ltr
            keyFreq = frequency[ltr]
    if key <= ord('e'):
        return ord('e') - key
    return 94 - (key - ord('e'))
    
encode("sent_decoded.txt", "received_encoded.txt", 85)

# frequencyAnalysis("received_encoded.txt", "received_decoded.txt")

decode("received_encoded.txt", "received_decoded.txt", 85)