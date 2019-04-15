#!/usr/bin/python
import serial
from time import sleep
import commands
import math
import subprocess

# Bluetooth-Serial

def valmap(value, istart, istop, ostart, ostop):
  return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

bluetoothSerial = serial.Serial("/dev/ttyAMA0", baudrate=9600)
bluetoothSerial.flushInput()
bluetoothSerial.flushOutput()
bluetoothSerial.write("Ready...\r\n");

def get_ip():
	return commands.getoutput('hostname -I').split(' ')[0]

def send(msg):
	bluetoothSerial.write(str(msg) + "\r\n");

def check_cmd(cmd):
	if(cmd == "" or cmd == " " or cmd == "\r\n"): 
		return;
	splitted = cmd.split('~')
	if(cmd == "restart\r\n"):
		send("Rebooting...")
	elif(cmd == "ack\r\n"):
		send("Connection established...")
	elif(cmd == "request_ip\r\n"):
		send(get_ip())
	elif(len(splitted) == 2):
		vel = Twist()
		try:
			vel.angular.z = float(splitted[0]) - 50
			vel.linear.x = (float(splitted[1].split('\r')[0]) - 50) / (-100)
			vel.linear.x /= 4
		except(Exception):
			pass
		return vel
	else:
		#print cmd.split(' ')
		try:
			p = subprocess.Popen(cmd.split('\r\n')[0].split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = p.communicate()
			send(out)
		except(Exception):
			bluetoothSerial.write("Error: " + cmd);

### ROS
import rospy
from geometry_msgs.msg import Twist

rospy.init_node('tara_controller')
pub = rospy.Publisher('/twist', Twist, queue_size=10)
rate = rospy.Rate(10)
get_ip()

while not rospy.is_shutdown():
	incoming = str(bluetoothSerial.readline())
	bluetoothSerial.flushInput()
	bluetoothSerial.flushOutput()
	if(len(incoming) > 0):
		vel = check_cmd(incoming)
		if(vel is None):
			continue
		pub.publish(vel)
