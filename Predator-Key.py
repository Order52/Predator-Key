#!/usr/bin/env python3
import evdev
import subprocess
import sys
import time

# ========== CONFIGURATION ==========
# Change this to whatever you want your Predator key to do!
# Examples:
#   "firefox"                           # Open Firefox
#   "code"                              # Open VS Code  
#   "kitty"                             # Open Kitty terminal
#   "/home/user/my-script.sh"           # Run custom script
#   "gnome-calculator"                  # Open calculator
#   "steam"                             # Open Steam
#   "discord"                           # Open Discord
#   "notify-send 'Hello' 'World!'"      # Show notification only

PREDATOR_KEY_COMMAND = "notify-send 'Hello' 'Linux!'"

# Optional: Add multiple commands (all will run when key is pressed)
# Leave empty [] if you only want the single command above
EXTRA_COMMANDS = [
    # "notify-send 'Predator Key' 'Activated!'",
    # "pactl set-sink-volume @DEFAULT_SINK@ +5%",  # Volume up
]

# Debounce time (seconds) - how long to wait between key presses
DEBOUNCE_TIME = 0.3
# ===================================

def find_predator_device():
    """Find the ACER Gaming Keyboard device"""
    
    # First try event9 since that's where you saw it in evtest
    try:
        device = evdev.InputDevice('/dev/input/event9')
        print(f"Trying event9 directly: {device.name}")
        return '/dev/input/event9'
    except:
        pass
    
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    
    # Then try to find by name
    for device in devices:
        if "ACER USB-HID Gaming Keyboard" in device.name:
            print(f"Found ACER Gaming Keyboard: {device.name} ({device.path})")
            return device.path
    
    # Fallback: look for devices with ABS_MISC capability
    for device in devices:
        if evdev.ecodes.EV_ABS in device.capabilities():
            abs_events = device.capabilities()[evdev.ecodes.EV_ABS]
            if evdev.ecodes.ABS_MISC in [event[0] for event in abs_events]:
                print(f"Found device with ABS_MISC: {device.name} ({device.path})")
                return device.path
    
    return None

def handle_predator_key():
    device_path = find_predator_device()
    
    if not device_path:
        print("Could not find Predator key device")
        return
    
    print(f"Monitoring device: {device_path}")
    
    try:
        device = evdev.InputDevice(device_path)
        print(f"Listening for Predator key on: {device.name}")
        
        last_press_time = 0
        
        for event in device.read_loop():
            # Debug: print all events to see what we're getting
            if event.type != evdev.ecodes.EV_SYN:  # Skip sync events (too noisy)
                print(f"Event: type={event.type}, code={event.code}, value={event.value}")
                print(f"  Type name: {evdev.ecodes.EV[event.type] if event.type in evdev.ecodes.EV else 'UNKNOWN'}")
                if event.type in evdev.ecodes.bytype:
                    code_dict = evdev.ecodes.bytype[event.type]
                    print(f"  Code name: {code_dict[event.code] if event.code in code_dict else 'UNKNOWN'}")
            
            # Check for ABS_MISC events (your Predator key)
            if event.type == evdev.ecodes.EV_ABS and event.code == evdev.ecodes.ABS_MISC:
                current_time = time.time()
                
                # Only trigger on press (value 1) and debounce
                if event.value == 1 and (current_time - last_press_time) > DEBOUNCE_TIME:
                    last_press_time = current_time
                    print("🔥 PREDATOR KEY PRESSED! 🔥")
                    
                    # Execute the main command
                    try:
                        print(f"Running: {PREDATOR_KEY_COMMAND}")
                        # Split command if it has arguments (like "notify-send 'Hello' 'World'")
                        if ' ' in PREDATOR_KEY_COMMAND and not PREDATOR_KEY_COMMAND.startswith('/'):
                            subprocess.run(PREDATOR_KEY_COMMAND.split(), check=False)
                        else:
                            subprocess.run([PREDATOR_KEY_COMMAND], check=False)
                            
                    except FileNotFoundError:
                        print(f"Command not found: {PREDATOR_KEY_COMMAND}")
                        print("Make sure the application is installed and in your PATH")
                    except Exception as e:
                        print(f"Error running command: {e}")
                    
                    # Execute any extra commands
                    for cmd in EXTRA_COMMANDS:
                        try:
                            print(f"Running extra command: {cmd}")
                            if ' ' in cmd and not cmd.startswith('/'):
                                subprocess.run(cmd.split(), check=False)
                            else:
                                subprocess.run([cmd], check=False)
                        except Exception as e:
                            print(f"Error running extra command '{cmd}': {e}")
                        
    except PermissionError:
        print("Permission denied. Try running with sudo or add your user to the input group:")
        print("sudo usermod -a -G input $USER")
        print("Then log out and back in")
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    handle_predator_key()
