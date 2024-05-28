#!/usr/bin/env python3

import rospy
from std_msgs.msg import String



def callback_complement(msg):
	rospy.loginfo("Got_my_Complement_Received")
	rospy.loginfo(msg)




if __name__=="__main__":
	rospy.init_node('Subsciber_node_name')
	sub=rospy.Subscriber("/topic_name",String,callback_complement)
	rospy.spin()
