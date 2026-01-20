#!/usr/bin/env python3
import rclpy,socket
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

class UDPBridge(Node):
    def __init__(self):
        super().__init__('udp_bridge')
        self.pub=self.create_publisher(Float32MultiArray,'/imu_raw',10)
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0",4242))
        self.sock.setblocking(False)
        self.create_timer(0.01,self.recv)

    def recv(self):
        try:
            data,_ = self.sock.recvfrom(256)
            for line in data.decode().splitlines():
                v=list(map(float,line.split(',')))
                msg=Float32MultiArray()
                msg.data=v
                self.pub.publish(msg)
        except:
            pass

def main():
    rclpy.init()
    rclpy.spin(UDPBridge())
    rclpy.shutdown()
