import RPi.GPIO as GPIO
import time
import sys,tty,termios,os
import rospy
from std_msgs.msg import Int64

class Encoder():
	def __init__(self, a, b, device_name = "encoder", printToScreen = False, rostopic = ""):
		self.counter = 0
		self.ros = rostopic
		print device_name + " initiated with topic: " + rostopic
		if(self.ros):
			rospy.init_node(device_name + "_processor", anonymous=True)
			self.publisher = rospy.Publisher(rostopic, Int64, queue_size=10)	
		self.printToScreen = printToScreen
		self.flag = 0
		self.name = device_name
		self.LastEncBStatus = 0
		self.Current_EncB_Status = 0
		self.EncAPin = a
		self.EncBPin = b
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.EncAPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.EncBPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	def testLoop(self):
		while True:
			self.CheckEncoderState()

	def RosLoop(self):
		if not self.ros:
			print "Please enable ros instantiation by setting Encoder class parameter 'rostopic'"
			exit(0)
		while not rospy.is_shutdown():
			self.CheckEncoderState()

	def CheckEncoderState(self):
		self.LastEncBStatus = GPIO.input(self.EncBPin)
		while(not GPIO.input(self.EncAPin) and not rospy.is_shutdown()):
			self.Current_EncB_Status = GPIO.input(self.EncBPin)
			self.flag = 1
		if(self.flag == 1):
			self.flag = 0
			if(self.LastEncBStatus == 0) and (self.Current_EncB_Status == 1):
				self.counter += 1
				self.PublishCounter()
			if(self.LastEncBStatus == 1) and (self.Current_EncB_Status == 0):
				self.counter -= 1
				self.PublishCounter()

	def PublishCounter(self):
		if(self.printToScreen):
			print (self.name + ' Counter = %d' % self.counter)
		if(self.ros):
			self.publisher.publish(self.counter)
