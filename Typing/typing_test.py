import tkinter as tk
from text_generator import TextGenerator
import time
from text_processor import process_event

class TypingTest:
    def __init__(self, root):
        self.start = time.time()
        self.root = root
        self.root.title("Typing Test")
        
        self.max_line = 60

        self.keyboard = "qwerty"

        self.gen = TextGenerator("data/alice_in_wonderland.txt", 5)

        self.previous_line = ""
        self.current_line = self.gen.generate(self.max_line)
        self.current_line = self.current_line[:self.current_line.rindex(" ") + 1]
        self.next_line = self.gen.generate(self.max_line, self.current_line)
        self.next_line = self.next_line[:self.next_line.rindex(" ") + 1]
    
        self.typed_text = ""
        self.typed_tot = ""

        self.wpm = 0
        
        self.canvas = tk.Canvas(self.root, width=1250, height=1000, bg="white")
        self.canvas.pack(pady=20)
        
        self.canvas.bind("<KeyRelease>", self.on_key_release)
        self.canvas.focus_set()

        self.root.update_idletasks()
        
        self.update_canvas()
        
    def update_canvas(self):
        self.canvas.delete("all")

        canvas_height = self.canvas.winfo_height()
        
        # Calculate the center position
        x_center = 10
        y_center = canvas_height / 2

        split_point = 0

        for i in range(0,len(self.typed_text)):
            if self.typed_text[i] != self.current_line[i]:
                break
            split_point += 1
        
        self.canvas.create_text(x_center, y_center, anchor='w', text=self.current_line[:split_point], font=('Helvetita', 45), fill="green")

        correct_bbox = self.canvas.bbox("all")
        correct_width = correct_bbox[2] - correct_bbox[0] if correct_bbox else 0

        self.canvas.create_text(x_center + correct_width, y_center, anchor='w', text=self.typed_text[split_point:len(self.typed_text)].replace(" ", "_"), font=('Helvetita', 45), fill="red")

        incorrect_bbox = self.canvas.bbox("all")
        incorrect_width = incorrect_bbox[2] - incorrect_bbox[0] if incorrect_bbox else 0

        self.canvas.create_line(x_center + incorrect_width, y_center - 20, x_center + incorrect_width, y_center + 20, fill="black", width=5)

        self.canvas.create_text(x_center + incorrect_width, y_center, anchor='w', text=self.current_line[len(self.typed_text):], font=('Helvetita', 45), fill="black")

        self.canvas.create_text(x_center, y_center - 75, anchor='w', text=self.previous_line, font=('Helvetita', 45), fill="grey")
        
        self.canvas.create_text(x_center, y_center + 75, anchor='w', text=self.next_line, font=('Helvetita', 45), fill="grey")

        time_spent = time.time() - self.start

        self.wpm = int((len(self.typed_tot) / 5 / time_spent) * 60)
        self.canvas.create_text(10, 30, anchor='w', text=f"wpm = {self.wpm}", font=('Helvitita', 30), fill="blue")
        
    def on_key_release(self, event):
        result = process_event(event, self.keyboard)
        if result == -1:
            self.typed_text = self.typed_text[:-1]
            self.typed_tot = self.typed_tot[:-1]
        elif result:
            self.typed_text += result
            self.typed_tot += result
        
        if self.typed_text == self.current_line:
            self.canvas.delete("all")

            self.previous_line = self.current_line
            self.current_line = self.next_line
            self.next_line = self.gen.generate(self.max_line, self.current_line)
            self.next_line = self.next_line[:self.next_line.rindex(" ") + 1]
            self.typed_text = ""
            
        self.update_canvas()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTest(root)
    root.mainloop()