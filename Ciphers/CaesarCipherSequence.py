def decode(encoded_message, decoded_message, key_seq):
    with open(encoded_message, "r") as m:
        msg = ""
        key_index = 0
        for line in m:
            key_index = 0
            for ltr in line:
                if ord(ltr) >= 97 and ord(ltr) <= 122:
                    msg += (chr(97 + ((ord(ltr) + key_seq[key_index] - 97) % 26)))
                    key_index = (key_index + 1) % len(key_seq)
                elif ord(ltr) >= 65 and ord(ltr) <= 90:
                    msg += (chr(65 + ((ord(ltr) + key_seq[key_index] - 65) % 26)))
                    key_index = (key_index + 1) % len(key_seq)
                else:
                    msg += ltr
    
    with open(decoded_message, "w") as d:
            d.write(msg)
            d.close()
            
def encode(decoded_message, encoded_message, key_seq):
    with open(decoded_message, "r") as m:
        msg = ""
        key_index = 0
        for line in m:
            key_index = 0
            for ltr in line:
                if ord(ltr) >= 97 and ord(ltr) <= 122:
                    msg += (chr(97 + ((ord(ltr) - key_seq[key_index] - 97) % 26)))
                    key_index = (key_index + 1) % len(key_seq)
                elif ord(ltr) >= 65 and ord(ltr) <= 90:
                    msg += (chr(65 + ((ord(ltr) - key_seq[key_index] - 65) % 26)))
                    key_index = (key_index + 1) % len(key_seq)
                else:
                    msg += ltr
    
    with open(encoded_message, "w") as d:
            d.write(msg)
            d.close()
            
def create_key_seq(word, key):
    key_seq = []
    
    for ltr in word:
        key_seq.append(key + ord(word[0]) - ord(ltr))
    
    return key_seq

key_seq = create_key_seq("HUZZAH", 10)
print(key_seq)
encode("data/sent_decoded.txt", "data/sent_encoded.txt", key_seq)
decode("data/sent_encoded.txt", "data/received_encoded.txt", key_seq)

key_seq = create_key_seq("boom", 25)
# decode("data/received_encoded.txt", "data/received_decoded.txt", key_seq)