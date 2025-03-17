import pygame
import time
import keyboard
import win32api, win32con, win32gui

pygame.init()


# Function to press a key
def press_key(key_code):
    win32api.keybd_event(key_code, 0, 0, 0)
    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)



class Controller:
    def __init__(self, player: int):
        # Sensitivity factor to reduce jitter
        self.SENSITIVITY = 10
        self.SCROLL_SENSITIVITY = 20
        self.EXPONENT_SCROLL_SENSITIVITY = 2

        # Deadzone to prevent jitter
        self.DEADZONE = 0.1

        self.joystick = pygame.joystick.Joystick(player)
    

    def exponent_scroll(self):
        # Left joystick (mouse movement)
        x_axis = round(self.joystick.get_axis(0), 1)
        y_axis = round(self.joystick.get_axis(1), 1)

        if abs(x_axis) > self.DEADZONE:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(x_axis * self.SENSITIVITY), 0, 0, 0)

        if abs(y_axis) > self.DEADZONE:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, int(y_axis * self.SENSITIVITY), 0, 0)

        # Right joystick (scrolling)
        right_x_axis = round(self.joystick.get_axis(2), 3)
        right_y_axis = round(self.joystick.get_axis(3), 3)

        direction_y = -1 if right_y_axis > 0 else 1
        direction_x = 1 if right_x_axis > 0 else -1

        # Combine vertical and horizontal scrolling
        if abs(right_x_axis) > self.DEADZONE or abs(right_y_axis) > self.DEADZONE:
            win32api.mouse_event(
                win32con.MOUSEEVENTF_WHEEL,
                0,
                0,
                direction_y * int(self.EXPONENT_SCROLL_SENSITIVITY ** abs(right_y_axis * 5)),
                0
            )
            win32api.mouse_event(
                win32con.MOUSEEVENTF_HWHEEL,
                0,
                0,
                direction_x * int(self.EXPONENT_SCROLL_SENSITIVITY ** abs(right_x_axis * 5)),
                0
            )


    def linear_scroll(self):
        # Left joystick (mouse movement)
        x_axis = round(self.joystick.get_axis(0), 1)
        y_axis = round(self.joystick.get_axis(1), 1)

        if abs(x_axis) > self.DEADZONE:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(x_axis * self.SENSITIVITY), 0, 0, 0)

        if abs(y_axis) > self.DEADZONE:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, int(y_axis * self.SENSITIVITY), 0, 0)

        # Right joystick (scrolling)
        right_x_axis = round(self.joystick.get_axis(2), 3)
        right_y_axis = round(self.joystick.get_axis(3), 3)

        # Combine vertical and horizontal scrolling
        if abs(right_x_axis) > self.DEADZONE or abs(right_y_axis) > self.DEADZONE:
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, int(right_y_axis * self.SCROLL_SENSITIVITY), 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_HWHEEL, 0, 0, int(right_x_axis * self.SCROLL_SENSITIVITY), 0)


class Main:
    def __init__(self):
        self.controllers = []

        self.clock = pygame.time.Clock()

        self.running = True
        self.held_keys = {"up": False, "down": False, "left": False, "right": False}
        self.last_press_time = {"up": 0, "down": 0, "left": 0, "right": 0}
        self.PRESS_DELAY = 0.2  # Delay between repeated key presses (in seconds)
        self.REPEAT_RATE = 0.05

        # Run detection at start
        self.detect_joysticks()

        # List of apps to ignore joystick input for
        self.BLACKLISTED_APPS = ["Steam Big Picture Mode"]


    # Function to get the active window title
    def get_active_window_title(self):
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)


    def detect_joysticks(self):
        self.controllers = [Controller(i) for i in range(pygame.joystick.get_count())]
        # self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for controller in self.controllers:
            print(f"Detected joystick: {controller.joystick.get_name()}")


    def run(self):
        while self.running:
            self.clock.tick(60)

            # Get active window
            active_window = self.get_active_window_title()

            # Check if a blacklisted app is active
            if any(app.lower() in active_window.lower() for app in self.BLACKLISTED_APPS):
                continue  # Skip joystick input

            # Event handling for buttons and quitting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Handle controller connection
                elif event.type == pygame.JOYDEVICEADDED:
                    print("Controller connected!")
                    self.detect_joysticks()

                # Handle controller disconnection
                elif event.type == pygame.JOYDEVICEREMOVED:
                    print("Controller disconnected!")
                    self.detect_joysticks()

                # Handle button presses
                elif event.type == pygame.JOYBUTTONDOWN:
                    joystick_id = event.instance_id
                    if event.button == 0:
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    elif event.button == 1:
                        keyboard.press_and_release("esc")
                    print(f"Joystick {joystick_id} - Button {event.button} pressed")

                elif event.type == pygame.JOYBUTTONUP:
                    joystick_id = event.instance_id
                    if event.button == 0:
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                    print(f"Joystick {joystick_id} - Button {event.button} released")
            
            # Poll D-PAD state every frame
            current_time = time.time()
            for controller in self.controllers:
                hat_x, hat_y = controller.joystick.get_hat(0)

                for direction, key, axis_value in [("up", win32con.VK_UP, hat_y == 1),
                                           ("down", win32con.VK_DOWN, hat_y == -1),
                                           ("left", win32con.VK_LEFT, hat_x == -1),
                                           ("right", win32con.VK_RIGHT, hat_x == 1)]:
                    if axis_value:
                        if not self.held_keys[direction]:
                            press_key(key)
                            self.held_keys[direction] = True
                            self.last_press_time[direction] = current_time
                        elif current_time - self.last_press_time[direction] > self.PRESS_DELAY:
                            if current_time - self.last_press_time[direction] > self.REPEAT_RATE:
                                press_key(key)
                                self.last_press_time[direction] = current_time
                    else:
                        self.held_keys[direction] = False

            for controller in self.controllers:
                controller.exponent_scroll()


if __name__ == "__main__":
    main = Main()
    main.run()
