#!/usr/bin/env python3

import math
from functools import partial

from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C

WHEEL_DIAMETER_IN_CENTIMETRES = 5.6
AXLE_IN_CENTIMETERS = 11.8
AXLE_CIRCUMFERENCE_IN_CENTIMETERS = AXLE_IN_CENTIMETERS * math.pi
MOTOR_SPEED_PERCENT = 25
MOTOR_SPEED_PERCENT_WHEN_TURNING = 10

left_motor = LargeMotor(OUTPUT_B)
right_motor = LargeMotor(OUTPUT_C)


def move_left_motor(speed: float, rotations: float, block=True, brake=True):
    left_motor.on_for_rotations(speed=speed, rotations=rotations, block=block, brake=brake)


def move_right_motor(speed: float, rotations: float, block=True, brake=True):
    right_motor.on_for_rotations(speed=speed, rotations=rotations, block=block, brake=brake)


def move_forward(speed: float, centimeters: float, brake=True):
    rotations = centimeters / (WHEEL_DIAMETER_IN_CENTIMETRES * math.pi)
    move_left_motor(speed=speed, rotations=rotations, block=False, brake=brake)
    move_right_motor(speed=speed, rotations=rotations, brake=brake)


def turn(speed: float, degrees: float):
    rotations = (AXLE_CIRCUMFERENCE_IN_CENTIMETERS * degrees / 360) / (WHEEL_DIAMETER_IN_CENTIMETRES * math.pi)
    move_left_motor(speed=speed, rotations=-rotations, block=False)
    move_right_motor(speed=speed, rotations=rotations)


move_forward_one_meter = partial(move_forward, speed=MOTOR_SPEED_PERCENT, centimeters=100)
turn_left_90_degrees = partial(turn, speed=MOTOR_SPEED_PERCENT_WHEN_TURNING, degrees=90)


def draw_one_meter_square():
    for _ in range(4):
        move_forward_one_meter()
        turn_left_90_degrees()


if __name__ == '__main__':
    draw_one_meter_square()
    left_motor.off()
    right_motor.off()
