import ctypes.wintypes
from src.utils.imports import *

from src.func.apply_deadzone import apply_deadzone

import random


class Controller:
    def __init__(self, player) -> None:
        self.joystick = pygame.joystick.Joystick(player)

        self.cursor = tk.Tk()
        self.cursor.withdraw()  # Hide until it's ready
        self.cursor.overrideredirect(True)
        self.cursor.attributes('-topmost', True)
        self.cursor.attributes('-transparentcolor', 'white')

        self.canvas = tk.Canvas(self.cursor, width=32, height=32, bg="white", highlightthickness=0)
        self.canvas.create_oval(7, 7, 25, 25, fill='red', outline='black')
        self.canvas.pack()

        # # Load system cursor image
        # self.cursor_image = self.load_cursor_image()

        # # Create transparent canvas
        # self.canvas = tk.Canvas(self.cursor, width=32, height=32, highlightthickness=0, bg='white')
        # self.canvas.pack()

        # # Draw cursor
        # self.cursor_icon = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.cursor_image)

        # # Draw player number
        # self.player_number = self.canvas.create_text(25, 25, text=str(player + 1), fill="red", font=("Arial", 12, "bold"))

        self.cursor_x = 500
        self.cursor_y = 500
        self.running = True

        self.cursor.after(10, self.update_cursor)  # Start updating cursor
        self.cursor.deiconify()  # Show the cursor window

        self.mouse = MouseController()


    def update_cursor(self):
        """Update cursor position without blocking Tkinter."""
        if not self.running:
            return
        
        pygame.event.pump()  # Prevent controller freeze

        x_axis = apply_deadzone(self.joystick.get_axis(0))  # Left stick X
        y_axis = apply_deadzone(self.joystick.get_axis(1))  # Left stick Y

        self.cursor_x += x_axis * 5  # Adjust speed if needed
        self.cursor_y += y_axis * 5

        self.cursor.geometry(f"32x32+{int(self.cursor_x)}+{int(self.cursor_y)}")

        self.cursor.after(10, self.update_cursor)  # Re-run this function after 10ms
    

    # def handle_button_press(self, event):
    #     """Handle button presses and simulate actions at the controller cursor position."""
    #     joystick_id = event.instance_id

    #     if event.button == 0:  # Left Button
    #         self.simulate_mouse_event(win32con.MOUSEEVENTF_LEFTDOWN)
    #         print(f"Joystick {joystick_id} - Left button pressed at {self.cursor_x}, {self.cursor_y}")
    #     elif event.button == 1:  # Escape button or another key (custom logic)
    #         self.simulate_key_press("esc")
    #         print(f"Joystick {joystick_id} - Button {event.button} pressed")

    # def simulate_mouse_event(self, event_type):
    #     """Simulate a mouse event at the current cursor position without moving the system cursor."""
        
    #     # Hide the cursor (with pyautogui)
    #     self.hide_cursor()

    #     # Simulate the mouse event at the controller cursor position
    #     pyautogui.click(self.cursor_x, self.cursor_y)  # Click at the controller cursor's position
    #     time.sleep(0.1)  # Small delay to ensure the click is registered
        
    #     # Restore the cursor back to its original position
    #     self.restore_cursor()

    # def hide_cursor(self):
    #     """Hide the mouse cursor (set position off-screen)."""
    #     # Move the system cursor far off-screen to hide it
    #     win32api.SetCursorPos((-100, -100))  # Move cursor off-screen temporarily

    # def restore_cursor(self):
    #     """Restore the system cursor back to the last known position (or any default position)."""
    #     # You could store the original cursor position and restore it here if desired
    #     # For simplicity, restore to the center of the screen or a known position
    #     win32api.SetCursorPos((int(self.cursor_x), int(self.cursor_y)))

    # def simulate_key_press(self, key):
    #     """Simulate a key press event."""
    #     keyboard.press(key)  # Simulating the 'esc' key press
    #     time.sleep(0.1)  # Small delay to ensure the key press is registered


    def run(self) -> None:
        """Run Tkinter's main loop in the main thread."""
        self.cursor.mainloop()
