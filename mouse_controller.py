import pyautogui
import numpy as np

class MouseController:
    def __init__(self, screen_width, screen_height, smoothening=5):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.smoothening = smoothening
        self.prev_x, self.prev_y = 0, 0

    def move_cursor(self, x, y, frame_width, frame_height):
        # Map camera coords to screen coords
        screen_x = np.interp(x, (100, frame_width - 100), (0, self.screen_width))
        screen_y = np.interp(y, (100, frame_height - 100), (0, self.screen_height))

        # Smooth the movement
        curr_x = self.prev_x + (screen_x - self.prev_x) / self.smoothening
        curr_y = self.prev_y + (screen_y - self.prev_y) / self.smoothening

        pyautogui.moveTo(curr_x, curr_y)
        self.prev_x, self.prev_y = curr_x, curr_y
        
    def right_click(self):
        pyautogui.rightClick()

    def click(self):
        pyautogui.click()
