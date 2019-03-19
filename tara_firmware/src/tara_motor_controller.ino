#include <ros.h>
#include <std_msgs/Int16.h>

ros::NodeHandle nh;
const int r_motor_pin_f = 5;
const int l_motor_pin_f = 10;
const int r_motor_pin_b = 6;
const int l_motor_pin_b = 11;

void messageCbLb( const std_msgs::Int16& msg)
{
  if(msg.data <= 255 || msg.data >= 0)
    analogWrite(l_motor_pin_b, msg.data); 
}

void messageCbLf( const std_msgs::Int16& msg)
{
  if(msg.data <= 255 || msg.data >= 0)
    analogWrite(l_motor_pin_f, msg.data); 
}

void messageCbRf( const std_msgs::Int16& msg)
{
  if(msg.data <= 255 || msg.data >= 0)
    analogWrite(l_motor_pin_f, msg.data); 
}


void messageCbRb( const std_msgs::Int16& msg)
{
  if(msg.data <= 255 || msg.data >= 0)
    analogWrite(r_motor_pin_b, msg.data); 
}

ros::Subscriber<std_msgs::Int16> sublf("hardware/lmotor/forward", &messageCbLf );
ros::Subscriber<std_msgs::Int16> sublb("hardware/lmotor/backward", &messageCbLb );
ros::Subscriber<std_msgs::Int16> subrf("hardware/rmotor/forward", &messageCbRf );
ros::Subscriber<std_msgs::Int16> subrb("hardware/rmotor/backward", &messageCbRb );

void setup()
{
  nh.initNode();
  nh.subscribe(sublf);
  nh.subscribe(sublb);
  nh.subscribe(subrb);
  nh.subscribe(subrf);
}

void loop()
{
  pinMode(r_motor_pin_b,OUTPUT);
  pinMode(l_motor_pin_b,OUTPUT);
  pinMode(r_motor_pin_f,OUTPUT);
  pinMode(l_motor_pin_f,OUTPUT);
  nh.spinOnce();
  delay(1);
}
