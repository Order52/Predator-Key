# Predator Key Linux Support

This Python script enables the special "Predator" key (usually located above the keyboard on Acer Predator laptops) to work under Linux.

Tested on:
- Model: Acer Predator Helios 16
- Module: PH16-71
- Kernel Input: `ABS_MISC` via `/dev/input/event9`

## Features

- Detects Predator key press using `evdev`
- Maps the key press to a custom command or script
- Optional support for multiple additional commands
- Built-in debounce to prevent repeated triggers
- Debug logging for key events
- Work on Startup

🖥️ Run on Startup

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

## Usage

Edit the `PREDATOR_KEY_COMMAND` in the script to your desired command:
```
nano Predator-Key.py
```

```
chmod +x Predator-Key.py
sudo chmod 666 /dev/input/event9
```
```
python Predator-Key.py
```
