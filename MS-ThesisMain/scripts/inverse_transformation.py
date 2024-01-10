#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import TransformStamped
from unity_robotics_demo_msgs.msg import CurrentDronePose

def drone_transform_callback(msg):
    # Assuming receiving the transformation of the drone with respect to the Hololens frame
    drone_transform = msg

    # Compute the inverse transformation to get Hololens with respect to the drone frame
    hololens_to_drone_transform = TransformStamped()
    hololens_to_drone_transform.header.stamp = rospy.Time.now()
    hololens_to_drone_transform.header.frame_id = "Hololens"  # Hololens frame
    hololens_to_drone_transform.child_frame_id = "Drone"  # Drone frame

    # Invert translation
    hololens_to_drone_transform.transform.translation.x = -drone_transform.pos_x
    hololens_to_drone_transform.transform.translation.y = -drone_transform.pos_y
    hololens_to_drone_transform.transform.translation.z = -drone_transform.pos_z

    # Invert rotation (set the identity as there's no provided orientation)
    hololens_to_drone_transform.transform.rotation.x = 0.0
    hololens_to_drone_transform.transform.rotation.y = 0.0
    hololens_to_drone_transform.transform.rotation.z = 0.0
    hololens_to_drone_transform.transform.rotation.w = 0.0
    
    # Publish the inverse transformation of the Hololens with respect to the drone frame
    pub.publish(hololens_to_drone_transform)

    # Publish the transformation of the Hololens with respect to the drone frame
    # You need to define a publisher for the inverted transformation
    # pub.publish(hololens_to_drone_transform)

    rospy.loginfo("Transformation of Hololens with respect to drone frame:\n%s", hololens_to_drone_transform)

if __name__ == '__main__':
    rospy.init_node('inverse_transform_node')
    
    # Publisher to publish the inverse transformation of the Hololens with respect to the drone frame
    pub = rospy.Publisher('/hololens_pose', TransformStamped, queue_size=10)

    # Subscriber to the topic where you receive the transformation of the drone with respect to the Hololens frame
    rospy.Subscriber('drone_pose', CurrentDronePose, drone_transform_callback)

    # Publisher to publish the inverted transformation of the Hololens with respect to the drone frame
    # Define your publisher here
    # pub = rospy.Publisher('inverted_hololens_transform', TransformStamped, queue_size=10)

    rospy.spin()
