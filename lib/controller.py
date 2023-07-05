from ds4drv import DS4drv
import time

def handle_event(event):
    if event.event_type == "button_press":
        print("Button Pressed:", event.button)
    elif event.event_type == "button_release":
        print("Button Released:", event.button)
    elif event.event_type == "axis_motion":
        print("Axis Motion:", event.axis, event.value)

def search_for_controller():
    while True:
        try:
            ds4 = DS4drv(callback=handle_event)
            ds4.start()
            print("DS4 controller found. Listening for events...")
            while True:
                time.sleep(1)
        except:
            print("DS4 controller not found. Retrying in 5 seconds...")
            time.sleep(5)

# Start the search loop
search_for_controller()