import random

class TextGenerator:
    def __init__(self, text, window):
        with open(text, "r") as t:
            self.text = t.read().replace("\n", " ")
        self.window = window

    def generate(self, length, seed=""):
        if seed == "":
            start = random.randint(0, len(self.text) - self.window)
            seed = self.text[start: start + self.window]
        else:
            seed = seed[-self.window:]

        result = seed

        for i in range(0, length):
            copy = self.text
            chars = []

            index = 0
            while(index != -1):
                try:
                    index = copy.index(seed)
                except:
                    index = -1

                if index >= 0 and len(copy) > index + self.window:
                    copy = copy[index + self.window:]
                    chars.append(copy[0])

            choice = chars[random.randint(0, len(chars) - 1)]
            result += choice
            seed += choice

            if len(seed) > self.window:
                seed = seed[1:]

        if result[self.window] == " ":
            return result[self.window + 1]
        return result[self.window:]
        
if __name__ == "__main__":
    gen = TextGenerator("data/alice_in_wonderland.txt", 2)
    print(gen.generate(10))
