import pip

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        # pip 10.0.0 or later
        from pip._internal.main import main as pip_main
        pip_main(['install', package])

import inputs, yaml, os, subprocess, threading, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    import vgamepad
except ImportError:
    install('vgamepad')
    import vgamepad

gamepad = vgamepad.VX360Gamepad()

controller_keyMap = {
    'ctrl': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    'w': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    'a': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
    's': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    'd': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT
}

CONFIG_FILE = "./config.yaml"

stratagems = {
    "SOS Beacon": "S, W, D, W",
    "Resupply": "S, S, W, D",
    "Reinforce": "W, S, D, A, W",
    "Machine Gun": "S, A, S, W, D",
    "Anti-Material Rifle": "S, A, D, W, S",
    "Stalwart": "S, A, S, W, W, A",
    "Expendable Anti-Tank": "S, S, A, W, D",
    "Recoilless Rifle": "S, A, D, D, A",
    "Flamethrower": "S, A, W, S, W",
    "Autocannon": "S, A, S, W, W, D",
    "Railgun": "S, D, A, S, S, W, A, S, D",
    "Spear": "S, S, W, S, S",
    "Orbital Gatling Barrage": "D, S, A, W, W",
    "Orbital Airburst Strike": "D, D, D",
    "Orbital 120MM HE Barrage": "D, D, S, A, D, S",
    "Orbital 380MM HE Barrage": "D, S, W, W, A, S, S",
    "Orbital Walking Barrage": "D, D, S, A, D, S",
    "Orbital Laser Strike": "D, S, W, D, S",
    "Orbital Railcannon Strike": "D, W, S, S, D",
    "Eagle Strafing Run": "W, D, D",
    "Eagle Airstrike": "W, D, S, D",
    "Eagle Cluster Bomb": "W, D, S, S, D, S",
    "Eagle Napalm Airstrike": "W, D, S, W",
    "Jump Pack": "S, W, W, S, W",
    "Eagle Smoke Strike": "W, D, W, S",
    "Eagle 110MM Rocket Pods": "W, D, W, A",
    "Eagle 500KG Bomb": "W, D, S, S, S",
    "Orbital Precision Strike": "A, A, W",
    "Orbital Gas Strike": "D, D, W",
    "Orbital EMS Strike": "D, D, S, D",
    "Orbital Smoke Strike": "D, D, S, W",
    "HMG Emplacement": "S, W, A, D, D, A",
    "Shield Generator Relay": "S, W, A, D, A, S",
    "Tesla Tower": "S, W, D, W, A, D",
    "Anti-Personnel Minefield": "S, A, S, W, D",
    "Supply Pack": "S, A, S, W, W, S",
    "Grenade Launcher": "S, A, S, W, A, S, S",
    "Laser Cannon": "S, A, S, W, A",
    "Incendiary Mines": "S, A, A, S",
    "Guard Dog Rover": "S, W, A, W, D, D",
    "Ballistic Shield Backpack": "S, A, W, W, D",
    "Arc Thrower": "S, D, W, A, S",
    "Shield Generator Pack": "S, W, A, S, D, D",
    "Machine Gun Sentry": "S, W, D, D, W",
    "Gatling Sentry": "S, W, D, A, S",
    "Mortar Sentry": "S, W, D, D, S",
    "Guard Dog": "S, W, A, S, W, D, S",
    "Autocannon Sentry": "S, W, D, W, A, W",
    "Rocket Sentry": "S, W, D, D, A",
    "EMS Mortar Sentry": "S, S, W, W, A",
    "Hell Bomb": "S, W, A, S, W, D, S, W",
    "None": "",
}

default_config = {
    "Right Button": "Recoilless Rifle",
    "Left Trigger": "SOS Beacon",
    "Right Trigger": "Reinforce",
    "Buttons": {
        "Y": "Anti-Material Rifle",
        "B": "Stalwart",
        "X": "Orbital Gatling Barrage",
        "A": "Orbital Precision Strike"
    }
}

def load_config():
    global config
    with open(CONFIG_FILE, "r") as file:
        try:
            file_config = yaml.safe_load(file)
        except:
            print("Error reading config file. Using default config.")
            file_config = {}

    config = {**default_config, **file_config}

class ConfigFileChangeMonitor(FileSystemEventHandler):
    def dispatch(event):
        if(event.event_type != "modified"):
            return
        print("Config File Modified, Reloading...")
        load_config()

def keyDown(key):
    gamepad.press_button(button=controller_keyMap[key])
    gamepad.update()

def keyUp(key):
    gamepad.release_button(button=controller_keyMap[key])
    gamepad.update()


# Play KeyStrokes
def play_keys(stratagem):
    if(stratagem not in stratagems):
        print("Stratagem not found: {}".format(stratagem))
        return

    print("Running Stratagem: {}".format(stratagem))
    keys = stratagems[stratagem].lower().split(", ") 

    if(keys == ['']):
        print("Stratagem has no keys to press... {}".format(stratagem))
        return # No keys to press

    for key in keys:
        # print(key) 
        keyDown(key)
        time.sleep(0.025)
        keyUp(key)
        time.sleep(0.025)

    # gamepad.reset()

def initialize_gamepad():
    try:
        return inputs.devices.gamepads[0]
    except IndexError:
        print("No gamepad found. Connect a gamepad and restart the application.")
        exit()

def handle_event(event, lButtonHeld, config):
    if event.ev_type == "Sync":
        return lButtonHeld  # No state change for sync events

    if event.code == "BTN_TL":
        lButtonHeld = event.state == 1
        print("Left Button Pushed" if lButtonHeld else "Left Button Released")

    if lButtonHeld:
        button_actions = {
            'ABS_RZ': ("Right Trigger", config['Right Trigger']),
            'BTN_TR': ("Right Button", config['Right Button']),
            'BTN_NORTH': ("Y Button", config['Buttons']['Y']),
            'BTN_SOUTH': ("B Button", config['Buttons']['A']),
            'BTN_WEST': ("X Button", config['Buttons']['X']),
            'BTN_EAST': ("A Button", config['Buttons']['B']),
        }
        
        action = button_actions.get(event.code)
        if action and event.state == 0:
            print(action[0])
            play_keys(action[1])
            
    return lButtonHeld

if __name__ == "__main__":

    # Create the config file if it doesn't exist
    if not os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as file:
            file.write("# Configuration file for Helldivers Stratagem Hotkeys.\n")
            yaml.dump(default_config, file)
            file.write("\n# Avaiable Stratagems: \n# {}".format('\n# '.join(stratagems.keys())))
        
        # View Config File
        subprocess.Popen(['notepad.exe', CONFIG_FILE], creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS)

    # Load the config file
    load_config()

    # Monitor the config file for changes
    ob = Observer()
    ob.schedule(ConfigFileChangeMonitor, os.path.dirname(CONFIG_FILE), recursive=False)
    ob.start()

    lButtonHeld = False
    listening_gamepad = initialize_gamepad()

    while True:
        try:
            events = listening_gamepad.read()
            for event in events:
                lButtonHeld = handle_event(event, lButtonHeld, config)
        except KeyboardInterrupt:
            print("Exiting...")
            exit()
        time.sleep(0.01)