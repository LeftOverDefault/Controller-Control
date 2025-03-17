import pygame
import threading
import tkinter as tk

# Initialize Pygame for controller input
pygame.init()
pygame.joystick.init()

# Get the first controller
joystick = pygame.joystick.Joystick(0)

# Cursor position variables
cursor_x, cursor_y = 500, 500

# Tkinter overlay window for a second cursor
root = tk.Tk()
root.overrideredirect(True)
root.attributes('-topmost', True)
canvas = tk.Canvas(root, width=20, height=20, bg='white', highlightthickness=0)
canvas.create_oval(2, 2, 18, 18, fill='red')
canvas.pack()

def update_cursor():
    """Update the virtual cursor position"""
    global cursor_x, cursor_y
    while True:
        pygame.event.pump()
        x_axis = x_axis = apply_deadzone(joystick.get_axis(0))  # Left stick X
        y_axis = y_axis = apply_deadzone(joystick.get_axis(1))  # Left stick Y

        print(x_axis, y_axis)
        
        cursor_x += x_axis * 0.6
        cursor_y += y_axis * 0.6
        
        root.geometry(f"20x20+{int(cursor_x)}+{int(cursor_y)}")

threading.Thread(target=update_cursor, daemon=True).start()
root.mainloop()
