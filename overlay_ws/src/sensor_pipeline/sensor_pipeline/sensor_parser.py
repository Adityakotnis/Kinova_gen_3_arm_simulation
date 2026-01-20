#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from collections import deque

class SensorParser(Node):
    def __init__(self):
        super().__init__('sensor_parser')
        self.create_subscription(Float32MultiArray,'/imu_raw',self.cb,10)
        self.pub=self.create_publisher(Float32MultiArray,'/imu_filtered',10)

        self.buf=[deque(maxlen=5) for _ in range(6)]

    def cb(self,msg):
        for i in range(6):
            self.buf[i].append(msg.data[i])

        o=Float32MultiArray()
        o.data=[sum(b)/len(b) if len(b)>0 else 0.0 for b in self.buf]
        self.pub.publish(o)

def main():
    rclpy.init()
    rclpy.spin(SensorParser())
    rclpy.shutdown()
