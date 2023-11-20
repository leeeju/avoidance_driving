#!/usr/bin/env python3
# -*- coding: utf-8 -*- #
import rclpy
import threading
import numpy as np
import math
import time

from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from sensor_msgs.msg import LaserScan as LiDAR
from std_msgs.msg import Float32
from rclpy.qos import QoSProfile
from geometry_msgs.msg import PoseStamped, Twist


class detection(Node):
    def __init__(self):
        super().__init__('detection_node')
        qos_profile = (QoSProfile(depth=10))
        self.cb_group = ReentrantCallbackGroup()

        self.lidar_data            = []
        self.partition_cnt         = 8
        self.min_global_y_LiDAR    = 150
        self.global_x_LiDAR        = 200 #mm
        self.global_y_LiDAR        = 400
        self.distance              = 0   #mm
        self.added_range           = int(2*((self.global_x_LiDAR)/(self.partition_cnt)))

        #subscriber
        self.create_subscription(LiDAR, '/scan', self.LiDAR_callback, qos_profile, callback_group=self.cb_group)

        #publisher
        self.target_num_pub = self.create_publisher(Float32, '/LiDAR_target_num', qos_profile, callback_group=self.cb_group)
        self.goal_pub = self.create_publisher(PoseStamped, '/move_base_simple/goal', qos_profile, callback_group=self.cb_group)
        self.avoidance_pub = self.create_publisher(Twist, '/cmd_vel', qos_profile, callback_group=self.cb_group)

        self.rate = self.create_rate(15)
        self.is_ready = False

        self.executor_ = MultiThreadedExecutor(num_threads=4)
        self.executor_.add_node(self)
        self.spin_thread = threading.Thread(target=self.spin)
        self.spin_thread.start()

        self.get_logger().info('detection_node has been started')

    def LiDAR_callback(self,msg):
        self.lidar_data = msg.ranges
        self.lidar_angle_increment = msg.angle_increment
        self.partition_list        = [0,0,0,0,0,0,0,0]
        self.distance_data         = []
        self.target_num            = 0
        self.max_value             = 0
        float_msg                  = Float32()

        for i in range(len(self.lidar_data)):

            angle = (self.lidar_angle_increment * i)
            x = -np.sin(angle) * self.lidar_data[i] * 1000
            y = np.cos(angle) * self.lidar_data[i] * 1000

            if (abs(x) < self.global_x_LiDAR) and (y > self.min_global_y_LiDAR) and (y < self.global_y_LiDAR): #mm
                for i in range(self.partition_cnt):
                    if ((-self.global_x_LiDAR)+ i*(self.added_range)) < (x) and \
                        (x) < ((-self.global_x_LiDAR)+ ((i+1)*(self.added_range))):
                        self.distance = (math.sqrt(x*x + y*y))
                        self.distance_data.append(self.distance)
                        self.partition_list[i] = len(self.distance_data)
                self.target_num, self.max_value = max(enumerate(self.partition_list),key=lambda x: x[1])
                self.target_num +=1

                # print(f'target_num: {self.target_num}')

        float_msg.data= float(self.target_num)
        print(f'num: {self.target_num}')
        print(self.partition_list)
        self.target_num_pub.publish(float_msg)

        if self.target_num >= 15:
            self.run_avoidance()

    def run_avoidance(self):
        tw = Twist()
        tw.angular.x = 0.0
        tw.angular.y = 0.0
        tw.angular.z = 1.5708  # 90 degrees in radians
        self.avoidance_pub.publish(tw)

    def spin(self):
        try:
            if not self.is_ready:
                self.executor_.spin()
                self.rate.sleep()
                self.spin_thread.start()
        except KeyboardInterrupt:
            self.destroy_node()
            rclpy.shutdown()

def main():
        rclpy.init()
        lidar = detection()
        try:
            rclpy.spin(lidar)
        finally:
            lidar.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()
