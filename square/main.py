#!/usr/bin/env python3

import logging
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, MoveDifferential
from ev3dev2.wheel import EV3EducationSetTire

WHEEL_DISTANCE_MM = 118
MOTOR_SPEED_PERCENT = 25
MOTOR_SPEED_PERCENT_WHEN_TURNING = 15

move_differential = MoveDifferential(
    left_motor_port=OUTPUT_B,
    right_motor_port=OUTPUT_C,
    wheel_class=EV3EducationSetTire,
    wheel_distance_mm=WHEEL_DISTANCE_MM,
    motor_class=LargeMotor
)

logging.basicConfig(filename='robot.log')

def move_forward(distance_cm: float, speed=MOTOR_SPEED_PERCENT, brake=True):
    # move_differential.on_for_distance(distance_mm=distance_cm * 10, speed=speed, brake=brake)
    move_differential.on_to_coordinates(x_target_mm=0, y_target_mm=distance_cm * 10.0, speed=speed, brake=brake)
    # logging.debug('position = %s', move_differential.position)


def turn_left(degrees: float, speed=MOTOR_SPEED_PERCENT_WHEN_TURNING, brake=True):
    move_differential.turn_left(degrees=degrees, speed=speed, brake=brake)

def turn_right(degrees: float, speed=MOTOR_SPEED_PERCENT_WHEN_TURNING, brake=True):
    move_differential.turn_right(degrees=degrees, speed=speed, brake=brake)

def turn_to_angle(degrees: float, speed=MOTOR_SPEED_PERCENT_WHEN_TURNING, brake=True):
    move_differential.turn_to_angle(angle_target_degrees=degrees, speed=speed, brake=brake)


def move_square(side_length_cm: float, laps: int = 1, direction: str = 'clockwise'):
    for _ in range(4 * laps):
        move_forward(distance_cm=side_length_cm)
        if direction == 'clockwise':
            # turn_right(degrees=90)
            turn_to_angle(degrees=-90)
        elif direction == 'counterclockwise':
            # turn_left(degrees=90)
            turn_to_angle(degrees=0)
        else:
            raise ValueError('direction must be either clockwise or counterclockwise')


if __name__ == '__main__':
    move_differential.odometry_start()
    move_square(side_length_cm=100, laps=10)
    move_square(side_length_cm=100, laps=10, direction='counterclockwise')
    move_differential.odometry_stop()
