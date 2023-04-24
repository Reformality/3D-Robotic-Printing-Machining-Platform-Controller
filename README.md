# Robotic Arm Command Interface using Dorna Library

This project provides an interactive command interface for controlling a robotic arm using the Dorna library. The script enables users to perform various tasks such as connecting to the robot, homing, calibrating, checking the robot's position, and working with different toolheads, such as a 3D printer and a drill.

## Requirements

- Python 3
- Dorna library
- A robotic arm compatible with the Dorna library
- A configuration file for the robotic arm

## Installation

1. Install Python 3 if you haven't already.

2. Install the Dorna library using pip:
```
pip install dorna
```

3. Ensure you have a robotic arm compatible with the Dorna library and a correctly set up configuration file.

## Usage

1. Run the Python script containing the main function:
```
python main.py
```

2. Once the script is running, you will be prompted to enter commands for controlling the robotic arm.

3. Enter the desired command and press Enter to execute the corresponding method.

4. To exit the program, enter 'q' and press Enter.

## Available Commands

- homing: Home the robot.
- homed: Check if the robot is homed.
- toolhead: Change the toolhead.
- calibrate: Calibrate the robot.
- terminate: Terminate the robot's connection.
- position: Get the robot's position.
- walkline: Walk the robot along a line.
- printer_pickup: Pick up a 3D printer toolhead.
- printer_putback: Put back a 3D printer toolhead.
- heat: Heat the extruder.
- test_print: Perform a test print.
- print: Execute a print operation.
- cool: Cool down the extruder.
- drill_pickup: Pick up a drill toolhead.
- drill_putback: Put back a drill toolhead.
- drill: Execute a drilling operation.

## Contributing

Please feel free to open an issue or submit a pull request with any improvements, bug fixes, or new features you would like to see in this project.

## License

This project is open-source and available under the [MIT License](LICENSE).
