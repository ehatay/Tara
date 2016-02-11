#!/usr/bin/env python
import rospy
from std_msgs.msg import Bool
import sys

class SecureMotorControl:
	def __init__(self):
		rospy.init_node('motor_shutdown')
		self.motor1_state_pub = rospy.Publisher('tara_firmware/motor1/change_state', Bool, queue_size = 10)
		self.motor2_state_pub = rospy.Publisher('tara_firmware/motor2/change_state', Bool, queue_size = 10)
#		signal = None
		#if(arg == "-e"):
		#	signal = True
		#elif(arg == "-d"):
	#		signal = False
	#	else:
	#		return;
	#	self.change_state(signal)
		#print (arg)
		rospy.on_shutdown(lambda: self.change_state(False))

	def change_state(self,data):
		if (data):
			rospy.loginfo("Enabling motors")
		else:
			rospy.loginfo("Disabling motors")
		self.motor1_state_pub.publish(Bool(data))
		self.motor2_state_pub.publish(Bool(data))

#rospy.init_node('disabler')
c = SecureMotorControl()

#rospy.spin()
#c.change_state(True)
while not rospy.is_shutdown():
	c.change_state(True)#continue
#rospy.spin()