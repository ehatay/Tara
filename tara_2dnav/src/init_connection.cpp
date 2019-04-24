#include <ros/ros.h>
#include <iostream>

using namespace std;

int main(int argc, char** argv)
{
  ros::init(argc, argv, "init_connection");
  ros::NodeHandle n;
 
  string ip, user, pass, cmd;

  n.getParam("/ip", ip);
  n.getParam("/user", user);

 //restart rosbeam-bridge
  cmd = "ssh " + user + "@" + ip + " \"init_firmware.sh\"";
  system(cmd.c_str());    

}



