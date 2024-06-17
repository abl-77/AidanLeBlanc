def decode(encoded_message, decoded_message, key):
    msg = ""
    with open(encoded_message, "r") as m:
        msg = m.read().replace(" ", "")
    length = len(msg)
    width, height = determineDimensions(length)
    grid = [ [0] * width for i in range(height)]

    x, y = width - 1, 0
    dir = "L"
    while len(msg) > 0:
        grid[y][x] = msg[0]
        msg = msg[1:]

        if dir == "L":
            if x == 0 or grid[y][x - 1] != 0:
                dir = "D"
                y += 1
            else:
                x -= 1
        elif dir == "D":
            if y == height - 1 or grid[y + 1][x] != 0:
                dir = "R"
                x += 1
            else:
                y += 1
        elif dir == "R":
            if x == width - 1 or grid[y][x + 1] != 0:
                dir = "U"
                y -= 1
            else:
                x += 1
        else:
            if y == 0 or grid[y - 1][x] != 0:
                dir = "L"
                x -= 1
            else:
                y -= 1

    decoded = ""
    for col in range(0, width):
        for row in range(0, height):
            decoded += grid[row][col]

    with open(decoded_message, "w") as r:
        r.write(decoded)
        r.close()


def encode(decoded_message, encoded_message, key):
    msg = ""
    with open(decoded_message, "r") as m:
        for line in m:
            msg += line.replace(" ", "")
        m.close()
    msg = msg.upper()
    length = len(msg)
    width, height = determineDimensions(length)
    grid = [ [0] * width for i in range(height)]

    for col in range(0, width):
        for row in range(0, height):
            if len(msg) > 0:
                grid[row][col] = [msg[0], False]
                msg = msg[1:]

    encoded = ""
    x, y = width - 1, 0
    dir = "L"
    count = 0
    numSpaces = 0
    while len(encoded) < length + numSpaces:
        encoded += grid[y][x][0]
        grid[y][x][1] = True
        count += 1

        if count == 5:
            encoded += " "
            count = 0
            numSpaces += 1
        
        # Move direction
        if dir == "L":
            if x == 0 or grid[y][x - 1][1] == True:
                dir = "D"
                y += 1
            else:
                x -= 1
        elif dir == "D":
            if y == height - 1 or grid[y + 1][x][1] == True:
                dir = "R"
                x += 1
            else:
                y += 1
        elif dir == "R":
            if x == width - 1 or grid[y][x + 1][1] == True:
                dir = "U"
                y -= 1
            else:
                x += 1
        else:
            if y == 0 or grid[y - 1][x][1] == True:
                dir = "L"
                x -= 1
            else:
                y -= 1

    with open(encoded_message, "w") as r:
        r.write(encoded)
        r.close()

def determineDimensions(len):
    w, h = len, 1
    while w > 3 * h:
        w = w // 2 + w % 2
        h *= 2
    return w, h

# encode("data/tran_decoded.txt", "data/tran_encoded.txt", 1)

decode("data/tran_encoded.txt", "data/tran_decoded.txt", 1)