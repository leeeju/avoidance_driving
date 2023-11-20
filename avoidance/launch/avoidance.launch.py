#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
        return LaunchDescription([
            Node(
                package='avoidance',
                executable='avoidance',
                name='avoidance',
                output='screen',
                emulate_tty=True,
            ),
        ])