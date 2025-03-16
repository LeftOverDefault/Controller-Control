import pygame
import win32api, win32con

pygame.init()

# Initialize joysticks
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    joystick.init()
    print(f"Detected joystick: {joystick.get_name()}")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Sensitivity factor to reduce jitter
SENSITIVITY = 5

# Deadzone to prevent jitter
DEADZONE = 0.1

# Main loop
running = True
while running:
    clock.tick(60)

    # Event handling for buttons and quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle button presses
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            else:
                print(f"Button {event.button} pressed")

        elif event.type == pygame.JOYBUTTONUP:
            if event.button == 0:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            else:
                print(f"Button {event.button} released")

    # Poll joystick axis manually for continuous movement
    for joystick in joysticks:
        x_axis = round(joystick.get_axis(0), 2)
        y_axis = round(joystick.get_axis(1), 2)

        if abs(x_axis) > DEADZONE:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(x_axis * SENSITIVITY), 0, 0, 0)

        if abs(y_axis) > DEADZONE:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, int(y_axis * SENSITIVITY), 0, 0)

pygame.quit()
