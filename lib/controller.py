import pygame
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class Controller:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            joystick.init()

        self._BUTTON_MAPPINGS = {
            0: "X",
            1: "CIRCLE",
            2: "SQUARE",
            3: "TRIANGLE",
            4: "SHARE",
            5: "PS",
            6: "OPTIONS",
            7: "L3",
            8: "R3",
            9: "L1",
            10: "R1",
            11: "UP",
            12: "DOWN",
            13: "LEFT",
            14: "RIGHT",
            15: "TOUCHPAD",
        }

        self._JOYSTICK_MAPPINGS ={
            0: "LEFT_STICK_X",
            1: "LEFT_STICK_Y",
            2: "RIGHT_STICK_X",
            3: "RIGHT_STICK_Y",
            4: "L2",
            5: "R2",
        }

        self._BUTTONS = {button_number: 0 for button_number in range(len(self._BUTTON_MAPPINGS))}
        self._ANALOG_STICKS = {axis: (0.0 if axis < 4 else -1.0) for axis in range(len(self._JOYSTICK_MAPPINGS))}

        self._DEADZONE = 0.2
    
    def updateState(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                axis = event.axis
                value = event.value
                if axis in range(4):
                    if value < self._DEADZONE and value > -self._DEADZONE:
                        value = 0.0
                self._ANALOG_STICKS[axis] = round(value, 3)
            elif event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                self._BUTTONS[button] = 1
            elif event.type == pygame.JOYBUTTONUP:
                button = event.button
                self._BUTTONS[button] = 0    

    def getValues(self):
        values = {}
        for i in range(len(self._JOYSTICK_MAPPINGS)):
            values[self._JOYSTICK_MAPPINGS[i]] = self._ANALOG_STICKS[i]
        for i in range(len(self._BUTTON_MAPPINGS)):
            values[self._BUTTON_MAPPINGS[i]] = self._BUTTONS[i]
        return values
    
    def setDeadzone(self, deadzone: float):
        self._DEADZONE = deadzone