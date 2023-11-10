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

### 4. Uso de MoveDifferential y ampliación de movimiento en cuadrado

La librería `ev3dev2` proporciona una clase denominada MoveDifferential, que permite al robot moverse hacia delante una cierta distancia y girar sobre sí mismo en un ángulo determinado, entre otras acciones, sin necesidad de utilizar los dos motores por separado ni realizar los cálculos manualmente. Utilizando esta nueva herramienta, el robot se comporta de manera idéntica y el código se simplifica considerablemente.
Además, se modificó la función `move_square` (previamente llamada `draw_one_meter_square`) para poder especificar el número de vueltas y el sentido, horario o antihorario, en que el robot realiza el movimiento en forma de cuadrado. El código resultante es el siguiente:

```python
#!/usr/bin/env python3

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


def move_forward(distance_cm: float, speed=MOTOR_SPEED_PERCENT, brake=True):
    move_differential.on_for_distance(distance_mm=distance_cm * 10, speed=speed, brake=brake)


def turn_left(degrees: float, speed=MOTOR_SPEED_PERCENT_WHEN_TURNING, brake=True):
    move_differential.turn_left(degrees=degrees, speed=speed, brake=brake)


def turn_right(degrees: float, speed=MOTOR_SPEED_PERCENT_WHEN_TURNING, brake=True):
    move_differential.turn_right(degrees=degrees, speed=speed, brake=brake)


def move_square(side_length_cm: float, laps: int = 1, direction: str = 'clockwise'):
    for _ in range(4 * laps):
        move_forward(distance_cm=side_length_cm)
        if direction == 'clockwise':
            turn_right(degrees=90)
        elif direction == 'counterclockwise':
            turn_left(degrees=90)
        else:
            raise ValueError('direction must be either clockwise or counterclockwise')


if __name__ == '__main__':
    move_square(side_length_cm=100, laps=10)
    move_square(side_length_cm=100, laps=10, direction='counterclockwise')

```

### 5. Resultados

Al realizar recorridos en forma de cuadrado, 10 en sentido horario y otros 10 en sentido antihorario, la conclusión es clara. Existe error sistemático debido a la imprecisión de la medida de la distancia entre las ruedas. Dado que la superficie de apoyo de las ruedas es considerablemente ancha, es muy difícil medir exactamente qué distancia existe entre dichas superficies. Es por ello que, al girar el robot sobre sí mismo, este efectúa la rotación con un ángulo aproximadamente un 10% menor al deseado, que es de 90º. En el primer giro no es demasiado apreciable, pero al acumularse en los cuatro giros del cuadrado, el error es muy claramente perceptible. 
\
&nbsp;&nbsp;&nbsp;&nbsp;No obstante, todo apunta a que el error de la medida del diámetro de las ruedas es sumamente bajo, puesto que el robot realiza el movimiento hacia delante en una recta casi perfecta y recorre una distancia muy próxima a 1 metro.

