from ursina import *
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

# At 50% throttle, lift approximately balances gravity
lift_strength = gravity

# Horizontal movement
horizontal_acceleration = 5
max_speed = 20

# Air resistance
drag = 1.5

# Rotation speed
pitch_speed = 30
roll_speed = 30
yaw_speed = 80


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

speed_text = Text(
    text='Speed: 0.0 m/s',
    position=(-0.85, 0.35),
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

    # --------------------------------------------------
    # THROTTLE
    # --------------------------------------------------

    if held_keys['space']:
        throttle += dt * 0.5

    if held_keys['shift']:
        throttle -= dt * 0.5

    throttle = clamp(
        throttle,
        min_throttle,
        max_throttle
    )


    # --------------------------------------------------
    # PITCH
    # --------------------------------------------------

    if held_keys['w']:
        drone.rotation_x -= pitch_speed * dt

    elif held_keys['s']:
        drone.rotation_x += pitch_speed * dt

    else:
        # Gradually return to level
        drone.rotation_x = lerp(
            drone.rotation_x,
            0,
            4 * dt
        )


    # --------------------------------------------------
    # ROLL
    # --------------------------------------------------

    if held_keys['a']:
        drone.rotation_z += roll_speed * dt

    elif held_keys['d']:
        drone.rotation_z -= roll_speed * dt

    else:
        # Gradually return to level
        drone.rotation_z = lerp(
            drone.rotation_z,
            0,
            4 * dt
        )


    # --------------------------------------------------
    # YAW
    # --------------------------------------------------

    if held_keys['q']:
        drone.rotation_y -= yaw_speed * dt

    if held_keys['e']:
        drone.rotation_y += yaw_speed * dt


    # --------------------------------------------------
    # LIFT + GRAVITY
    # --------------------------------------------------

    lift = throttle * lift_strength

    vertical_acceleration = lift - gravity

    velocity.y += vertical_acceleration * dt


    # --------------------------------------------------
    # HORIZONTAL THRUST
    # --------------------------------------------------

    forward = drone.forward
    right = drone.right

    # Amount of tilt
    pitch_amount = math.sin(
        math.radians(drone.rotation_x)
    )

    roll_amount = math.sin(
        math.radians(drone.rotation_z)
    )

    # Forward/backward acceleration
    velocity += (
        forward
        * pitch_amount
        * horizontal_acceleration
        * dt
    )

    # Left/right acceleration
    velocity += (
        right
        * roll_amount
        * horizontal_acceleration
        * dt
    )


    # --------------------------------------------------
    # AIR DRAG
    # --------------------------------------------------

    velocity.x *= max(
        0,
        1 - drag * dt
    )

    velocity.z *= max(
        0,
        1 - drag * dt
    )


    # --------------------------------------------------
    # MAXIMUM HORIZONTAL SPEED
    # --------------------------------------------------

    horizontal_velocity = Vec3(
        velocity.x,
        0,
        velocity.z
    )

    if horizontal_velocity.length() > max_speed:

        horizontal_velocity = (
            horizontal_velocity.normalized()
            * max_speed
        )

        velocity.x = horizontal_velocity.x
        velocity.z = horizontal_velocity.z


    # --------------------------------------------------
    # MOVE DRONE
    # --------------------------------------------------

    drone.position += velocity * dt


    # --------------------------------------------------
    # GROUND COLLISION
    # --------------------------------------------------

    if drone.y < 1:

        drone.y = 1

        if velocity.y < 0:
            velocity.y = 0


    # --------------------------------------------------
    # HUD
    # --------------------------------------------------

    altitude_text.text = (
        f'Altitude: {drone.y:.1f} m'
    )

    throttle_text.text = (
        f'Throttle: {throttle * 100:.0f}%'
    )

    speed = velocity.length()

    speed_text.text = (
        f'Speed: {speed:.1f} m/s'
    )


# --------------------------------------------------
# CAMERA
# --------------------------------------------------

camera.position = (0, 6, -12)
camera.look_at(drone)


# --------------------------------------------------
# START
# --------------------------------------------------

app.run()