from lib.controller import Controller
from lib.piSerial import SerialOutput
# from lib.piWrapper import Board # Doesn't work on Windows, commented out for testing

from time import sleep

controller = Controller()
arduinoInput = SerialOutput()
# piBoard = Board()

while 1:
    print(controller.getValues())
    sleep(0.1)