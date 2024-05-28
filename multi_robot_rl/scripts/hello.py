
#!/usr/bin/env python3

import rospy

if __name__ == '__main__':
	rospy.init_node('Hello_node')
	rospy.loginfo('This node has been started')
	rate=rospy.Rate(10)

	while not rospy.is_shutdown():
		rospy.loginfo('Hello')
		rate.sleep()
