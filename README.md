# Yongnuo CLI Light Switcher

The Yongnuo CLI Light Switcher is a command-line tool that allows you to control and manage your Yongnuo lights through your computer. It provides functionality to turn the lights on or off, adjust the color temperature, and discover nearby lights for control. The tool also maintains a configuration file to remember your preferred settings.

## Installation

1. Make sure you have Python installed on your system.
2. Clone or download the repository to your preferred directory.
3. Open a terminal and navigate to the project directory.

## Dependencies

The script uses the following external libraries:

- `lantern`: A library for controlling Bluetooth lights. This library abstracts the communication with the Yongnuo lights.
- `argparse`: A library for parsing command-line arguments.
- `os`: Library for working with the operating system (used for file operations).
- `yaml`: A library for reading and writing YAML files.

You can install the required dependencies using the following command:

```bash
pip install lantern argparse pyyaml
```

## Usage
The script provides the following command-line options:

`--on`: Turn on the light.  
`--off`: Turn off the light.  
`-t, --toggle`: Toggle the current light state.  
`-a, --address [MAC_ADDRESS]`: Directly communicate with a light using its MAC address.  
`-d, --discover`: Search for all nearby lights and perform actions on them.  
`--warm [0-100]`: Set the warm light color (color temperature around 3200K).  
`--cool [0-100]`: Set the cool light color (color temperature around 5500K).  

## Examples

To turn on the light:
```bash
python yongnuo-cli.py --on
```
To turn off the light:
```bash
python yongnuo-cli.py --off
```

To toggle the light state:
```bash
python yongnuo-cli.py -t
python yongnuo-cli.py --toggle
```

To set a specific MAC address and turn on the light:
```bash
python yongnuo-cli.py --address 00:00:00:00:00:00 --on
```
To discover nearby lights and set warm and cool colors:
bash
```
python yongnuo-cli.py --discover --warm 50 --cool 70
```

To display help and usage information:
```bash
python yongnuo-cli.py --help
```

## Configuration
The script stores configuration settings in a YAML file located at `~/.config/yongnuo-cli/config.yaml`. The configuration includes the light's state (on/off), warm and cool color settings, and the light's MAC address.

```yaml
# Configuration for Yongnuo CLI Light Switcher

# Default configuration values
state: false         # Current state of the light (true for on, false for off)
warm_color: 50       # Warm light color setting (0-100)
cool_color: 70       # Cool light color setting (0-100)
address: "00:00:00:00:00:00"  # MAC address of the light

# Example configuration values after using the CLI tool
# state: true
# warm_color: 70
# cool_color: 30
# address: "11:22:33:44:55:66"
```

## Note
The script might need to connect to the light multiple times due to Bluetooth connectivity issues.
The lantern library is used for communication with the Yongnuo lights and abstracts some low-level operations.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
