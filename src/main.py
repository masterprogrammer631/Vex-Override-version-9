# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       rapid                                                        #
# 	Created:      11/16/2026, 3:59:50 PM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

brain = Brain()
controller_1 = Controller()
# instantiate motors and groups
left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_6_1, True)
left_motor_b = Motor(Ports.PORT12, GearSetting.RATIO_6_1, True)
right_motor_a = Motor(Ports.PORT4, GearSetting.RATIO_6_1, False)
right_motor_b = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
left_lift_motor = Motor(Ports.PORT7, GearSetting.RATIO_36_1, True)
right_lift_motor = Motor(Ports.PORT8, GearSetting.RATIO_36_1)
toggle_motor = Motor(Ports.PORT9, GearSetting.RATIO_18_1)
left_drive = MotorGroup(left_motor_a, left_motor_b)
right_drive = MotorGroup(right_motor_a, right_motor_b)
lift_motor = MotorGroup(left_lift_motor, right_lift_motor)
# instantiate pneumatics
claw_pneumatic = Pneumatics(brain.three_wire_port.g)
rotator_pneumatic = Pneumatics(brain.three_wire_port.d)
# instantiate sensors
ai_vision = AiVision(Ports.PORT6, AiVision.ALL_TAGS, AiVision.ALL_AIOBJS)
imu = Inertial(Ports.PORT21)
optical_sensor = Optical(Ports.PORT15)
# instantiate Smart drivetrain for autonomous
drivetrain = SmartDrive(left_drive, right_drive, imu, 83, 292, 330, MM, 2.33)
# global variables
selected_autonomous = 1 # 1 = Red 1, 2 = Red 2, 3 = Blue 1, 4 = Blue 2, 5 = Skills
# AI Vision Override constants
OBJECT = 0
TAG = 1
RED_BLUE_PIN = 0
BLUE_YELLOW_PIN = 1
RED_YELLOW_PIN = 2
YELLOW_PIN = 3
CUP = 4

# cycle through the 5 autonomous options
def brain_touched():
    global selected_autonomous
    selected_autonomous += 1
    if selected_autonomous > 5:
        selected_autonomous = 1

# show the selected auton on the brain screen
def show_auton_selection():
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(3, 10)
        brain.screen.set_font(FontType.MONO40)
        if selected_autonomous == 1:
            brain.screen.set_fill_color(Color.RED)
            brain.screen.print(" Red 1 ")
        elif selected_autonomous == 2:
            brain.screen.set_fill_color(Color.RED)
            brain.screen.print(" Red 2 ")
        elif selected_autonomous == 3:
            brain.screen.set_fill_color(Color.BLUE)
            brain.screen.print(" Blue 1 ")
        elif selected_autonomous == 4:
            brain.screen.set_fill_color(Color.BLUE)
            brain.screen.print(" Blue 2 ")
        elif selected_autonomous == 5:
            brain.screen.set_fill_color(Color.GREEN)
            brain.screen.print(" Skills ")
        wait(500)

# AI Vision function to drive to desired target game element
def drive_to_target(type, id, timeout=5):
    center_offset = 160
    max_forward_velocity = 90
    max_turning_velocity = 40
    target_forward_offset = 0
    target_turning_offset = 0
    target_reached = False
    brain.timer.reset()
    while not target_reached:
        located_target = None
        if type == 0:
            # detect pins and cups sorted by largest area
            target_area = 7000
            objects = sorted(ai_vision.take_snapshot(AiVision.ALL_AIOBJS), key=lambda k: k.width * k.height, reverse=True)
            for obj in objects:
                if obj.id == id:
                    located_target = obj
                    break
        elif type == 1:
            # detect April tags sorted by largest area
            target_area = 400
            tags = sorted(ai_vision.take_snapshot(AiVision.ALL_TAGS), key=lambda k: k.width * k.height, reverse=True)
            for tag in tags:
                if tag.id == id:
                    located_target = tag
                    break
        if located_target:
            target_forward_offset = 1 - located_target.width * located_target.height / target_area
            target_turning_offset = (located_target.centerX - center_offset) / center_offset
            if target_forward_offset <= 0.01:
                target_reached = True
        else:
            target_forward_offset = 0
            target_turning_offset = 0
        left_drive.spin(FORWARD, max_forward_velocity * target_forward_offset + max_turning_velocity * target_turning_offset)
        right_drive.spin(FORWARD, max_forward_velocity * target_forward_offset - max_turning_velocity * target_turning_offset)
        if brain.timer.time(SECONDS) > timeout:
            break
        sleep(100)
    left_drive.stop(BRAKE)
    right_drive.stop(BRAKE)

def lift_up(turns=1.0):   
    lift_motor.spin_for(FORWARD, turns, TURNS)

def lift_down(turns=1.0):
    lift_motor.spin_for(REVERSE, turns, TURNS)

def claw_open():
    claw_pneumatic.open()

def claw_close():
    claw_pneumatic.close()

def claw_up():
    # claw out facing foward for upright cups/pins
    rotator_pneumatic.open()

def claw_down():
    # claw tucked in facing down
    rotator_pneumatic.close()

# flip toggle until desired color is reached
def flip_toggle(color, timeout=4):
    brain.timer.reset()
    optical_sensor.set_light(LedStateType.ON)
    left_drive.spin(FORWARD, 2, PERCENT)
    right_drive.spin(FORWARD, 2, PERCENT)
    while optical_sensor.color() != color and brain.timer.time(SECONDS) < timeout:
        toggle_motor.spin(FORWARD, 50, PERCENT)
        wait(250)
    toggle_motor.stop()
    left_drive.stop()
    right_drive.stop()
    optical_sensor.set_light(LedStateType.OFF)

def autonomous():
    if selected_autonomous == 1:
        red1_auton()
    elif selected_autonomous == 2:
        red2_auton()
    elif selected_autonomous == 3:
        blue1_auton()
    elif selected_autonomous == 4:
        blue2_auton()
    elif selected_autonomous == 5:
        skills(3)

def red1_auton():
    # flip toggle to red
    flip_toggle(Color.RED)
    drivetrain.drive_for(REVERSE, 6, INCHES)
    # score preload pin in red goal #2
    lift_up()
    claw_up()
    drivetrain.turn_for(RIGHT, 195, DEGREES)
    drivetrain.drive_for(FORWARD, 18, INCHES)
    lift_down()
    claw_open()
    drivetrain.drive_for(REVERSE, 10, INCHES)
    # grab second cup and pin and score on top of goal #2
    drivetrain.turn_for(LEFT, 40, DEGREES)
    drivetrain.drive_for(FORWARD, 18, INCHES)
    drivetrain.drive_for(FORWARD, 7, INCHES, 20, PERCENT)
    claw_close()
    lift_up()
    drivetrain.turn_for(RIGHT, 125, DEGREES)
    drivetrain.drive_for(FORWARD, 12, INCHES, 30, PERCENT)
    lift_down(0.5)
    claw_open()

def red2_auton():
    # TODO: code quadrant 2
    pass

def blue1_auton():
    # flip toggle to blue
    flip_toggle(Color.BLUE)
    drivetrain.drive_for(REVERSE, 6, INCHES)
    # score preload pin in red goal #2
    lift_up()
    claw_up()
    drivetrain.turn_for(RIGHT, 195, DEGREES)
    drivetrain.drive_for(FORWARD, 18, INCHES)
    lift_down()
    claw_open()
    drivetrain.drive_for(REVERSE, 10, INCHES)
    # grab second cup and pin and score on top of goal #2
    drivetrain.turn_for(LEFT, 40, DEGREES)
    drivetrain.drive_for(FORWARD, 18, INCHES)
    drivetrain.drive_for(FORWARD, 7, INCHES, 20, PERCENT)
    claw_close()
    lift_up()
    drivetrain.turn_for(RIGHT, 125, DEGREES)
    drivetrain.drive_for(FORWARD, 12, INCHES, 30, PERCENT)
    lift_down(0.5)
    claw_open()

def blue2_auton():
    # TODO: code quadrant 2
    pass

def skills(pin_count):
    if pin_count == 0:
        print("Finished!")
        return
    else:
        print(pin_count)
        drive_to_target(OBJECT, YELLOW_PIN)
        drive_to_target(TAG, 2)
        return skills(pin_count - 1)

def user_control():
    while True:
        # add a deadband to controller joysticks
        horizontal = controller_1.axis1.position()
        vertical = controller_1.axis3.position()
        if abs(horizontal) < 5:
            horizontal = 0
        if abs(vertical) < 5:
            vertical = 0
        # move drivetrain according to joystick positions
        left_drive.spin(FORWARD, vertical + horizontal, PERCENT)
        right_drive.spin(FORWARD, vertical - horizontal, PERCENT)
        # controls for lift up and down
        if controller_1.buttonR1.pressing():
            lift_motor.spin(FORWARD, 50, PERCENT)
        elif controller_1.buttonR2.pressing():
            lift_motor.spin(REVERSE, 50, PERCENT)
        else:
            lift_motor.stop(HOLD)
        # controls for claw open, close, up and down
        if controller_1.buttonY.pressing():
            claw_pneumatic.open()
        elif controller_1.buttonB.pressing():
            claw_pneumatic.close()
        if controller_1.buttonRight.pressing():
            rotator_pneumatic.open()
        elif controller_1.buttonDown.pressing():
            rotator_pneumatic.close()
        # controls for toggle flipper
        if controller_1.buttonL1.pressing():
            # rotate toggle up
            toggle_motor.spin(FORWARD, 50, PERCENT)
        elif controller_1.buttonL2.pressing():
            # rotate toggle down
            toggle_motor.spin(REVERSE, 50 ,PERCENT)
        else:
            toggle_motor.stop()
        wait(20)

# make sure inertial sensor is fully calibrated before running code
while imu.is_calibrating():
    wait(20)
# create competition instance
comp = Competition(user_control, autonomous)
# set up callback for when brain screen is touched
brain.screen.pressed(brain_touched)
# set default timeout and speeds for autonomous
drivetrain.set_timeout(5, SECONDS)
drivetrain.set_drive_velocity(90, PERCENT)
drivetrain.set_turn_velocity(80, PERCENT)
# set default timeout for lift in autonomous
lift_motor.set_timeout(3, SECONDS)
# start function to show selected auton in a dedicated thread
Thread(show_auton_selection)
