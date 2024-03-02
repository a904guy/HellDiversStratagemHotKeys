# Hell Divers 2 Stratagem HotKeys Macro
A python application to map Stratagems to GamePad Controls.

Press a single game pad button to run an entire strategem combo.

This application only works with controller users. I'll work on making it work with keyboard in the future.

# To install
First you need to install the required python packages, this includes a driver for a virtual game pad that will need to be installed. The pip install will walk you through that process.
Try the following commands, only one of them needs to be ran. I'm supplying a few because python setups on windows can be finiky.
```
pip install -r packages.list
pip.exe install -r packages.list
python -m pip install -r packages.list
python.exe -m pip install -r packages.list
```
# To run
You'll need to run just one of the command lines below. Again I supply multiple because depending on your python install some may not work. You only need to run one command successfully for the application to run.
```
python app.py
python.exe app.py
```

When you launch the application it will open Notepad, and it will open the config file for the application. The application file will be full of information on setting it up, and list all the Stratagems for usage.
The config will look like this.

```./config.yaml```
```yaml
# Configuration file for Helldivers Stratagem Hotkeys.
Buttons:
  A: Mortar Sentry
  B: Machine Gun Sentry
  X: Gatling Sentry
  Y: Guard Dog Rover
Right Button: Resupply
Left Trigger: SOS Beacon
Right Trigger: Reinforce

# Avaiable Stratagems: 
# Reinforce
# Machine Gun
# Anti-Material Rifle
# Stalwart
# Expendable Anti-Tank
# Recoilless Rifleglamethrower
# Autocannon
# Railgun
# Spear
# Orbital Gatling Barrage
# Orbital Airburst Strike
# ... Continued
```

To set a new combo you just copy the Stratagem's name from the list below (without the hashtag/pound sign #) onto the button you want it mapped to.
Save the file and the application will reload the config file real time and you can begin using them immediately.

# To use
Simply hold down the left button above the left trigger. Then press the button in the config. The combo will be entered and you can then throw the beacon wherever you like.

Enjoy!
