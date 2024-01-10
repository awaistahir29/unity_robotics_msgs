#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import TransformStamped

def drone_transform_callback(msg):
    # Assuming receiving the transformation of the drone with respect to the Hololens frame
    drone_transform = msg

    # Compute the inverse transformation to get Hololens with respect to the drone frame
    hololens_to_drone_transform = TransformStamped()
    hololens_to_drone_transform.header.stamp = rospy.Time.now()
    hololens_to_drone_transform.header.frame_id = drone_transform.child_frame_id  # Hololens frame
    hololens_to_drone_transform.child_frame_id = drone_transform.header.frame_id  # Drone frame

    # Invert translation
    hololens_to_drone_transform.transform.translation.x = -drone_transform.transform.translation.x
    hololens_to_drone_transform.transform.translation.y = -drone_transform.transform.translation.y
    hololens_to_drone_transform.transform.translation.z = -drone_transform.transform.translation.z

    # Invert rotation (quaternion inverse)
    hololens_to_drone_transform.transform.rotation.x = -drone_transform.transform.rotation.x
    hololens_to_drone_transform.transform.rotation.y = -drone_transform.transform.rotation.y
    hololens_to_drone_transform.transform.rotation.z = -drone_transform.transform.rotation.z
    hololens_to_drone_transform.transform.rotation.w = drone_transform.transform.rotation.w

    # Publish the transformation of the Hololens with respect to the drone frame
    # You need to define a publisher for the inverted transformation
    # pub.publish(hololens_to_drone_transform)

    rospy.loginfo("Transformation of Hololens with respect to drone frame:\n%s", hololens_to_drone_transform)

if __name__ == '__main__':
    rospy.init_node('inverse_transform_node')

    # Subscriber to the topic where you receive the transformation of the drone with respect to the Hololens frame
    rospy.Subscriber('drone_transform_in_hololens_frame', TransformStamped, drone_transform_callback)

    # Publisher to publish the inverted transformation of the Hololens with respect to the drone frame
    # Define your publisher here
    # pub = rospy.Publisher('inverted_hololens_transform', TransformStamped, queue_size=10)

    rospy.spin()
