
import matplotlib.pyplot as plt
import numpy as np

def decode(encoded_message, decoded_message, keys):
    check = ""
    i = 0
    while check == "":
        print(f"Using key {keys[i]}")
        with open(encoded_message, "r") as m:
            test = m.readline()
            test = decodeLine(test, keys[i])
            print(f"First Line: {test}")
            check = input("Verify Results:")
            
            if check == "":
                i += 1
                continue
            
            msg = test
            for line in m:
                msg += decodeLine(line, keys[i])
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
                if (ord(ltr) >= 65 and ord(ltr) < 123):
                    if (ord(ltr) in frequency):
                        frequency[ord(ltr)] += 1
                    else:
                        frequency[ord(ltr)] = 1
        m.close()
    keys = list(frequency.keys())
    values = list(frequency.values())
    sorted_index = np.argsort(values)[::-1]
    sorted_freq = {keys[i]: values[i] for i in sorted_index}
    keys = convertKeys(sorted_freq)
    decode(encoded_message, decoded_message, keys)

def convertKeys(frequency):
    keys = []
    for ltr in frequency.keys():
        if ltr <= ord("e"):
            keys.append(ord("e") - ltr)
        else:
            keys.append(26 - (ltr - ord("e")))
    return keys

# encode("data/sent_decoded.txt", "data/received_encoded.txt", 1)

frequencyAnalysis("data/received_encoded.txt", "data/received_decoded.txt")

# decode("data/received_encoded.txt", "data/received_decoded.txt", 10)