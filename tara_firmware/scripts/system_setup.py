#!/usr/bin/env python
from firmware import Encoder
import rospy, sys

name = sys.argv[1]
enc1_pins = rospy.get_param("/"+name+"/pins")
enc1_device_name = rospy.get_param("/"+name+"/device_name")
enc1_printToScreen = rospy.get_param("/"+name+'/print_to_screen', False)
enc1_topic = rospy.get_param("/"+name+"/topic")

e1 = Encoder(enc1_pins['A'], enc1_pins['B'], enc1_pins['S'], enc1_device_name, enc1_printToScreen, enc1_topic)
e1.RosLoop()
