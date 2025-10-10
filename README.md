# Predator Key Linux Support

This Python script enables the special "Predator" key (usually located above the keyboard on Acer Predator laptops) to work under Linux.

## Tested On

| Model | Module | Kernel Input | Event Device |
|-------|--------|--------------|--------------|
| Acer Predator Helios 16 | PH16-71 | `ABS_MISC` | `/dev/input/event9` |
| Acer Predator Helios 300 | PH315-52 | `KEY_PRESENTATION` | `/dev/input/event4` |

> **Note**: With auto-detection, the script works on any Acer Predator model without manual configuration!

## Features

- **Auto-Detection**: Automatically detects the correct input device and key code
- **Smart Caching**: Saves configuration for instant startup on subsequent runs
- **Universal Compatibility**: Works across different Acer Predator models without manual configuration
- **Immediate Execution**: Runs your command from the very first press
- Maps the key press to any custom command or script
- Optional support for multiple additional commands
- Built-in debounce to prevent repeated triggers
- Works on startup

## 🖥️ Run on Startup

You can run the script automatically at login using one of the following methods:
1. Autostart (Desktop Environments)

For GNOME, KDE, XFCE, etc. create a .desktop entry:
```bash
cat > ~/.config/autostart/predator-key.desktop << EOF
[Desktop Entry]
Name=Predator Key Handler
Exec=$HOME/predator-handler.py
Type=Application
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF
```
## 2. Hyprland (exec-once)

If you're using Hyprland, add this line to your ~/.config/hypr/hyprland.conf:
```
exec-once = python3 ~/Predator/predator-handler.py

```
Replace with the full path to your script.


## Requirements

- Python 3
- `evdev` library (`pip install evdev`)
- Access to input devices (`/dev/input/event*`)

## Installation

1. Clone the repo:
    ```bash
    git clone https://github.com/Order52/predator-key
    cd predator-key
    ```

2. Install dependencies:
    ```bash
    pip install evdev
    ```

3. (Optional) Add your user to the `input` group:
    ```bash
    sudo usermod -aG input $USER
    newgrp input
    ```

4. Make the script executable:
    ```bash
    chmod +x Predator/Predator-Key.py
    ```

## Usage

### 1. Configure Your Command

Edit the `PREDATOR_KEY_COMMAND` in the script to your desired command:
```bash
cd ~/predator-key/Predator/
nano Predator-Key.py
```

Change this line to whatever you want:
```python
PREDATOR_KEY_COMMAND = "notify-send 'Hello' 'Linux!'"
```

Examples:
```python
PREDATOR_KEY_COMMAND = "firefox"
PREDATOR_KEY_COMMAND = "kitty"
PREDATOR_KEY_COMMAND = "python /home/user/my-script.py"
```

### 2. First Run (Auto-Detection)

Run the script with sudo:
```bash
sudo python3 Predator-Key.py
```

When prompted, **press your Predator key once**. The script will:
- Automatically detect the correct input device (event4, event7, etc.)
- Detect the correct key code
- Save the configuration to `/tmp/predator_key.json`
- Run your command immediately
- Continue monitoring for future presses

### 3. Subsequent Runs

After the first detection, the script uses the cached configuration and starts immediately:
```bash
sudo python3 Predator-Key.py
```

### Reset Detection

If you need to re-detect (e.g., after hardware changes):
```bash
rm /tmp/predator_key.json
```

### ⚠️ Important Note on Paths

Do not use `~` (tilde) shortcuts in paths for startup commands or .desktop files. Always use the full absolute path.

✅ Correct:
```python
PREDATOR_KEY_COMMAND = "python /home/username/script.py"
```

❌ Incorrect:
```python
PREDATOR_KEY_COMMAND = "python ~/script.py"
```
