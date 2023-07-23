from evdev import InputDevice, ecodes

DEADZONE = 10

def main():
    try:
        device = InputDevice('/dev/input/event25')
        print(f"Using device: {device.name}")

        for event in device.read_loop():
            if event.type == ecodes.EV_KEY or event.type == ecodes.EV_ABS:
                if event.code in [ecodes.ABS_X, ecodes.ABS_Y, ecodes.ABS_Z, ecodes.ABS_RX]:
                    if event.value > (127 + DEADZONE) or event.value < (127 - DEADZONE):
                        print(f"{event.code}, {event.value}")
                elif event.code in [ecodes.ABS_WHEEL, ecodes.ABS_RZ]:
                    print(f"{event.code}, {event.value}")
                else:
                    print(f"{event.code}, {event.value}")

    except FileNotFoundError:
        print("E Controller not found")
        return 1

    return 0

if __name__ == "__main__":
    main()