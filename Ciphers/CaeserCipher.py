
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
    words = line.split()
    for word in words:
        str += decodeWord(word, key)
    str += "\n"
    return str

def decodeWord(word, key):
    shifted = ""
    for ltr in word:
        if ord(ltr) >= 97 and ord(ltr) <= 122:
            if (ord(ltr) + key <= 122):
                shifted += (chr((ord(ltr) + key)))
            else:
                shifted += (chr(97 + (ord(ltr) + key) % 123))
        elif ord(ltr) >= 65 and ord(ltr) <= 90:
            if (ord(ltr) + key <= 90):
                shifted += (chr((ord(ltr) + key)))
            else:
                shifted += (chr(65 + (ord(ltr) + key) % 91))
        else:
            shifted += ltr
    
    return shifted + " "

def encode(message, result, key):
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
    words = line.split()
    for word in words:
        str += encodeWord(word, key)
    str += "\n"
    return str

def encodeWord(word, key):
    key = 26 - key
    shifted = ""
    for ltr in word:
        if ord(ltr) >= 97 and ord(ltr) <= 122:
            if (ord(ltr) + key <= 122):
                shifted += (chr((ord(ltr) + key)))
            else:
                shifted += (chr(97 + (ord(ltr) + key) % 123))
        elif ord(ltr) >= 65 and ord(ltr) <= 90:
            if (ord(ltr) + key <= 90):
                shifted += (chr((ord(ltr) + key)))
            else:
                shifted += (chr(65 + (ord(ltr) + key) % 91))
        else:
            shifted += ltr
    
    return shifted + " "

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

encode("sent_decoded.txt", "sent_encoded.txt", 10)

decode("received_encoded.txt", "received_decoded.txt", 10)