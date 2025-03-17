#======================#
#  CONTROLLER-CONTROL  #
#======================#
#
#  Description: This application allows you to control windows 10/11 with a game controller.
#  Version: 0.1.0
#  Author: Michael Goddard (LeftOverDefault)
#  License: MIT
#  GitHub: https://github.com/LeftOverDefault/controller-control


#===========#
#  IMPORTS  #
#===========#
from src.utils.imports import *

from src.controller import Controller

from src.func.get_active_window_title import get_active_window_title


#===========#
#  GLOBALS  #
#===========#

BLACKLISTED_APPS = ["Steam Big Picture Mode"]


class Main:
    def __init__(self) -> None:
        pygame.init()
        self.controllers = []
        self.clock = pygame.time.Clock()
        self.running = True

        pyautogui.FAILSAFE = False

        self.detect_joysticks()


    def detect_joysticks(self):
        """Detect all connected controllers, ignoring the Razer virtual controller."""
        self.controllers.clear()  # Clear existing list

        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick_name = joystick.get_name()

            # Ignore Razer virtual controllers
            if "Razer" in joystick_name or "Xbox 360" in joystick_name:
                print(f"Ignoring virtual controller: {joystick_name}")
                continue  # Skip adding it

            self.controllers.append(Controller(i))  # Add only real controllers

        for controller in self.controllers:
            print(f"Detected joystick: {controller.joystick.get_name()}")
    

    def handle_input(self):
        """Handle input for all controllers."""
        for controller in self.controllers:
            # We no longer call controller.run(), just handle button presses directly
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    # controller.handle_button_press(event)
                    pass


    def run(self) -> None:
        """Run the Pygame event loop in a separate thread."""
        while self.running:
            self.clock.tick(60)
            pygame.event.pump()  # Ensures controllers stay responsive

            # Get active window
            active_window = get_active_window_title()

            # Check if a blacklisted app is active
            if any(app.lower() in active_window.lower() for app in BLACKLISTED_APPS):
                continue  # Skip joystick input
                
            # Handle the input for each controller (button presses and cursor updates)
            self.handle_input()

            # Handle quitting events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.JOYDEVICEADDED:
                    print("Controller connected!")
                    self.detect_joysticks()

                elif event.type == pygame.JOYDEVICEREMOVED:
                    print("Controller disconnected!")
                    self.detect_joysticks()

                


if __name__ == "__main__":
    main = Main()

    # Start Pygame event loop in a separate thread
    pygame_thread = threading.Thread(target=main.run, daemon=True)
    pygame_thread.start()

    # Start each controller (Tkinter must be in the main thread!)
    for controller in main.controllers:
        controller.run()  # Tkinter's mainloop runs in the main thread

# class Main:
#     def __init__(self) -> None:
#         pygame.init()

#         # pyautogui.FAILSAFE = False
#         # pyautogui.moveTo(self.root.winfo_screenwidth(), self.root.winfo_screenheight() / 2)

#         self.controllers = []

#         self.clock = pygame.time.Clock()
#         self.fps = 60

#         self.running = True

#         self.detect_joysticks()


#     def detect_joysticks(self):
#         self.controllers = [Controller(i) for i in range(pygame.joystick.get_count())]
#         for controller in self.controllers:
#             print(f"Detected joystick: {controller.joystick.get_name()}")


#     def run(self) -> None:
#         while self.running:
#             self.clock.tick(60)

#             active_window = get_active_window_title()

#             if any(app.lower() in active_window.lower() for app in BLACKLISTED_APPS):
#                 continue  # Skip joystick input

#             try:
#                 self.controllers.pop(len(self.controllers) - 1)  # Remove the last controller (it's a keyboard)
#             except IndexError:
#                 print("No keyboard detected")

#             # Event handling for buttons and quitting
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False

#                 # Handle controller connection
#                 elif event.type == pygame.JOYDEVICEADDED:
#                     print("Controller connected!")
#                     self.detect_joysticks()

#                 # Handle controller disconnection
#                 elif event.type == pygame.JOYDEVICEREMOVED:
#                     print("Controller disconnected!")
#                     self.detect_joysticks()
                


# if __name__ == "__main__":
#     main = Main()
#     for controller in main.controllers:
#         controller.run()
#     threading.Thread(target=main.run, daemon=True).start()
    


