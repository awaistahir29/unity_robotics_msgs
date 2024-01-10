#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PointStamped, TransformStamped
import tf2_ros
import tf2_geometry_msgs

current_transform = None

def transform_callback(msg):
    global current_transform
    current_transform = msg

def trajectory_points_callback(msg):
    global current_transform

    if current_transform is None:
        rospy.logwarn("No transformation information received yet. Skipping transformation.")
        return

    # Process each received trajectory point
    for point in msg.points:
        transformed_point = transform_point(point, current_transform)
        #if transformed_point:
            # Publish each transformed point
            #pub.publish(transformed_point)

def transform_point(point, transform):
    try:
        # Transform the point from Hololens to drone frames
        transformed_point = tf2_geometry_msgs.do_transform_point(point, transform)
        return transformed_point

    except Exception as e:
        rospy.logerr("Transformation Exception: %s", str(e))
        return None

if __name__ == '__main__':
    rospy.init_node('hololens_to_drone_transformer')

    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(tf_buffer)

    # Subscriber for the transformation between Hololens and drone frames
    rospy.Subscriber('/hololens_pose', TransformStamped, transform_callback)

    # Subscriber for the trajectory points in the Hololens frame
    #rospy.Subscriber('/hololens_trajectory', YourTrajectoryMessageType, trajectory_points_callback)

    # Publisher for the transformed trajectory points in the drone frame
    #pub = rospy.Publisher('/drone_trajectory', YourTrajectoryMessageType, queue_size=10)

    rospy.spin()
