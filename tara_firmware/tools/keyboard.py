import pygame
import rospy
from std_msgs.msg import Int16

class KeyboardController():
	def __init__(self):
		pygame.init()
		rospy.init_node("KeyboardController")
		self.motor1_pub = rospy.Publisher('deep_tara/motor1', Int16, queue_size=10)
		self.motor2_pub = rospy.Publisher('deep_tara/motor2', Int16, queue_size=10)
		#self.backward_l = rospy.Publisher('hardware/lmotor/backward', Int16, queue_size=10)
		#self.backward_r = rospy.Publisher('hardware/rmotor/backward', Int16, queue_size=10)
		screen = pygame.display.set_mode((400, 300))

	def main_loop(self):
		done = False
		while not done:
			try:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						done = True
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_UP:
							self.forward()
						elif event.key == pygame.K_DOWN:
							self.backward()
						elif event.key == pygame.K_SPACE:
							self.stop()					
				pygame.display.flip()
			except KeyboardInterrupt:
				exit()

	def stop(self):
		msg = Int16()
		msg.data = 0
		print "Stop"
		self.motor1_pub.publish(msg)
		self.motor2_pub.publish(msg)
		#self.backward_r.publish(msg)
		#self.backward_l.publish(msg)
		#self.forward_r.publish(msg)
		#self.forward_l.publish(msg)

	def backward(self):
		msg = Int16()
		msg.data = -5
		print "Backward"
		#self.backward_r.publish(msg)
		#self.backward_l.publish(msg)
		self.motor1_pub.publish(msg)
		self.motor2_pub.publish(msg)

	def forward(self):
		msg = Int16()
		msg.data = 5
		print "Forward"
		self.motor2_pub.publish(msg)
		self.motor1_pub.publish(msg)

k = KeyboardController()
k.main_loop()
