#!/usr/bin/env python3
import rclpy, time, math
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

HAPPY = 1
SCARED = 2
BORED = 3

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        self.swing_phase_start = 0.0

        self.pub = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )

        self.create_subscription(
            Float32MultiArray,
            '/imu_control',
            self.cb,
            10
        )

        self.joints = [f'joint_{i}' for i in range(1, 8)]

        self.bored_pose = [
            0.0,
            math.radians(90),
            0.0,
            math.radians(15),
            0.0,
            0.0,
            0.0
        ]

        self.prev_state = BORED
        self.happy_start_time = 0.0

    def send(self, pos, d=1.5):
        t = JointTrajectory()
        t.joint_names = self.joints
        p = JointTrajectoryPoint()
        p.positions = pos
        p.time_from_start = Duration(sec=int(d))
        t.points.append(p)
        self.pub.publish(t)

    def cb(self, msg):
        state = int(msg.data[3])
        gain = msg.data[4]
        now = time.time()

        # ---------- STATE TRANSITIONS ----------
        if state != self.prev_state:

            # BORED → SCARED
            if self.prev_state == BORED and state == SCARED:
                self.send([
                    0.0, math.radians(10), 0.0,
                    math.radians(105), 0.0,
                    math.radians(105), 0.0
                ], 2.0)

                time.sleep(2.0)
                self.send([
                    0.0, math.radians(50), 0.0,
                    math.radians(105), 0.0,
                    math.radians(105), 0.0
                ])

            # HAPPY → SCARED
            elif self.prev_state == HAPPY and state == SCARED:
                self.send([
                    0.0, math.radians(0), 0.0,
                    math.radians(105), 0.0,
                    math.radians(105), 0.0
                ], 2.0)

                time.sleep(1.5)
                self.send([
                    0.0, math.radians(50), 0.0,
                    math.radians(105), 0.0,
                    math.radians(105), 0.0
                ])

            # SCARED → BORED
            elif self.prev_state == SCARED and state == BORED:
                self.send([
                        0.0,
                        math.radians(10),
                        0.0,
                        math.radians(105),
                        0.0,
                        math.radians(105),
                        0.0
                    ],1.0)

                time.sleep(1.0)
                self.send(self.bored_pose, 2.0)

            # ANY → HAPPY
            elif state == HAPPY:
                self.send([
                    0.0,
                    math.radians(60),
                    0.0,
                    math.radians(-20),
                    0.0,
                    math.radians(-40),
                    0.0
                ], 1.5)

                self.happy_start_time = now + 1.5
                self.swing_phase_start = now + 1.5

        # ---------- CONTINUOUS BEHAVIOR ----------
        if state == HAPPY and now >= self.happy_start_time:
            swing = math.sin((now - self.swing_phase_start) * 3.0) * math.radians(90) * gain
            self.send([
                swing,
                math.radians(60),
                0.0,
                math.radians(-20),
                0.0,
                math.radians(-40),
                0.0
            ], 1.0)

        elif state == BORED:
            self.send(self.bored_pose, 2.0)

        elif state == SCARED:
            self.send([
                0.0,
                math.radians(50),
                0.0,
                math.radians(105),
                0.0,
                math.radians(105),
                0.0
            ], 1.5)

        self.prev_state = state


def main():
    rclpy.init()
    rclpy.spin(RobotController())
    rclpy.shutdown()
