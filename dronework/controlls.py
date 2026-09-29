from ursina import *


class DroneControls:

    def __init__(self, physics):
        self.physics = physics

    def update(self, drone, dt):

        # THROTTLE
        if held_keys['space']:
            self.physics.throttle += dt * 0.5

        if held_keys['shift']:
            self.physics.throttle -= dt * 0.5

        self.physics.throttle = clamp(
            self.physics.throttle,
            self.physics.min_throttle,
            self.physics.max_throttle
        )

        # PITCH
        if held_keys['w']:
            drone.rotation_x -= (
                self.physics.pitch_speed * dt
            )

        elif held_keys['s']:
            drone.rotation_x += (
                self.physics.pitch_speed * dt
            )

        else:
            drone.rotation_x = lerp(
                drone.rotation_x,
                0,
                4 * dt
            )

        # ROLL
        if held_keys['a']:
            drone.rotation_z += (
                self.physics.roll_speed * dt
            )

        elif held_keys['d']:
            drone.rotation_z -= (
                self.physics.roll_speed * dt
            )

        else:
            drone.rotation_z = lerp(
                drone.rotation_z,
                0,
                4 * dt
            )

        # YAW
        if held_keys['q']:
            drone.rotation_y -= (
                self.physics.yaw_speed * dt
            )

        if held_keys['e']:
            drone.rotation_y += (
                self.physics.yaw_speed * dt
            )