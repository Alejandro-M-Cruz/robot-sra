#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, MoveDifferential
from ev3dev2.wheel import EV3EducationSetTire

WHEEL_DISTANCE_MM = 92
MOTOR_SPEED_PERCENT = 40
MOTOR_SPEED_PERCENT_WHEN_TURNING = 15

move_differential = MoveDifferential(
    left_motor_port=OUTPUT_B,
    right_motor_port=OUTPUT_C,
    wheel_class=EV3EducationSetTire,
    wheel_distance_mm=WHEEL_DISTANCE_MM,
    motor_class=LargeMotor
)


def move_forward(distance_cm: float, speed=MOTOR_SPEED_PERCENT, brake=True):
    move_differential.on_for_distance(distance_mm=distance_cm * 10, speed=speed, brake=brake)


def turn_left(degrees: float, speed=MOTOR_SPEED_PERCENT_WHEN_TURNING, brake=True):
    move_differential.turn_left(degrees=degrees, speed=speed, brake=brake)


def turn_right(degrees: float, speed=MOTOR_SPEED_PERCENT_WHEN_TURNING, brake=True):
    move_differential.turn_right(degrees=degrees, speed=speed, brake=brake)


def move_square(side_length_cm: float):
    for _ in range(4):
        move_forward(distance_cm=side_length_cm)
        turn_left(degrees=90)


if __name__ == '__main__':
    move_square(side_length_cm=100)
