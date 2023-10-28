## Desarrollo de la práctica 3

### 1. Movimiento de ambos motores a la vez

En un principio, conseguimos hacer que el robot se moviera hacia adelante
utilizando hilos para mover los motores
izquiero y derecho a la vez. El resultado parecía ser el esperado, el robot
se movía hacia delante aproximadamente un metro (3 baldosas). Se utilizó el
siguiente código:

```python
#!/usr/bin/env python3

import math
from functools import partial
from threading import Thread

from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C

WHEEL_DIAMETER_IN_CENTIMETERS = 5.6
MOTOR_SPEED_PERCENT = 25

left_motor = LargeMotor(OUTPUT_B)
right_motor = LargeMotor(OUTPUT_C)


def move_left_motor(speed: float, rotations: float):
    left_motor.on_for_rotations(speed=speed, rotations=rotations)


def move_right_motor(speed: float, rotations: float):
    right_motor.on_for_rotations(speed=speed, rotations=rotations)


def move_forward(speed: float, centimeters: float):
    rotations = centimeters / (WHEEL_DIAMETER_IN_CENTIMETERS * math.pi)
    left_motor_thread = Thread(target=move_left_motor,
                               kwargs=dict(speed=speed, rotations=rotations))
    right_motor_thread = Thread(target=move_right_motor,
                                kwargs=dict(speed=speed, rotations=rotations))
    left_motor_thread.start()
    right_motor_thread.start()
    left_motor_thread.join()
    right_motor_thread.join()


move_forward_one_meter = partial(move_forward, speed=MOTOR_SPEED_PERCENT,
                                 centimeters=100)

if __name__ == '__main__':
    move_forward_one_meter()
    left_motor.off()
    right_motor.off()

```

### 2. Refactorización 

Como utilizar hilos suponía una complejidad añadida y hacía que el código fuera considerablemente
más largo, decidimos utilizar el parámetro `block` de la función `on_for_rotations` para conseguir
el mismo resultado.

```python
#!/usr/bin/env python3

import math
from functools import partial

from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C

WHEEL_DIAMETER_IN_CENTIMETERS = 5.6
MOTOR_SPEED_PERCENT = 25

left_motor = LargeMotor(OUTPUT_B)
right_motor = LargeMotor(OUTPUT_C)


def move_left_motor(speed: float, rotations: float, block=True):
    left_motor.on_for_rotations(speed=speed, rotations=rotations, block=block)


def move_right_motor(speed: float, rotations: float, block=True):
    right_motor.on_for_rotations(speed=speed, rotations=rotations, block=block)


def move_forward(speed: float, centimeters: float):
    rotations = centimeters / (WHEEL_DIAMETER_IN_CENTIMETERS * math.pi)
    move_left_motor(speed=speed, rotations=rotations, block=False)
    move_right_motor(speed=speed, rotations=rotations)


move_forward_one_meter = partial(move_forward, speed=MOTOR_SPEED_PERCENT, centimeters=100)

if __name__ == '__main__':
    move_forward_one_meter()
    left_motor.off()
    right_motor.off()

```

### 3. Movimiento formando un cuadrado de 1 metro de lado

A continuación, se procedió a incluir el código necesario para que el robot moviera sus ruedas 
en sentidos opuestos, pudiendo girar sobre sí mismo. En consecuencia, se consiguió que el robot
se moviera en forma de cuadrado de 1 metro de lado. El robot gira 90 grados a la izquierda y se mueve
hacia delante 1 metro, repitiendo este proceso 4 veces. 

```python
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

```

