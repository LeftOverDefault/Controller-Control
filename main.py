import pygame
import win32api, win32con, win32gui

pygame.init()

# Initialize joysticks
# joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
joysticks = []

def detect_joysticks():
    global joysticks
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        print(f"Detected joystick: {joystick.get_name()}")

# Run detection at start
detect_joysticks()

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Sensitivity factor to reduce jitter
SENSITIVITY = 8
SCROLL_SENSITIVITY = 20
# SCROLL_SENSITIVITY = 2

# Deadzone to prevent jitter
DEADZONE = 0.1

# List of apps to ignore joystick input for
BLACKLISTED_APPS = ["Steam Big Picture Mode", "Steam"]

# Function to get the active window title
def get_active_window_title():
    hwnd = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(hwnd)


# Main loop
running = True
while running:
    clock.tick(60)

    # Get active window
    active_window = get_active_window_title()

    # Check if a blacklisted app is active
    if any(app.lower() in active_window.lower() for app in BLACKLISTED_APPS):
        continue  # Skip joystick input

    # Event handling for buttons and quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle button presses
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            if event.button == 1:
                print(f"Button {event.button} pressed")
            if event.button == 2:
                print(f"Button {event.button} pressed")
            if event.button == 3:
                print(f"Button {event.button} pressed")
            if event.button == 4:
                print(f"Button {event.button} pressed")
            if event.button == 5:
                print(f"Button {event.button} pressed")
            if event.button == 6:
                print(f"Button {event.button} pressed")
            if event.button == 7:
                print(f"Button {event.button} pressed")
            if event.button == 8:
                print(f"Button {event.button} pressed")
            if event.button == 9:
                print(f"Button {event.button} pressed")
            if event.button == 10:
                print(f"Button {event.button} pressed")
            else:
                print(f"Button {event.button} pressed")

        elif event.type == pygame.JOYBUTTONUP:
            if event.button == 0:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            else:
                print(f"Button {event.button} released")

        # Handle controller connection
        elif event.type == pygame.JOYDEVICEADDED:
            print("Controller connected!")
            detect_joysticks()

        # Handle controller disconnection
        elif event.type == pygame.JOYDEVICEREMOVED:
            print("Controller disconnected!")
            detect_joysticks()

    # Poll joystick axis manually for continuous movement
    for joystick in joysticks:
        # Left joystick (mouse movement)
        x_axis = round(joystick.get_axis(0), 1)
        y_axis = round(joystick.get_axis(1), 1)

        if abs(x_axis) > DEADZONE:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(x_axis * SENSITIVITY), 0, 0, 0)

        if abs(y_axis) > DEADZONE:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, int(y_axis * SENSITIVITY), 0, 0)

        # Right joystick (scrolling)
        right_x_axis = round(joystick.get_axis(2), 3)
        right_y_axis = round(joystick.get_axis(3), 3)

        direction_y = -1 if right_y_axis > 0 else 1
        direction_x = 1 if right_x_axis > 0 else -1

        # Combine vertical and horizontal scrolling
        if abs(right_x_axis) > DEADZONE or abs(right_y_axis) > DEADZONE:
            win32api.mouse_event(
                win32con.MOUSEEVENTF_WHEEL, 
                0,
                0,
                int(-right_y_axis * SCROLL_SENSITIVITY), 
                # direction_y * int(SCROLL_SENSITIVITY ** abs(right_y_axis * 5)),
                0
            )
            win32api.mouse_event(
                win32con.MOUSEEVENTF_HWHEEL, 
                0, 
                0, 
                int(right_x_axis * SCROLL_SENSITIVITY), 
                # direction_x * int(SCROLL_SENSITIVITY ** abs(right_x_axis * 5)),
                0
            )

pygame.quit()
