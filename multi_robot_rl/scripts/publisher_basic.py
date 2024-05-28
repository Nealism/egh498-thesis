#!/usr/bin/env python3

import rospy 
from std_msgs.msg import String 

if __name__ == '__main__':
	rospy.init_node('node_name')
	pub=rospy.Publisher("/topic_name",String, queue_size=10)
	rate=rospy.Rate(2)


	while not rospy.is_shutdown():
		msg=String()
		msg_data="Hi,Noob!"
		pub.publish(msg_data)
		rate.sleep()
	rospy.loginfo("Node was Stopped")
