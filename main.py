from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import math


app = Ursina()

# --------------------------------------------------
# WORLD
# --------------------------------------------------

ground = Entity(
    model='plane',
    scale=100,
    texture='white_cube',
    texture_scale=(100, 100),
    color=color.green,
    collider='box'
)

Sky()


# --------------------------------------------------
# DRONE
# --------------------------------------------------

drone = Entity(
    model='cube',
    color=color.orange,
    scale=(1.5, 0.3, 1.5),
    position=(0, 2, 0)
)

# Drone body
Entity(
    parent=drone,
    model='cube',
    color=color.dark_gray,
    scale=(0.5, 0.25, 0.5),
    y=0.25
)


# --------------------------------------------------
# PHYSICS
# --------------------------------------------------

velocity = Vec3(0, 0, 0)

gravity = 9.81
throttle = 0.5

max_throttle = 1.0
min_throttle = 0.0

lift_strength = 20
movement_speed = 8


# --------------------------------------------------
# HUD
# --------------------------------------------------

altitude_text = Text(
    text='Altitude: 0.0 m',
    position=(-0.85, 0.45),
    scale=1.2
)

throttle_text = Text(
    text='Throttle: 50%',
    position=(-0.85, 0.40),
    scale=1.2
)

help_text = Text(
    text='SPACE/SHIFT: Throttle   W/S: Pitch   A/D: Roll   Q/E: Yaw',
    position=(-0.85, -0.45),
    scale=0.9
)


# --------------------------------------------------
# UPDATE
# --------------------------------------------------

def update():

    global throttle, velocity

    dt = time.dt

    # ------------------------------
    # THROTTLE
    # ------------------------------

    if held_keys['space']:
        throttle += dt * 0.5

    if held_keys['shift']:
        throttle -= dt * 0.5

    throttle = clamp(throttle, min_throttle, max_throttle)


    # ------------------------------
    # VERTICAL PHYSICS
    # ------------------------------

    lift = throttle * lift_strength

    vertical_acceleration = lift - gravity

    velocity.y += vertical_acceleration * dt

    drone.y += velocity.y * dt


    # ------------------------------
    # PITCH
    # ------------------------------

    if held_keys['w']:
        drone.rotation_x -= 50 * dt

    if held_keys['s']:
        drone.rotation_x += 50 * dt


    # ------------------------------
    # ROLL
    # ------------------------------

    if held_keys['a']:
        drone.rotation_z += 50 * dt

    if held_keys['d']:
        drone.rotation_z -= 50 * dt


    # ------------------------------
    # YAW
    # ------------------------------

    if held_keys['q']:
        drone.rotation_y -= 80 * dt

    if held_keys['e']:
        drone.rotation_y += 80 * dt


    # ------------------------------
    # GROUND COLLISION
    # ------------------------------

    if drone.y < 1:

        drone.y = 1
        velocity.y = 0


    # ------------------------------
    # HUD
    # ------------------------------

    altitude_text.text = f'Altitude: {drone.y:.1f} m'
    throttle_text.text = f'Throttle: {throttle * 100:.0f}%'


# --------------------------------------------------
# CAMERA
# --------------------------------------------------

camera.position = (0, 6, -12)
camera.look_at(drone)


app.run()