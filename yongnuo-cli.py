from lantern import Light
import argparse
import os
import yaml

CONFIG_DIR = os.path.expanduser("~/.config/yongnuo-cli/")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.yaml")

DEFAULT_CONFIG = {
    "state": False,
    "warm_color": 00,
    "cool_color": 00,
    "address": ""
}

def ensure_config_file():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if not os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as file:
            yaml.dump(DEFAULT_CONFIG, file, default_flow_style=False)

def read_state(filename):
    try:
        with open(filename, 'r') as file:
            state = yaml.safe_load(file)
            return state
    except (IOError, yaml.YAMLError):
        return DEFAULT_CONFIG

def write_state(filename, state):
    with open(filename, 'w') as file:
        yaml.dump(state, file, default_flow_style=False)

def main():
    parser = argparse.ArgumentParser(
                    prog='Yongnuo Cli switcher',
                    description='Turn on/off Yongnuo, and set colors',
                    epilog='Text at the bottom of help')

    group_onoff = parser.add_mutually_exclusive_group(required=True)
    group_onoff.add_argument('--on', action='store_true', help='Turn on the light')
    group_onoff.add_argument('--off', action='store_true', help='Turn off the light')
    group_onoff.add_argument('-t', '--toggle', action='store_true', help='Change the current light state, this is not reliable, as we cannot fetch the light state')

    group_discover = parser.add_mutually_exclusive_group()
    group_discover.add_argument('-a', '--address',  metavar='00:00:00:00:00:00', type=str, help='Light mac address to directly communicate to a light')
    group_discover.add_argument('-d', '--discover', action='store_true', help='Search for all nearby lights and act on all')

    parser.add_argument('--warm', metavar='[0-100]', type=int, help='Warm light color, also noted as 3200k in some Yongnuo lights')
    parser.add_argument('--cool', metavar='[0-100]', type=int, help='Cool light, also noted as 5500k in some Yongnuo lights')

    # Load values from args
    args = parser.parse_args()

    # Load values from config file
    ensure_config_file()
    state = read_state(CONFIG_FILE)

    if args.address:
        lights = [Light(args.address)]
    else:
        lights = [Light(state['address'])]
    print(state['state'])
    print(f"Toggle state: {'ON' if state['state'] else 'OFF'}")
    print(f"Warm color: {state['warm_color']}")
    print(f"Cool color: {type(state['cool_color'])}")
    print(f"Address: {state['address']}")

    # Seach for nearby lights
    if args.discover:
        lights = Light.discover()

    if not args.warm:
        args.warm = state['warm_color']

    if not args.cool:
        args.cool = state['cool_color']

    # Iterate over all light detectedu
    for light in lights:
        # connect to the light
        # ugly hack because bluetooth is terrible
        try:
            light.connect()
        except:
            light.connect()

        # Toggle on/off state
        if args.toggle:
            if state['state']:
                args.off = True
            else:
                args.on = True

        # Set colors turns on light
        if args.on:
            print(f"Turning On light {light._mac}")
            light._send_packet(0xaa, 0x01, args.cool, args.warm)
            state['state'] = True

        # Set colors to 0 to turn off
        # Note: unfortatly light.power_off() doesnt work on my light model(600L II)
        if args.off:
            print(f"Turning Off light {light._mac}")
            light._send_packet(0xaa, 0x01, 00, 00)
            state['state'] = False

        write_state(CONFIG_FILE, state)
        light.disconnect()

if __name__ == "__main__":
    main()
