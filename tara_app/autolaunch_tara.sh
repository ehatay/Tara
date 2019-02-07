#!/usr/bin/env bash
echo "STARTING"
export THEIP=$(ifconfig | grep 'inet addr:'| grep -v '127.0.0.1' | tail -1 | cut -d: -f2 | awk '{ print $1 }')
source /opt/ros/kinetic/setup.bash
source ~/ros_catkin_ws/devel/setup.bash
if [ "$THEIP" = "" ]; then 
	echo "Not connected to network" 
else 
	echo "Connected to network. Assigning ROS_MASTER_URI and ROS_IP automatically..."
	export ROS_MASTER_URI=http://$THEIP:11311
	export ROS_IP=$THEIP
fi;
bash -c "source /home/pi/ros_catkin_ws/devel/setup.bash && 
roslaunch tara_controller run.launch"
