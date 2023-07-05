import evdev

def find_ds4_controller():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if "Wireless Controller" in device.name:
            return device
    return None

def handle_event(event):
    if event.type == evdev.ecodes.EV_KEY:
        key_event = evdev.categorize(event)
        if key_event.keystate == 1:  # Key press event
            print("Button Pressed:", key_event.keycode)
        elif key_event.keystate == 0:  # Key release event
            print("Button Released:", key_event.keycode)
    elif event.type == evdev.ecodes.EV_ABS:
        if event.code == evdev.ecodes.ABS_X:
            print("Left Stick X-axis:", event.value)
        elif event.code == evdev.ecodes.ABS_Y:
            print("Left Stick Y-axis:", event.value)

# Find the DS4 controller
ds4 = find_ds4_controller()

if ds4 is not None:
    print("DS4 controller found:", ds4.name)

    # Create an event device for the DS4 controller
    device = evdev.InputDevice(ds4.path)

    # Read events from the DS4 controller
    for event in device.read_loop():
        handle_event(event)
else:
    print("DS4 controller not found.")
