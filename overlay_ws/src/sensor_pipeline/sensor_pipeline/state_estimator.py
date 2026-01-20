#!/usr/bin/env python3
import rclpy, time
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

HAPPY = 1
SCARED = 2
BORED = 3

class StateEstimator(Node):
    def __init__(self):
        super().__init__('state_estimator')

        self.create_subscription(
            Float32MultiArray,
            '/imu_filtered',
            self.cb,
            10
        )

        self.pub = self.create_publisher(
            Float32MultiArray,
            '/imu_control',
            10
        )

        self.state = BORED
        self.state_until = 0.0
        self.happy_gain = 1.0

    def cb(self, msg):
        now = time.time()

        ir = int(msg.data[3])
        jolt = int(msg.data[4])
        ticks = msg.data[5]

        # ---- Gain from encoder ----
        if ticks > 2:
            self.happy_gain = 2.0
            self.state_until = now + 10
        elif ticks < -2:
            self.happy_gain = 0.5
            self.state_until = now + 10

        # ---- State priority logic ----
        if ir:
            self.state = HAPPY
            self.state_until = now + 10

        elif jolt:
            self.state = SCARED
            self.state_until = now + 10

        elif now > self.state_until:
            self.state = BORED

        out = Float32MultiArray()
        out.data = [
            0.0, 0.0, 0.0,
            float(self.state),
            float(self.happy_gain)
        ]
        self.pub.publish(out)


def main():
    rclpy.init()
    rclpy.spin(StateEstimator())
    rclpy.shutdown()
