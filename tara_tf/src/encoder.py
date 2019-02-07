import rospy, roslib
from std_msgs.msg import *

class PseudoEncoder():
	name = None
	current = 0;
	pub = None;
	def __init__(self, name):
		print("Pseudo encoder '" + name + "' initialized")
		self.name = name
		self.pub = rospy.Publisher('/' + name + "/current", Float64, queue_size=10)


	def main(self):
		self.current += 1;
		self.pub.publish(self.current)

rospy.init_node('pseudo_encoders')

left = PseudoEncoder("Left")
right = PseudoEncoder("Right")
rate = rospy.Rate(10)

while not rospy.is_shutdown():
	left.main()
	right.main()
