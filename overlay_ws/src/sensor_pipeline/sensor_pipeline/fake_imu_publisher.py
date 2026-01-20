#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import math
import time


class FakeIMUPublisher(Node):
    def __init__(self):
        super().__init__('fake_imu_publisher')
        
        # Publisher for IMU control data
        self.pub = self.create_publisher(
            Float32MultiArray,
            '/imu_control',
            10
        )
        
        # Timer to publish at regular intervals (similar to real IMU rate)
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz
        
        # Time tracking for patterns
        self.start_time = time.time()
        
        # Configuration
        self.amplitude_roll = 0.5   # radians (about 28 degrees)
        self.amplitude_pitch = 0.4  # radians (about 23 degrees)
        self.amplitude_yaw = 0.3    # radians (about 17 degrees)
        
        self.get_logger().info('Fake IMU publisher started')
        self.get_logger().info('Publishing to /imu_control topic')
        
    def timer_callback(self):
        t = time.time() - self.start_time
        
        # Generate sinusoidal patterns for smooth motion
        # Using different frequencies for each axis to create interesting motion
        roll = self.amplitude_roll * math.sin(t * 0.3)      # Slow roll oscillation
        pitch = self.amplitude_pitch * math.cos(t * 0.4)    # Medium pitch oscillation
        yaw = self.amplitude_yaw * math.sin(t * 0.5)        # Faster yaw oscillation
        
        # Create and publish message
        msg = Float32MultiArray()
        msg.data = [roll, pitch, yaw]
        
        self.pub.publish(msg)
        
        # Log periodically (every 2 seconds)
        if int(t * 10) % 20 == 0:  # Every 2 seconds at 10 Hz
            self.get_logger().info(
                f'Publishing: roll={roll:.3f}, pitch={pitch:.3f}, yaw={yaw:.3f}'
            )


def main():
    rclpy.init()
    node = FakeIMUPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
