import evdev

def find_ds4_controller():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if "Wireless Controller" in device.name:
            return device
    return None

def handle_event(event):
    print(event)

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
