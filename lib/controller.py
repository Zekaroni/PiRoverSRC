import evdev
import time
import threading
from queue import Queue

RATE_LIMIT_PERIOD = 0.1  # Rate limit period in seconds

def find_ds4_controller():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if "Wireless Controller" in device.name:
            return device
    return None

def handle_event(event, result_queue):
    if event.type == evdev.ecodes.EV_KEY:
        key_event = evdev.categorize(event)
        if key_event.keystate == 1:  # Key press event
            result_queue.put("Button Pressed: " + key_event.keycode)
        elif key_event.keystate == 0:  # Key release event
            result_queue.put("Button Released: " + key_event.keycode)
    # elif event.type == evdev.ecodes.EV_ABS:
    #     if event.code == evdev.ecodes.ABS_X:
    #         result_queue.put("Left Stick X-axis: " + str(event.value))
    #     elif event.code == evdev.ecodes.ABS_Y:
    #         result_queue.put("Left Stick Y-axis: " + str(event.value))
    #     elif event.code == evdev.ecodes.ABS_RX:
    #         result_queue.put("Right Stick X-axis: " + str(event.value))
    #     elif event.code == evdev.ecodes.ABS_RY:
    #         result_queue.put("Right Stick Y-axis: " + str(event.value))
    #     elif event.code == evdev.ecodes.ABS_Z:  # Left trigger
    #         result_queue.put("Left Trigger: " + str(event.value))
    #     elif event.code == evdev.ecodes.ABS_RZ:  # Right trigger
    #         result_queue.put("Right Trigger: " + str(event.value))

def event_handling_thread(device, result_queue):
    for event in device.read_loop():
        handle_event(event, result_queue)

# Find the DS4 controller
ds4 = find_ds4_controller()

if ds4 is not None:
    print("DS4 controller found:", ds4.name)

    # Create an event device for the DS4 controller
    device = evdev.InputDevice(ds4.path)

    # Create a result queue for storing the event handling results
    result_queue = Queue()

    # Create and start the event handling thread
    event_thread = threading.Thread(target=event_handling_thread, args=(device, result_queue))
    event_thread.daemon = True  # Allow the program to exit even if this thread is running
    event_thread.start()

    # Rate-limiting loop
    while True:
        # Perform other non-blocking tasks here

        # Check if there are results in the queue
        while not result_queue.empty():
            result = result_queue.get()
            print("Received result:", result)

        # Sleep for the rate limit period
        time.sleep(RATE_LIMIT_PERIOD)

else:
    print("DS4 controller not found.")
