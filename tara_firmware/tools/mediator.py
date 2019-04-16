import rospy
from std_msgs.msg import Float32

class Mediator():
	def __init__(self):
		rospy.init_node('Mediator')
		rospy.Subscriber("tara_firmware/motor1_cmd", Float32, self.motor1_cmd)
		rospy.Subscriber("tara_firmware/motor2_cmd", Float32, self.motor2_cmd)
		self.motor1_signal_pub = rospy.Publisher("tara_firmware/motor1/signal", Float32, queue_size = 5)
		self.motor2_signal_pub = rospy.Publisher("tara_firmware/motor2/signal", Float32, queue_size = 5)

	def motor1_cmd(self, msg):
		divider = 1.0
		to_send = Float32()
		to_send.data = msg.data / divider
		self.motor1_signal_pub.publish(to_send)
	
	def motor2_cmd(self, msg):
		divider = 1.0
		to_send = Float32()
		to_send.data = msg.data / divider
		self.motor2_signal_pub.publish(to_send)

a = Mediator()
while not rospy.is_shutdown():
	continue
