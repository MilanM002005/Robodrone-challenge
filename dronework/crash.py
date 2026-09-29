from ursina import *


class CrashSystem:

    def __init__(self, drone, physics):

        self.drone = drone
        self.physics = physics

        self.crashed = False
        self.crash_reason = ""

        self.start_position = Vec3(0, 2, 0)

        self.crash_text = Text(
            text="",
            origin=(0, 0),
            scale=2,
            y=0.1,
            color=color.red
        )

    def check_ground_collision(self):

        if self.crashed:
            return

        # Hard landing
        if (
            self.drone.y <= 1.05
            and self.physics.velocity.y < -4.5
        ):
            self.trigger_crash("HARD LANDING")
            return

        # Tilted landing
        if self.drone.y <= 1.05:

            pitch = abs(self.drone.rotation_x)
            roll = abs(self.drone.rotation_z)

            if pitch > 15 or roll > 15:
                self.trigger_crash("TILTED LANDING")

    def trigger_crash(self, reason):

        self.crashed = True
        self.crash_reason = reason

        self.physics.velocity = Vec3(0, 0, 0)

        self.crash_text.text = (
            f"CRASH!\n"
            f"{reason}\n\n"
            f"Press R to reset"
        )

    def reset(self):

        self.drone.position = self.start_position
        self.drone.rotation = (0, 0, 0)

        self.physics.reset()

        self.crashed = False
        self.crash_reason = ""

        self.crash_text.text = ""

    def update(self):

        if not self.crashed:
            self.check_ground_collision()