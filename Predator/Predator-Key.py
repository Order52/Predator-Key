#!/usr/bin/env python3
import evdev
import subprocess
import sys
import time
import os
import json
import argparse

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
PREDATOR_KEY_COMMAND = "python /home/o0xwolf/GitHub-SSD/PredatorSense-Linux/src/main.py"

# Optional: Add multiple commands (all will run when key is pressed)
# Leave empty [] if you only want the single command above

EXTRA_COMMANDS = [
    # "notify-send 'Predator Key' 'Activated!'",
    # "pactl set-sink-volume @DEFAULT_SINK@ +5%",  # Volume up
]

DEBOUNCE_TIME = 0.3

# Cache file to store detected device and key code
CACHE_FILE = "/tmp/predator_key.json"
# ===================================

def load_cache():
    """Load cached device path and key code"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return None

def save_cache(device_path, key_code):
    """Save detected device path and key code"""
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump({"device": device_path, "key_code": key_code}, f)
    except:
        pass

def detect_predator_key():
    """Interactive detection: Press the Predator key to detect it"""
    print("=" * 60)
    print("PREDATOR KEY DETECTION MODE")
    print("=" * 60)
    print("\nPress your Predator key now (within 10 seconds)...")
    print("Monitoring all input devices...\n")
    
    devices = []
    for path in evdev.list_devices():
        try:
            devices.append(evdev.InputDevice(path))
        except:
            pass
    
    start_time = time.time()
    timeout = 10
    detected = False
    
    # Monitor all devices simultaneously
    while time.time() - start_time < timeout:
        for device in devices:
            try:
                # Non-blocking read
                for event in device.read():
                    if event.type == evdev.ecodes.EV_KEY and event.value == 1:
                        # Filter out common keys
                        if event.code not in range(1, 90):  # Skip normal keyboard keys
                            if not detected:
                                print(f"\n✓ DETECTED!")
                                print(f"  Device: {device.name}")
                                print(f"  Path: {device.path}")
                                print(f"  Key Code: {event.code}")
                                print("🔥 PREDATOR KEY PRESSED! 🔥")
                                
                                # Run the command immediately on detection
                                try:
                                    print(f"Running: {PREDATOR_KEY_COMMAND}")
                                    subprocess.run(PREDATOR_KEY_COMMAND.split(), check=False)
                                except Exception as e:
                                    print(f"Error: {e}")
                                
                                save_cache(device.path, event.code)
                                detected = True
                                print("\nDetection complete! Continuing to monitor...\n")
                                return device.path, event.code
            except BlockingIOError:
                continue
            except:
                pass
        time.sleep(0.01)
    
    print("\n✗ No Predator key detected within timeout")
    return None, None

def find_predator_device():
    """Find the Predator key device using cache or detection"""
    
    # Try cache first
    cache = load_cache()
    if cache:
        device_path = cache.get("device")
        key_code = cache.get("key_code")
        if device_path and os.path.exists(device_path):
            print(f"✓ Using cached device: {device_path} (key code: {key_code})")
            print("  (To re-detect, delete: /tmp/predator_key_cache.json)\n")
            return device_path, key_code
    
    # Run detection
    print("No cached device found. Running detection...\n")
    return detect_predator_key()

def handle_predator_key():
    device_path, key_code = find_predator_device()
    
    if not device_path or not key_code:
        print("\nFailed to detect Predator key.")
        print("Try running the script again and press the Predator key when prompted.")
        return
    
    print(f"\n{'=' * 60}")
    print(f"Monitoring: {device_path}")
    print(f"Key Code: {key_code}")
    print(f"Command: {PREDATOR_KEY_COMMAND}")
    print(f"{'=' * 60}\n")
    
    try:
        device = evdev.InputDevice(device_path)
        last_press_time = 0
        
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY and event.code == key_code:
                current_time = time.time()
                
                if event.value == 1 and (current_time - last_press_time) > DEBOUNCE_TIME:
                    last_press_time = current_time
                    print("🔥 PREDATOR KEY PRESSED! 🔥")
                    
                    try:
                        print(f"Running: {PREDATOR_KEY_COMMAND}")
                        subprocess.run(PREDATOR_KEY_COMMAND.split(), check=False)
                    except FileNotFoundError:
                        print(f"Command not found: {PREDATOR_KEY_COMMAND}")
                    except Exception as e:
                        print(f"Error: {e}")
                    
                    for cmd in EXTRA_COMMANDS:
                        try:
                            subprocess.run(cmd.split(), check=False)
                        except Exception as e:
                            print(f"Error running extra command: {e}")
                        
    except PermissionError:
        print("Permission denied. Try running with sudo or add your user to the input group:")
        print("sudo usermod -a -G input $USER")
        print("Then log out and back in")
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")

def daemonize():
    """Fork the process to run in background"""
    try:
        pid = os.fork()
        if pid > 0:
            # Parent process, exit
            sys.exit(0)
    except OSError as e:
        print(f"Fork failed: {e}")
        sys.exit(1)
    
    # Decouple from parent environment
    os.chdir('/')
    os.setsid()
    os.umask(0)
    
    # Second fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        print(f"Fork failed: {e}")
        sys.exit(1)
    
    # Redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    
    # Redirect to /dev/null
    with open('/dev/null', 'r') as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'a+') as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open('/dev/null', 'a+') as f:
        os.dup2(f.fileno(), sys.stderr.fileno())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Predator Key Handler for Linux')
    parser.add_argument('--run-background', action='store_true',
                        help='Run in background (daemon mode)')
    args = parser.parse_args()
    
    if args.run_background:
        daemonize()
    
    handle_predator_key()
