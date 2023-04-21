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
    # print("[wait] Working on job id={}".format(job_id))
    while parsed_json[0]['state'] != 2:
        time.sleep(0.1)
        parsed_json = json.loads(robot.command({"id": job_id}))
    # print("[Wait] Work Done!\n")


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
    # Calibrate Prime Position [180, 50, -140, 0, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 90, "j1": 40, "j2": -130, "j3": 0, "j4": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # Calibrate Position [90,0,0,0,0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 90, "j1": 0, "j2": 0, "j3": 0, "j4": 0}}
    job = robot.play(arg)
    wait(robot, job)
    print(robot.position())
    # Calibrate j3 and j4
    while True:
        choice = input("[Calibrate] Choose: j3, j4, \"save\" to finish calibration, or \"q\" to quit:\n")
        if choice == "q":
            # priming position [90, 30, -120, 0, 0]
            arg = {"command": "move",
                   "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 90, "j1": 40, "j2": -130, "j3": 0,
                           "j4": 0}}
            job = robot.play(arg)
            wait(robot, job)
            return
        elif choice == "save":
            robot.calibrate([90, 0, 0, 0, 0])
            robot.save_config()
            # priming position [90, 30, -120, 0, 0]
            arg = {"command": "move",
                   "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 90, "j1": 40, "j2": -130, "j3": 0,
                           "j4": 0}}
            job = robot.play(arg)
            wait(robot, job)
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
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": 0, "y": 8, "z": 1.5, "a": -90, "b": 180}}
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


def printer_pickup(robot):
    # printer priming position [180, 40, -130, 0, 0]
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

    # Rotate j4 -45 degrees (- rotate in)
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
    job = robot.play(arg)
    wait(robot, job)

    # printer pad priming position, ready to print [90, 50, -130, 0, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 90, "j1": 50, "j2": -130, "j3": 0, "j4": 0}}
    job = robot.play(arg)
    wait(robot, job)


def printer_putback(robot):
    # printer pad priming position, ready to putback [180, 50, -130, 0, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 90, "j1": 50, "j2": -130, "j3": 0, "j4": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # printer priming position [180, 50, -140, 0, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 180, "j1": 40, "j2": -130, "j3": 0, "j4": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # 3D extruder out
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -10.5, "y": 0, "z": 4.3, "a": -90, "b": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # 3D extruder in
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -12.5, "y": 0, "z": 4.2, "a": -90, "b": 0}}
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

    # printer priming position [180, 40, -130, 0, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 180, "j1": 40, "j2": -130, "j3": 0, "j4": 45}}
    job = robot.play(arg)
    wait(robot, job)


def gcode_read(robot):
    with open("C:/Users/zwu22/Downloads/gcode_test3.gcode") as f:
        content = f.readlines()

    gc = []
    job = None

    for i in range(0, len(content)):
        if content[i][0:3] == 'G00' or content[i][0:3] == 'G01':
            gc.append("G91")
            # gc.append("F 60")
            gc.append(content[i])

    for l in gc:
        tmp = {"gc": l}
        job = robot.gcode(tmp)

    wait(robot, job)
    print("job finished!")


def extrude_heat(robot):
    heat_prm = {"command": "set_io", "prm": {"out1": 1, "out2": 0}}
    robot.play(heat_prm)
    # io_out = robot.io()
    # io_out = json.loads(io_out)
    # time.sleep(1)
    # print(io_out)
    # while io_out["in1"] == 0:  # wait for in_out signal from arduino, 0 = temp not ready, 1 = temp ready
    #     # print(io_out["in1"])
    #     time.sleep(0.1)
    #     io_out = robot.io()
    #     io_out = json.loads(io_out)
    print("continue when temp is ready")


def extrude_print(robot):
    heat_and_step_prm = {"command": "set_io", "prm": {"out1": 0, "out2": 1}}
    robot.play(heat_and_step_prm)


def extrude_cool(robot):
    prm = {"command": "set_io", "prm": {"out1": 0, "out2": 0}}
    robot.play(prm)


def print_test(robot):
    # printer pad priming position, ready to print [180, 50, -140, 0, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 90, "j1": 50, "j2": -130, "j3": 0, "j4": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # drop prepare XYZ[0,11,6]
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": 0, "y": 11, "z": 6, "a": -90, "b": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # drop XYZ[0,11,5.22]
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": 0, "y": 11, "z": 5.25, "a": -90, "b": 0}}
    job = robot.play(arg)
    wait(robot, job)

    extrude_print(robot)  # start extruding
    time.sleep(2)

    gcode_read(robot)  # run gcode

    # temp
    heat_prm = {"command": "set_io", "prm": {"out1": 1, "out2": 0}}
    robot.play(heat_prm)
    time.sleep(2)

    # printer pad priming position, ready to print [180, 50, -140, 0, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 90, "j1": 50, "j2": -130, "j3": 0, "j4": 0}}
    job = robot.play(arg)
    wait(robot, job)


def drill_pickup(robot):
    # Drill priming position [180, 40, -130, 0, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 135, "j1": 40, "j2": -130, "j3": 0, "j4": 45}}
    job = robot.play(arg)
    wait(robot, job)

    # Drill pick up drop prime
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -10, "y": 10, "z": 5.5, "a": -90, "b": 45}}
    job = robot.play(arg)
    wait(robot, job)

    # Drill pick up drop in
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 240, "x": -10, "y": 10, "z": 3.4, "a": -90, "b": 45}}
    job = robot.play(arg)
    wait(robot, job)

    # Rotate j4 -45 degrees (- rotate in)
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 1, "speed": 2000, "j0": 0, "j1": 0, "j2": 0, "j3": 0, "j4": -45}}
    job = robot.play(arg)
    wait(robot, job)

    # Drill pick up drop prime
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -10, "y": 10, "z": 5.5, "a": -90, "b": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # Drill rotated priming position [180, 40, -130, 90, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 500, "j0": 135, "j1": 30, "j2": -100, "j3": 90, "j4": 0}}
    job = robot.play(arg)
    wait(robot, job)


def drill_putback(robot):
    # Drill rotated priming position [180, 40, -130, 90, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 1000, "j0": 135, "j1": 30, "j2": -100, "j3": 90, "j4": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # Drill pick up drop prime
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -10, "y": 10, "z": 5.5, "a": -90, "b": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # Drill pick up drop in
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -10, "y": 10, "z": 3.4, "a": -90, "b": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # Rotate j4 45 degrees (+ rotate out)
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 1, "speed": 2000, "j0": 0, "j1": 0, "j2": 0, "j3": 0, "j4": 45}}
    job = robot.play(arg)
    wait(robot, job)

    # Drill pick up drop prime
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 240, "x": -10, "y": 10, "z": 5.5, "a": -90, "b": 45}}
    job = robot.play(arg)
    wait(robot, job)

    # Drill priming position [180, 40, -130, 0, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 2000, "j0": 135, "j1": 40, "j2": -130, "j3": 0, "j4": 45}}
    job = robot.play(arg)
    wait(robot, job)


def drill_test(robot):
    # var for drilling position
    drill_y = 10.62
    drill_z = 3.3
    drill_z_p = 5

    # Drill rotated priming position [135, 40, -130, 90, 0]
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 500, "j0": 135, "j1": 30, "j2": -100, "j3": 90, "j4": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # drill toolhead setting change
    # from '[135, 30, -100, 90.0, 0.0]' to j3=0;
    robot.calibrate([135, 30, -100, 0.0, 0.0])
    robot.set_toolhead({"x": 3})  # drill head

    # drill starting prime
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": 2, "y": drill_y, "z": drill_z_p, "a": -90, "b": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # drill starting point
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": 2, "y": drill_y, "z": drill_z, "a": -90, "b": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # ask user if the feed is enough
    while True:
        user_input = input("[ACTION] Adjust Y by 0.01 in. + or - , \"q\" to exit\n")
        if user_input == "+":
            drill_y = drill_y + 0.01
        elif user_input == "-":
            drill_y = drill_y - 0.01
        elif user_input == "q":
            break
        else:
            print("Invalid input!\n")
            continue
        # move to adjusted position
        arg = {"command": "move",
               "prm": {"path": "line", "movement": 0, "speed": 120, "x": 2, "y": drill_y, "z": drill_z, "a": -90,
                       "b": 0}}
        job = robot.play(arg)
        wait(robot, job)



    # ----- START DRILLING -----
    drill_speed = 10
    # ask user to turn on the drill
    drill_running = input("[ACTION] Please turn on the drill now!\nPress \"y\" to start, \"q\" to abort\n")
    if drill_running == "y":
        print("[WARING]Starting in 5 seconds!!")
        time.sleep(5)
    elif drill_running == "q":
        return

    # drill finish point
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": drill_speed, "x": -2, "y": drill_y, "z": drill_z, "a": -90, "b": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # ask user to turn off the drill
    print("[ACTION] Please turn off the drill now!")
    time.sleep(5)
    # ----- END DRILLING -----

    # drill finish prime
    arg = {"command": "move",
           "prm": {"path": "line", "movement": 0, "speed": 120, "x": -2, "y": drill_y, "z": drill_z_p, "a": -90, "b": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # putback position
    arg = {"command": "move",
           "prm": {"path": "joint", "movement": 0, "speed": 1000, "j0": 135, "j1": 30, "j2": -100, "j3": 0, "j4": 0}}
    job = robot.play(arg)
    wait(robot, job)

    # set toolhead back to nohead
    robot.calibrate([135, 30, -100, 90, 0.0])
    robot.set_toolhead({"x": 1.25})  # no tool


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

    # init io modes
    io_init = {"command": "set_io", "prm": {"out1": 0, "out2": 0, "out3": 0, "out4": 0}}
    robot.play(io_init)
    print("Reset IO\n")

    while True:
        method = input("\nEnter the method you would like to run.\n "
                       "homing, homed, toolhead, calibrate, terminate, position, walkline\n"
                       "Printer control: printer_pickup, printer_putback, print, test_print\n"
                       "Drill control: drill_pickup, drill_putback, drill\n")
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
        elif method == 'printer_pickup':
            printer_pickup(robot)
        elif method == 'printer_putback':
            printer_putback(robot)
        elif method == 'heat':
            extrude_heat(robot)
        elif method == 'test_print':
            extrude_print(robot)
        elif method == 'print':
            print_test(robot)
        elif method == 'cool':
            extrude_cool(robot)
        elif method == 'drill_pickup':
            drill_pickup(robot)
        elif method == 'drill_putback':
            drill_putback(robot)
        elif method == 'drill':
            drill_test(robot)
        else:
            print("Invalid method:", method)


if __name__ == '__main__':
    main()
