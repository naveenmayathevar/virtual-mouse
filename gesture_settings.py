import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk, ImageSequence

class GestureSettings:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gesture Control Settings")

        bold_font = font.Font(weight="bold")

        # Instruction labels (clickable)
        tk.Label(self.root, text="📹 Before starting:", font=bold_font).pack()

        self.create_instruction("Press Q to end", None)
        self.create_instruction("Move your hand to control mouse", "media/03baf8cfb1d8bd8a8163b5c0d251f257.gif")
        self.create_instruction("Pinch to Left Click", "media/zoom-fingers.gif")
        self.create_instruction("Fist to Right Click", "media/K4r2.gif")
        

        # GIF display area
        self.gif_label = tk.Label(self.root)
        self.gif_label.pack(pady=10)
        self.gif_frames = []
        self.gif_running = False

        # Agreement checkbox
        self.agree_var = tk.BooleanVar()
        self.agree_checkbox = tk.Checkbutton(self.root, text="I understand the controls", variable=self.agree_var, command=self.toggle_start_button)
        self.agree_checkbox.pack()

        # Start button
        self.start_button = tk.Button(self.root, text="Start App", command=self.start_app, state="disabled")
        self.start_button.pack(pady=10)

        # Gesture toggles
        self.move_enabled = tk.BooleanVar(value=True)
        self.click_enabled = tk.BooleanVar(value=True)
        self.right_click_enabled = tk.BooleanVar(value=True)

        self.move_toggle = tk.Checkbutton(self.root, text="Move Mouse", variable=self.move_enabled)
        self.click_toggle = tk.Checkbutton(self.root, text="Left Click", variable=self.click_enabled)
        self.right_click_toggle = tk.Checkbutton(self.root, text="Right Click", variable=self.right_click_enabled)

        self.move_toggle.pack()
        self.click_toggle.pack()
        self.right_click_toggle.pack()

        self.should_start = False

    def create_instruction(self, text, gif_path):
        label = tk.Label(self.root, text="- " + text, cursor="hand2", fg="blue")
        label.pack()
        if gif_path:
            label.bind("<Button-1>", lambda e, path=gif_path: self.show_gif(path))

    def show_gif(self, path):
        if self.gif_running:
            self.root.after_cancel(self.gif_running)
        gif = Image.open(path)
        self.gif_frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(gif)]
        self.play_gif(0)

    def play_gif(self, index):
        if not self.gif_frames:
            return
        self.gif_label.configure(image=self.gif_frames[index])
        self.gif_label.image = self.gif_frames[index]
        self.gif_running = self.root.after(100, self.play_gif, (index + 1) % len(self.gif_frames))

    def toggle_start_button(self):
        self.start_button.config(state="normal" if self.agree_var.get() else "disabled")

    def start_app(self):
        self.should_start = True
        self.root.quit()

    def start_ui(self):
        self.root.mainloop()
