# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       rapid                                                        #
# 	Created:      11/16/2026, 3:59:50 PM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #


from vex import *

is_claw_open = False
is_Toggle_spiining = False
is_LiftUp = False


brain = Brain()
leftMotorA = Motor(Ports.PORT1, GearSetting.RATIO_6_1, True)
leftMotorB = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)
rightMotorA = Motor(Ports.PORT4, GearSetting.RATIO_6_1, False)
rightMotorB = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
LeftliftMotor = Motor(Ports.PORT7, GearSetting.RATIO_36_1, True)
RightliftMotor = Motor(Ports.PORT8, GearSetting.RATIO_36_1)
ToggleMotor = Motor(Ports.PORT9, GearSetting.RATIO_18_1)

# IntakeMotor = Motor(Ports.PORT9, GearSetting.RATIO_6_1)
leftMotors = MotorGroup(leftMotorA, leftMotorB)
rightMotors = MotorGroup(rightMotorA, rightMotorB)
IMU = Inertial(Ports.PORT21)
drivetrain = SmartDrive(leftMotors, rightMotors,IMU)
controller_1 = Controller()
liftMotorsGroup = MotorGroup(LeftliftMotor,RightliftMotor)
claw_pneumatic = Pneumatics(brain.three_wire_port.g)
rotator_pneumatic = Pneumatics(brain.three_wire_port.d)
TagSensor = AiVision(Ports.PORT6,AiVision.ALL_AIOBJS)
Optical_Sensor = Optical(Ports.PORT15)
selected_autonmous = 0

# class PIDController:
    # def __init__(self, kp, ki, kd, max_integral=50):
        # self.kp = kp
        # self.ki = ki
        # self.kd = kd
        # self.max_integral = max_integral
        # self.integral = 0
        #self.prev_error = 0
    # def calculate(self, error):
        # self.integral += error
        # self.integral = max(-self.max_integral, min(self.max_integral, self.integral))
        # derivative = error - self.prev_error
        # self.prev_error = error
        # return self.kp * error + self.ki * self.integral + self.kd * derivative
    # def reset(self):
        # self.integral = 0
        # self.prev_error = 0



def FlipToggle(): # pyright: ignore[reportSelfClsParameterName]
    brain.timer.reset()
    Optical_Sensor.set_light(LedStateType.ON)
    leftMotors.spin(FORWARD,5,PERCENT)
    rightMotors.spin(FORWARD,10,PERCENT)
    # while  Optical_Sensor.color() != Color.RED:
    while brain.timer.time(SECONDS) < 0.7:
        ToggleMotor.spin(FORWARD,50, PERCENT)
        wait(10)
    ToggleMotor.stop(BRAKE)
    leftMotors.stop()
    leftMotors.stop()
    Optical_Sensor.set_light(LedStateType.OFF)

def BrainTouched():
    brain.screen.clear_screen()
    global selected_autonmous 
    selected_autonmous += 1
    if selected_autonmous == 1:
        brain.screen.print_at(" fifteen second autonmous.", x=20, y=20)
    elif selected_autonmous == 2:
        brain.screen.print_at(" one minute autonmous.", x=20, y=20)
    else:
        selected_autonmous = 1
        brain.screen.print_at(" fifteen second autonmous.", x=20, y=20)
    



def toggle_auton():
    global selected_autonmous
    selected_autonmous =+ 1
    print(selected_autonmous)
    if selected_autonmous > 1:
        selected_autonmous = 0
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    if selected_autonmous == 0:
        brain.screen.print("15 second auton")
    elif selected_autonmous == 1:
        brain.screen.print("1 minute auton")

brain.screen.pressed(BrainTouched)






# Wrap you autonmous functions into a loop.
# Wrap all of functions into a loop.
def autonomous():
    # claw_rotateUp()
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    
    drivetrain.set_timeout(3, SECONDS)
    drivetrain.set_drive_velocity(50, PERCENT)
    drivetrain.set_turn_velocity(10, PERCENT)
    selected_autonmous = 2 # For right now for toggling between the 15 second and 1 a minute autonomous periods choose 1 one four fifteen second autonomous and two for one minute autonomous.
    if selected_autonmous == 1:
        fiften_sec_autonomous()
    elif selected_autonmous == 2:
        one_minute_autonmous(3)


    # LiftUp()
    # drivetrain.turn_for(RIGHT,45,DEGREES)
    # drivetrain.drive_for(FORWARD,6,INCHES)
    # # claw_close()
    # drivetrain.turn_for(RIGHT,65,DEGREES)
    # drivetrain.drive_for(FORWARD,24,INCHES)
    # LiftDown()
    # claw_open()
    return
    # This is the rest of the autonomous function that will test on friday See lines up above
    # drivepid = PIDController(kp=0.8, ki = 0.002, kd = 0.1)


    return
    # driving and tuning the pid
    # PIDController(kp = 1.5, ki= 0.003, kd = 0.2)


    def pid_drive(target_inches):
# Move forward via the PID
        drive.pid.reset()
       
       
   
           
        LiftUp()
    drivetrain.drive_for(FORWARD, 18, INCHES)
    LiftDown()
    # place automonous code here
    Intake()
    drivetrain.drive_for(FORWARD, 24, INCHES)
    drivetrain.turn_for(RIGHT,45, DEGREES)
    drivetrain.drive_for(FORWARD,8,INCHES)
    claw_open()
    wait(3.5,SECONDS)
    claw_close()
    drivetrain.set_drive_velocity(50, PERCENT)
    drivetrain.drive_for(REVERSE,6, INCHES)
    claw_rotateDown()
    wait(2, SECONDS)
    IntakeStop()
    claw_close()
    claw_rotateUp()














    # drivetrain.turn_for(LEFT,90)
    # drivetrain.drive_for(FORWARD,18, INCHES)
    # LiftDown()
    # claw_open()
    # drivetrain.drive_for(REVERSE,6, INCHES)
    # drivetrain.turn_for(RIGHT, 90)
    # drivetrain.drive_for(FORWARD,12, INCHES)
    # claw_close()
    # LiftUp()
    # drivetrain.turn_for(LEFT,90)
    # drivetrain.drive_for(FORWARD,18, INCHES)
    # drivetrain.drive_for(REVERSE,8,INCHES)
    # drivetrain.turn_for(RIGHT,85)
    # drivetrain.drive_for(FORWARD,12,INCHES)
    # claw_close()
    # LiftUp()
    # drivetrain.turn_for(LEFT,180)
    # drivetrain.drive_for(FORWARD, 12,INCHES)
   


    LiftDown()
    claw_open()


    Intake()
    PickUpPin()




def PickUp_Pin():
    if is_claw_open:
         drivetrain.drive_for(FORWARD,2, INCHES)
    elif claw_close:
         pass

def fiften_sec_autonomous():
    drivetrain.drive_for(FORWARD, 4, INCHES)
    FlipToggle()
    drivetrain.drive_for(REVERSE, 5,INCHES)
    LiftUp(1)
    claw_rotateDown()
    drivetrain.drive_for(REVERSE,3, INCHES)
    drivetrain.turn_for(RIGHT,205,DEGREES)
    drivetrain.drive_for(FORWARD,32,INCHES)
    LiftDown()
    claw_open()
    LiftUp() # Comment this Line out.
    # Second pin autonmous
    drivetrain.drive_for(REVERSE,10,INCHES)
    drivetrain.turn_for(LEFT,48,DEGREES)

    LiftDown()
    drivetrain.drive_for(FORWARD,20,INCHES)
    drivetrain.turn_for(RIGHT,15,DEGREES)
    drivetrain.set_drive_velocity(25)
    drivetrain.drive_for(FORWARD,8,INCHES)
    LiftDown()
    claw_close()



def one_minute_autonmous(FORWARD):
        
        if FORWARD <= 32:
            print("Finished!")
            return
        else:
            print(FORWARD)
            one_minute_autonmous(FORWARD - 1)


            drivetrain.set_timeout(3, SECONDS)
            drivetrain.set_drive_velocity(50, PERCENT)
            drivetrain.set_turn_velocity(10, PERCENT)
            
            
            drivetrain.drive_for(FORWARD, 4, INCHES)
            FlipToggle()
            drivetrain.drive_for(REVERSE, 5,INCHES)
            LiftUp(1)
            drivetrain.drive_for(REVERSE,3, INCHES)
            drivetrain.turn_for(RIGHT,185,DEGREES)
            drivetrain.drive_for(FORWARD,28,INCHES)
            LiftDown()
            claw_open()
            # Second pin autonmous
            LiftUp() # Comment this Line out.
            drivetrain.drive_for(REVERSE,10,INCHES)
            drivetrain.turn_for(LEFT,45,DEGREES)
            LiftDown()
            drivetrain.drive_for(FORWARD,20,INCHES)
            drivetrain.set_drive_velocity(25)
            drivetrain.drive_for(FORWARD,8,INCHES)
            return
            LiftDown()
            claw_close()


def LiftUp(turns=0.7):   
    liftMotorsGroup.spin_for(FORWARD,turns,TURNS)
    # Then pick up the pin
def PickUpPin():
    pass    


def LiftDown():
    liftMotorsGroup.spin_for(REVERSE,0.7,TURNS)


def Intake():


     IntakeStop.set_velocity(75, PERCENT)
     IntakeStop.spin(FORWARD)
    #  IntakeMotor.spin_for(FORWARD,3, SECONDS, wait=False)


def IntakeStop():
    IntakeStop.stop()


def Outake():
    IntakeStop.spin_for(REVERSE,3, SECONDS)
def claw_open():
    global is_claw_open
    claw_pneumatic.open()
    is_claw_open = True


def claw_close():
    claw_pneumatic.close()
    global is_claw_open
    is_claw_open = False
def claw_rotateUp():
    rotator_pneumatic.close()

   


def claw_rotateDown():
    rotator_pneumatic.open()




     




def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control hey")
    # place driver control in this while loop
    while True:
       
       
       
        # add a deadband to controller joysticks
        horizontal = controller_1.axis1.position()
        vertical = controller_1.axis3.position()
        if abs(horizontal) < 5:
            horizontal = 0
        if abs(vertical) < 5:
            vertical = 0
        leftMotors.spin(FORWARD, vertical + horizontal, PERCENT)
        rightMotors.spin(FORWARD, vertical - horizontal, PERCENT)
        if controller_1.buttonR1.pressing():
            liftMotorsGroup.spin(FORWARD, 50, PERCENT)
        elif controller_1.buttonR2.pressing():
            liftMotorsGroup.spin(REVERSE, 50, PERCENT)
        else:
            liftMotorsGroup.stop(HOLD)
            # pneumatic claw
        if controller_1.buttonY.pressing():
            claw_pneumatic.open()
        elif controller_1.buttonB.pressing():
            claw_pneumatic.close()
        if controller_1.buttonRight.pressing():
            claw_rotateUp()
        elif controller_1.buttonDown.pressing():
            claw_rotateDown()
        # if controller_1.buttonL1.pressing():
            # ToggleMotor.spin(FORWARD, 50, PERCENT)
        # elif controller_1.buttonL2.pressing():
            # ToggleMotor.spin(REVERSE, 50 ,PERCENT)
        # else:
            # ToggleMotor.stop()
        # wait(20, MSEC)






# create competition instance
comp = Competition(user_control, autonomous)


# actions to do when the program starts
brain.screen.clear_screen()
