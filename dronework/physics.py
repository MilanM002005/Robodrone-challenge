from ursina import *
import math


class DronePhysics:
    def __init__(self):
        self.velocity = Vec3(0, 0, 0)

        self.gravity = 9.81

        self.throttle = 0.5
        self.max_throttle = 1.0
        self.min_throttle = 0.0

        # 50% throttle should approximately hover
        self.lift_strength = self.gravity

        self.horizontal_acceleration = 5
        self.max_speed = 20
        self.drag = 1.5

        self.pitch_speed = 30
        self.roll_speed = 30
        self.yaw_speed = 80

    def update_physics(self, drone, dt):

        # Lift + gravity
        lift = self.throttle * self.lift_strength
        vertical_acceleration = lift - self.gravity

        self.velocity.y += vertical_acceleration * dt

        # Drone orientation
        forward = drone.forward
        right = drone.right

        pitch_amount = math.sin(
            math.radians(drone.rotation_x)
        )

        roll_amount = math.sin(
            math.radians(drone.rotation_z)
        )

        # Horizontal thrust
        self.velocity += (
            forward
            * pitch_amount
            * self.horizontal_acceleration
            * dt
        )

        self.velocity += (
            right
            * roll_amount
            * self.horizontal_acceleration
            * dt
        )

        # Air drag
        self.velocity.x *= max(0, 1 - self.drag * dt)
        self.velocity.z *= max(0, 1 - self.drag * dt)

        # Maximum horizontal speed
        horizontal_velocity = Vec3(
            self.velocity.x,
            0,
            self.velocity.z
        )

        if horizontal_velocity.length() > self.max_speed:
            horizontal_velocity = (
                horizontal_velocity.normalized()
                * self.max_speed
            )

            self.velocity.x = horizontal_velocity.x
            self.velocity.z = horizontal_velocity.z

        # Move drone
        drone.position += self.velocity * dt

        # Ground
        if drone.y < 1:
            drone.y = 1

            if self.velocity.y < 0:
                self.velocity.y = 0

    def reset(self):
        self.velocity = Vec3(0, 0, 0)
        self.throttle = 0.5