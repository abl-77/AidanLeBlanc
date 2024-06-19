import tkinter as tk

class SimpleTypingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Test")
        
        with open("data/sample.txt", "r") as sample:
            self.sample_text = sample.read().strip() + " "
        self.max_line = 60
        self.lines = []
        while (len(self.sample_text) > self.max_line):
            split_index = self.max_line - 1
            while (self.sample_text[split_index] != " "):
                split_index -= 1
            self.lines.append(self.sample_text[:split_index + 1])
            self.sample_text = self.sample_text[split_index + 1:]

        self.lines.append(self.sample_text)

        self.typed_text = ""
        self.current_line = 0
        
        self.canvas = tk.Canvas(self.root, width=1250, height=1000, bg="white")
        self.canvas.pack(pady=20)
        
        self.canvas.bind("<KeyRelease>", self.on_key_release)
        self.canvas.focus_set()

        self.root.update_idletasks()
        
        self.update_canvas()
        
    def update_canvas(self):
        self.canvas.delete("all")

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Calculate the center position
        x_center = 10
        y_center = canvas_height / 2

        split_point = 0

        if len(self.typed_text) > len(self.lines[self.current_line]):
            self.typed_text = self.typed_text[:len(self.lines[self.current_line])]

        for i in range(0,len(self.typed_text)):
            if self.typed_text[i] != self.lines[self.current_line][i]:
                break
            split_point += 1
        
        self.canvas.create_text(x_center, y_center, anchor='w', text=self.lines[self.current_line][:split_point], font=('Helvetita', 45), fill="green")

        correct_bbox = self.canvas.bbox("all")
        correct_width = correct_bbox[2] - correct_bbox[0] if correct_bbox else 0


        self.canvas.create_text(x_center + correct_width, y_center, anchor='w', text=self.lines[self.current_line][split_point:len(self.typed_text)], font=('Helvetita', 45), fill="red")

        incorrect_bbox = self.canvas.bbox("all")
        incorrect_width = incorrect_bbox[2] - incorrect_bbox[0] if incorrect_bbox else 0

        self.canvas.create_line(x_center + incorrect_width, y_center - 20, x_center + incorrect_width, y_center + 20, fill="black", width=5)

        self.canvas.create_text(x_center + incorrect_width, y_center, anchor='w', text=self.lines[self.current_line][len(self.typed_text):], font=('Helvetita', 45), fill="black")

        if (self.current_line > 0):
            self.canvas.create_text(x_center, y_center - 75, anchor='w', text=self.lines[self.current_line - 1], font=('Helvetita', 45), fill="grey")
        
        if (self.current_line < len(self.lines) - 1):
            self.canvas.create_text(x_center, y_center + 75, anchor='w', text=self.lines[self.current_line + 1], font=('Helvetita', 45), fill="grey")
        
    def on_key_release(self, event):
        if event.keysym == "BackSpace":
            self.typed_text = self.typed_text[:-1]
        elif event.keysym == "Return":
            self.typed_text += "\n"
        elif len(event.char) == 1:
            self.typed_text += event.char
        
        self.update_canvas()

        if self.typed_text == self.lines[self.current_line]:
            self.canvas.delete("all")

            self.current_line += 1
            if self.current_line >= len(self.lines):
                self.current_line = 0
            self.typed_text = ""

            self.update_canvas()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleTypingApp(root)
    root.mainloop()