#!/usr/bin/env python3

import math
from functools import partial
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, MoveTank, MoveSteering
from time import sleep

WHEEL_DIAMETER = 5.6
FORWARD_SPEED = 25
TURN_SPEED = 10
ONE_METER_ROTATIONS = 100 / (WHEEL_DIAMETER * math.pi)
LEFT_TURN_ROTATIONS = (AXIS_CIRCUMFERENCE * angle / 360) / (WHEEL_DIAMETER * math.pi)
AXIS = 11.8
AXIS_CIRCUMFERENCE = AXIS * math.pi

left_motor = LargeMotor(OUTPUT_B)
right_motor = LargeMotor(OUTPUT_C)
tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)
steering_pair = MoveSteering(OUTPUT_B, OUTPUT_C)

def move_left_motor(speed: float, rotations: float, block=True, brake=True):
     left_motor.on_for_rotations(speed=speed, rotations=rotations, block=block, brake=brake)

def move_right_motor(speed: float, rotations: float, block=True, brake=True):
    right_motor.on_for_rotations(speed=speed, rotations=rotations, block=block, brake=brake)

def move_forward(speed: float, rotations: float, brake=True):
    # move_left_motor(speed=speed, rotations=rotations, block=False, brake=brake)
    # move_right_motor(speed=speed, rotations=rotations, brake=brake)
    tank_pair.on_for_rotations(left_speed=speed, right_speed=speed, rotations=rotations, brake=brake)

def turn(speed: float, angle: float):
    # move_left_motor(speed=speed, rotations=-rotations, block=False)
    # move_right_motor(speed=speed, rotations=rotations)
    steering_pair.on_for_rotations(steering=100, speed=speed, degrees=angle)


move_forward_one_meter = partial(move_forward, speed=FORWARD_SPEED, rotations=ONE_METER_ROTATIONS)

def draw_one_meter_square():
    for _ in range(4):
        move_forward_one_meter()
        turn(TURN_SPEED, 90)

if __name__ == '__main__':
    draw_one_meter_square()
    left_motor.off()
    right_motor.off()
