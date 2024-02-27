import inputs, keyboard, yaml, os, subprocess, threading, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CONFIG_FILE = "./config.yaml"

stratagems = {
    "Reinforce": "W, S, D, A, W",
    "Machine Gun": "S, A, S, W, D",
    "Anti-Material Rifle": "S, A, D, W, S",
    "Stalwart": "S, A, S, W, W, A",
    "Expendable Anti-Tank": "S, S, A, W, D",
    "Recoilless Rifle": "S, A, D, D, A",
    "Flamethrower": "S, A, W, S, W",
    "Autocannon": "S, D, A, S, S, W, W, D",
    "Railgun": "S, D, A, S, S, W, A, S, D",
    "Spear": "S, S, W, S, S",
    "Orbital Gatling Barrage": "D, S, A, W, W",
    "Orbital Airburst Strike": "D, D, D",
    "Orbital 120MM HE Barrage": "D, S, S, A, S, D, S, S",
    "Orbital 380MM HE Barrage": "D, S, S, W, W, A, S, S, S",
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
    "Guard Dog Rover": "S, A, S, W, A, S, S",
    "Ballistic Shield Backpack": "S, A, W, W, D",
    "Arc Thrower": "S, D, W, A, S",
    "Shield Generator Pack": "S, W, A, S, D, D",
    "Machine Gun Sentry": "S, W, D, S, D, S, W",
    "Gatling Sentry": "S, W, D, A, S",
    "Mortar Sentry": "S, W, D, D, S",
    "Guard Dog": "S, W, A, S, W, D, S",
    "Autocannon Sentry": "S, W, D, W, A, W",
    "Rocket Sentry": "S, W, D, D, A",
    "EMS Mortar Sentry": "S, S, W, W, A",
    "None": "",
}

default_config = {
    'DPad': {
        'Up': "Autocannon Sentry",
        'Down': "Guard Dog Rover",
        'Left': "Gatling Sentry",
        'Right': "Mortar Sentry"
    },
    "Left Button": "Machine Gun",
    "Right Button": "Recoilless Rifle",
    "Right Trigger": "Reinforce",
    "Buttons": {
        "Y": "Anti-Material Rifle",
        "B": "Stalwart",
        "X": "Orbital Gatling Barrage",
        "A": "Orbital Precision Strike"
    }
}

if not os.path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as file:
        file.write("# Configuration file for Helldivers Stratagem Hotkeys.\n")
        yaml.dump(default_config, file)
        file.write("\n# Avaiable Stratagems: \n# {}".format('\n# '.join(stratagems.keys())))

def load_config():
    global config
    with open(CONFIG_FILE, "r") as file:
        file_config = yaml.safe_load(file)
    config = {**default_config, **file_config}

class ConfigFileChangeMonitor(FileSystemEventHandler):
    def dispatch(event):
        if(event.event_type != "modified"):
            return
        print("Config File Modified, Reloading...")
        load_config()


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

    keyboard.press('ctrl')

    print(keys)
    for key in keys:
        keyboard.press(key)
        keyboard.release(key)
        time.sleep(0.001)
    
    keyboard.release('ctrl')

# Load the config file
load_config()

# Monitor the config file for changes
ob = Observer()
ob.schedule(ConfigFileChangeMonitor, os.path.dirname(CONFIG_FILE), recursive=False)
ob.start()

# View Config File
subprocess.Popen(['notepad.exe', CONFIG_FILE], creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS)

# Left Trigger is Held Down?
ltriggerPulled = False

# Application Logic
while True:

    try:
        gamepad = inputs.devices.gamepads[0]
    except: # Check if GamePad is connected.
        print("No gamepad found. Connect a gamepad and restart the application.")
        exit()

    try:
        events = gamepad.read()
    except KeyboardInterrupt: # Allow Control+C to exit the application
        ob.stop()
        print("Exiting...")
        exit()

    # Events were found and can be iterated over now.
    for event in events:
        if(event.ev_type == "Sync"):
            continue

        if(ltriggerPulled is False and event.code == "ABS_Z" and event.state > 0):
            ltriggerPulled = True
            print("Left trigger pulled")
        if(ltriggerPulled is True and event.code == "ABS_Z" and event.state == 0):
            ltriggerPulled = False
            print("Left trigger released")

        if(ltriggerPulled and event.code == 'ABS_RZ' and event.state == 0):
            play_keys(config['Right Trigger'])
            print("Right Trigger")

        if(ltriggerPulled and event.code == "ABS_HAT0X"):
            if(event.state == -1):
                play_keys(config['DPad']['Left'])
                print("Left DPad")
            if(event.state == 1):
                play_keys(config['DPad']['Right'])
                print("Right DPad")
        
        if(ltriggerPulled and event.code == "ABS_HAT0Y"):
            if(event.state == -1):
                play_keys(config['DPad']['Up'])
                print("Up DPad")
            if(event.state == 1):
                play_keys(config['DPad']['Down'])
                print("Down DPad")
        
        if(ltriggerPulled and event.code == "BTN_TL" and event.state == 1):
            play_keys(config['Left Button'])
            print("Left Button")
        
        if(ltriggerPulled and event.code == "BTN_TR" and event.state == 1):
            play_keys(config['Right Button'])
            print("Right Button")
        
        if(ltriggerPulled and event.code == "BTN_NORTH" and event.state == 1):
            play_keys(config['Buttons']['Y'])
            print("Y Button")
        
        if(ltriggerPulled and event.code == "BTN_SOUTH" and event.state == 1):
            play_keys(config['Buttons']['B'])
            print("B Button")
        
        if(ltriggerPulled and event.code == "BTN_WEST" and event.state == 1):
            play_keys(config['Buttons']['X'])
            print("X Button")
        
        if(ltriggerPulled and event.code == "BTN_EAST" and event.state == 1):
            play_keys(config['Buttons']['A'])
            print("A Button")


