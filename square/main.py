#!/usr/bin/env python3

import math
from functools import partial

from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C

WHEEL_DIAMETER = 5.6
AXIS = 11.8
AXIS_CIRCUMFERENCE = AXIS * math.pi
FORWARD_SPEED = 25
TURN_SPEED = 10

left_motor = LargeMotor(OUTPUT_B)
right_motor = LargeMotor(OUTPUT_C)


def move_left_motor(speed: float, rotations: float, block=True, brake=True):
    left_motor.on_for_rotations(speed=speed, rotations=rotations, block=block, brake=brake)


def move_right_motor(speed: float, rotations: float, block=True, brake=True):
    right_motor.on_for_rotations(speed=speed, rotations=rotations, block=block, brake=brake)


def move_forward(speed: float, centimeters: float, brake=True):
    rotations = centimeters / (WHEEL_DIAMETER * math.pi)
    move_left_motor(speed=speed, rotations=rotations, block=False, brake=brake)
    move_right_motor(speed=speed, rotations=rotations, brake=brake)


def turn(speed: float, degrees: float):
    rotations = (AXIS_CIRCUMFERENCE * degrees / 360) / (WHEEL_DIAMETER * math.pi)
    move_left_motor(speed=speed, rotations=-rotations, block=False)
    move_right_motor(speed=speed, rotations=rotations)


move_forward_one_meter = partial(move_forward, speed=FORWARD_SPEED, centimeters=100)
turn_left_90_degrees = partial(turn, speed=TURN_SPEED, degrees=90)


def draw_one_meter_square():
    for _ in range(4):
        move_forward_one_meter()
        turn_left_90_degrees()


if __name__ == '__main__':
    draw_one_meter_square()
    left_motor.off()
    right_motor.off()
