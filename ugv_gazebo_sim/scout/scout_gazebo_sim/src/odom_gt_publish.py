#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
import tf
from geometry_msgs.msg import TransformStamped

def odom_callback(msg):
    # 从 Odometry 消息中提取位置和方向
    position = msg.pose.pose.position
    orientation = msg.pose.pose.orientation

    # 发布 TF
    broadcaster = tf.TransformBroadcaster()
    broadcaster.sendTransform(
        (position.x, position.y, position.z),  # 平移
        (orientation.x, orientation.y, orientation.z, orientation.w),  # 旋转 (四元数)
        rospy.Time.now(),  # 时间戳
        "base_link",       # 子坐标系
        "odom"             # 父坐标系
    )

    # 创建并发布新的 Odometry 消息
    new_odom = Odometry()
    new_odom.header.stamp = msg.header.stamp
    new_odom.header.frame_id = "odom"
    new_odom.child_frame_id = "base_link"
    
    # 复制位姿和速度信息
    new_odom.pose = msg.pose
    new_odom.twist = msg.twist
    
    # 发布消息
    odom_publisher.publish(new_odom)

def main():
    rospy.init_node('odom_to_tf_publisher')

    global odom_publisher
    odom_publisher = rospy.Publisher('/odom', Odometry, queue_size=10)

    # 订阅 /odom 话题
    rospy.Subscriber('/trueodom', Odometry, odom_callback)

    # rospy.loginfo("TF publisher from /odom is running...")
    rospy.spin()

if __name__ == '__main__':
    main()