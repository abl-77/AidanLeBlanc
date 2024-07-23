def process_event(event, keyboard):
    if keyboard == "qwerty":
        if event.keysym == "BackSpace":
            return -1
        elif event.keysym == "Return":
            return "\n"
        elif len(event.char) == 1:
            return event.char