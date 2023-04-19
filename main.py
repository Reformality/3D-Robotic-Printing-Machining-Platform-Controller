from dorna import Dorna
import time
import json

# Connect to Dorna

configFile = "C:/Users/zwu22/Downloads/newConfig.yaml"
robot = Dorna(configFile)
a = robot.connect()
parsed_json = json.loads(a)
print(parsed_json)

if parsed_json['connection'] == 2:
    print("Status: Robot Object Created!")

    # Homing
    print("###### START HOMING ######")
    print("Homing j0")
    robot.home("j0")
    print("Homing j1")
    robot.home("j1")
    print("Homing j2")
    robot.home("j2")
    print("Homing j3")
    robot.home("j3")
    print("###### END HOMING ######")

    robot.set_toolhead({"x": 1.25})  # no tool

    # ===========CALIBRATION=========== #

    # Calibrate Position [90,0,0,0,0]
    start = {"command": "move",
             "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 90, "j1": 0, "j2": 0, "j3": 0, "j4": 0}}
    robot.play(start)

    # Rotate j4 25 degrees
    j4_arg = {"command": "move",
             "prm": {"path": "joint", "movement": 1, "speed": 2000, "j0": 0, "j1": 0, "j2": 0, "j3": 0, "j4": 25}}
    robot.play(j4_arg)

    # Rotate j3 10 degrees
    j3_arg = {"command": "move",
             "prm": {"path": "joint", "movement": 1, "speed": 2000, "j0": 0, "j1": 0, "j2": 0, "j3": 10, "j4": 0}}
    robot.play(j3_arg)

    # Calibrate j3 to 0
    robot.calibrate([90, 0, 0, 0, 0])

    # =========== WALK LINE =========== #

    # walk line priming position [90, 30, -120, 0, 0]
    start = {"command": "move",
             "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 90, "j1": 30, "j2": -120, "j3": 0, "j4": 0}}
    robot.play(start)

    # plate inner edge
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": 0, "y": 7, "z": 1.5, "a": -90, "b": 0}}
    robot.play(arg)

    # plate outer edge
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": 0, "y": 16, "z": 1.5, "a": -90, "b": 0}}
    robot.play(arg)

    # =========== PRINTER PICKUP =========== #

    # Rotate j4 45 degrees (+ rotate out)
    j4_arg = {"command": "move",
             "prm": {"path": "joint", "movement": 1, "speed": 2000, "j0": 0, "j1": 0, "j2": 0, "j3": 0, "j4": 45}}
    robot.play(j4_arg)

    # printer priming position [180, 50, -140, 0, 0]
    arg = {"command": "move",
             "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 180, "j1": 40, "j2": -130, "j3": 0, "j4": 45}}
    robot.play(arg)

    # 3D extruder drop prime
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -12.5, "y": 0, "z": 6.5, "a": -90, "b": 45}}
    robot.play(arg)

    # 3D extruder in
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -12.5, "y": 0, "z": 4.3, "a": -90, "b": 45}}
    robot.play(arg)

    # 3D extruder out
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -10.5, "y": 0, "z": 4.3, "a": -90, "b": 0}}
    robot.play(arg)

    # =========== DRILL PICKUP =========== #
    # Drill pick up drop prime
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 240, "x": -10, "y": 10, "z": 5.5, "a": -90, "b": 45}}
    robot.play(arg)

    # Drill pick up drop in
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 240, "x": -10, "y": 10, "z": 3.4, "a": -90, "b": 45}}
    robot.play(arg)

    # Rotate j4 -45 degrees (- rotate in)
    j4_arg = {"command": "move",
              "prm": {"path": "joint", "movement": 1, "speed": 2000, "j0": 0, "j1": 0, "j2": 0, "j3": 0, "j4": -45}}
    robot.play(j4_arg)



    # printing location
    # robot.position("x")
    # '[0, 12, 5.22, -90, 0]'

    # drill toolhead setting change
    # from '[135, 30, -100, 90.0, 0.0]' to j3=0;
    robot.calibrate([135, 30, -100, 0.0, 0.0])
    robot.set_toolhead({"x": 3}) # drill head




    # drill starting prime
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": 2, "y": 10.7, "z": 5, "a": -90, "b": 0}}
    robot.play(arg)

    # drill starting point
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": 2, "y": 10.7, "z": 3.5, "a": -90, "b": 0}}
    robot.play(arg)

    # drill path
    # ------------

    # drill finish prime
    # ------------

    # putback position
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 1000, "j0": 135, "j1": 30, "j2": -100, "j3": 0, "j4": 0}}
    job = robot.play(arg)

    # set toolhead back to nohead
    robot.calibrate([135, 30, -100, 90, 0.0])
    robot.set_toolhead({"x": 1.25})  # no tool







else:
    print("ERROR: Robot Not Connected!")

time.sleep(5)
robot.terminate()
print("Status: Robot process terminated!")


