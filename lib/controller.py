from ds4drv.device import DS4Device
import time
import threading
from queue import Queue

RATE_LIMIT_PERIOD = 0.1  # Rate limit period in seconds

def handle_event(event, result_queue):
    if event['type'] == 'button':
        button_name = event['name']
        if event['value']:
            result_queue.put("Button Pressed: " + button_name)
        else:
            result_queue.put("Button Released: " + button_name)
    elif event['type'] == 'axis':
        axis_name = event['name']
        axis_value = event['value']
        result_queue.put(f"{axis_name}: {axis_value}")

def event_handling_thread(ds4dev, result_queue):
    for event in ds4dev.events():
        handle_event(event, result_queue)

# Create a DS4Device object
ds4dev = DS4Device()

# Find the DS4 controller
ds4dev.find()

if ds4dev.connected:
    print("DS4 controller found:", ds4dev.name)

    # Create a result queue for storing the event handling results
    result_queue = Queue()

    # Create and start the event handling thread
    event_thread = threading.Thread(target=event_handling_thread, args=(ds4dev, result_queue))
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
