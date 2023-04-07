import sys
from dorna import Dorna
import time
import json


def is_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def wait(robot, job):
    parsed_json = json.loads(job)
    job_id = parsed_json[0]["id"]
    print("[wait] Working on job id={}".format(job_id))
    while parsed_json[0]['state'] != 2:
        time.sleep(0.1)
        parsed_json = json.loads(robot.command({"id": job_id}))
    print("[Wait] Work Done!\n")


def homing(robot):
    print("###### START HOMING ######")
    print(robot.homed())
    print("Homing j0")
    robot.home("j0")
    print("Homing j1")
    robot.home("j1")
    print("Homing j2")
    robot.home("j2")
    print("Homing j3")
    robot.home("j3")
    print(robot.homed())
    print("###### END HOMING ######")


def toolhead(robot):
    tool_type = input("[Tool Head] Select the toolhead type (nohead, print, mill), or q to quit:\n")
    if tool_type == 'q':
        return
    elif tool_type == 'nohead':
        robot.set_toolhead({"x": 1.25})  # no tool head, adaptor only
        print(robot.toolhead())
    elif tool_type == 'print':
        robot.set_toolhead({"x": 5.75})  # printing package
        print(robot.toolhead())
    elif tool_type == 'mill':
        print("INOP")
    else:
        print("Invalid method")


def calibrate(robot):
    # Calibrate Position [90,0,0,0,0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 90, "j1": 0, "j2": 0, "j3": 0, "j4": 0}}
    job = robot.play(arg)
    wait(robot, job)
    print(robot.position())
    # Calibrate j3 and j4
    while True:
        choice = input("[Calibrate] Choose: j3, j4, \"end\" to finish calibration, or \"q\" to quit:\n")
        if choice == "q":
            return
        elif choice == "end":
            robot.calibrate([90, 0, 0, 0, 0])
            return
        elif choice == "j3" or choice == "j4":
            angle = input("[Calibrate] type {} calibration angle:".format(choice))
            if is_integer(angle) and abs(int(angle)) <= 180:
                turn_deg = int(angle)
                if choice == "j3":
                    arg = {"command": "move",
                           "prm": {"path": "joint", "movement": 1, "speed": 2000,
                                   "j0": 0, "j1": 0, "j2": 0, "j3": turn_deg, "j4": 0}}
                    job = robot.play(arg)
                    wait(robot, job)
                else:  # j4
                    arg = {"command": "move",
                           "prm": {"path": "joint", "movement": 1, "speed": 2000,
                                   "j0": 0, "j1": 0, "j2": 0, "j3": 0, "j4": turn_deg}}
                    job = robot.play(arg)
                    wait(robot, job)
                print(robot.position())
            else:
                print("Invalid choice (-180 < degree < 180)!")
        else:
            print("Invalid input!")


def terminate(robot):
    robot.terminate()
    print("Status: Robot process terminated!")
    return


def walk_line_hotpad(robot):
    # priming position [90, 30, -120, 0, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 90, "j1": 40, "j2": -130, "j3": 0, "j4": 0}}
    job = robot.play(arg)
    wait(robot, job)
    print("At Priming position")
    time.sleep(1)

    # rotate j4 180 degree
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 6000, "j0": 90, "j1": 40, "j2": -130, "j3": 0, "j4": 180}}
    job = robot.play(arg)
    wait(robot, job)
    print("Flip 180")
    time.sleep(1)

    # plate inner edge
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": 0, "y": 7, "z": 1.5, "a": -90, "b": 180}}
    job = robot.play(arg)
    wait(robot, job)
    print("X:0, Y:7, Z:1.5, A:-90, B:0")
    time.sleep(1)

    # plate outer edge
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": 0, "y": 16, "z": 1.5, "a": -90, "b": 180}}
    job = robot.play(arg)
    wait(robot, job)
    print("X:0, Y:16, Z:1.5, A:-90, B:0")
    time.sleep(1)

    # priming position [90, 30, -120, 0, 180]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 90, "j1": 40, "j2": -130, "j3": 0, "j4": 180}}
    job = robot.play(arg)
    wait(robot, job)
    print("Flip 180")
    time.sleep(1)

    # priming position [90, 30, -120, 0, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 6000, "j0": 90, "j1": 40, "j2": -130, "j3": 0, "j4": 0}}
    job = robot.play(arg)
    wait(robot, job)
    print("Flip 180")
    time.sleep(1)


def printer_demo(robot):
    # printer priming position [180, 50, -140, 0, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 180, "j1": 40, "j2": -130, "j3": 0, "j4": 45}}
    job = robot.play(arg)
    wait(robot, job)

    # 3D extruder drop prime position
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -12.5, "y": 0, "z": 6.5, "a": -90, "b": 45}}
    job = robot.play(arg)
    wait(robot, job)

    # 3D extruder in
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -12.5, "y": 0, "z": 4.1, "a": -90, "b": 45}}
    job = robot.play(arg)
    wait(robot, job)

    # Rotate j4 45 degrees (+ rotate out)
    arg = {"command": "move",
              "prm": {"path": "joint", "movement": 1, "speed": 2000, "j0": 0, "j1": 0, "j2": 0, "j3": 0, "j4": -45}}
    job = robot.play(arg)
    wait(robot, job)

    # 3D extruder out
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -10.5, "y": 0, "z": 4.3, "a": -90, "b": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # printer priming position [180, 50, -140, 0, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 180, "j1": 40, "j2": -130, "j3": 0, "j4": 0}}
    robot.play(arg)

    # PUT BACK
    time.sleep(5)

    # 3D extruder out
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -10.5, "y": 0, "z": 4.3, "a": -90, "b": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # 3D extruder in
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -12.5, "y": 0, "z": 4.3, "a": -90, "b": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # Rotate j4 45 degrees (+ rotate out)
    arg = {"command": "move",
              "prm": {"path": "joint", "movement": 1, "speed": 2000, "j0": 0, "j1": 0, "j2": 0, "j3": 0, "j4": 45}}
    job = robot.play(arg)
    wait(robot, job)

    # 3D extruder drop prime position
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -12.5, "y": 0, "z": 6.5, "a": -90, "b": 45}}
    job = robot.play(arg)
    wait(robot, job)

    # printer priming position [180, 50, -140, 0, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 180, "j1": 40, "j2": -130, "j3": 0, "j4": 0}}
    job = robot.play(arg)
    wait(robot, job)


def main():
    print("\n## START CONNECT ##")
    configFile = "C:/Users/zwu22/Downloads/newConfig.yaml"
    robot = Dorna(configFile)
    a = robot.connect()
    parsed_json = json.loads(a)
    print(parsed_json)
    if parsed_json['connection'] == 2:
        print("Status: Robot Object Created!")
    else:
        print("ERROR: Robot Not Connected!")
        robot.terminate()
        print("Status: Robot process terminated!")
        return
    print("## END CONNECT ##\n")

    while True:
        method = input("\nEnter the method you would like to run. \n "
                       "homing, homed, toolhead, calibrate, terminate, position, walkline, printer_demo, q (quit)\n")
        if method == 'q':
            return
        elif method == 'homing':
            homing(robot)
        elif method == 'homed':
            print(robot.homed())
        elif method == 'toolhead':
            toolhead(robot)
        elif method == 'calibrate':
            calibrate(robot)
        elif method == 'terminate':
            terminate(robot)
            return
        elif method == 'position':
            print("j-axis: ", robot.position())
            print("xyz: ", robot.position("xyz"))
        elif method == 'walkline':
            walk_line_hotpad(robot)
        elif method == 'printer_demo':
            printer_demo(robot)
        else:
            print("Invalid method:", method)


if __name__ == '__main__':
    main()
