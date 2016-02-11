#include <ros.h>
#include <std_msgs/Int16.h>
#include <std_msgs/Bool.h>

ros::NodeHandle nh;

/* Right motor */
const int motor1_pwm = 11;
const int motor1_en = 12;
const int motor1_dir = 13;
boolean motor1_stopped = true;
boolean motor1_enabled = false;
boolean motor1_forward = true;

/* Left motor */
const int motor2_pwm = 10;
const int motor2_en = 8;
const int motor2_dir = 9;
boolean motor2_stopped = true;
boolean motor2_enabled = false;
boolean motor2_forward = true;

const int EMF_wait_buffer_msecs = 50;

void change_motor_direction (int motor, boolean forward)
{
  if(motor == 1)
  {
    motor1_forward = forward;
    if(forward)
    {
      digitalWrite(motor1_dir, HIGH);
      delay(EMF_wait_buffer_msecs);
    }
    else
    {
      digitalWrite(motor1_dir, LOW);
      delay(EMF_wait_buffer_msecs);
    }
  }
  else if(motor == 2)
  {
    motor2_forward = forward;
    if(forward)
    {
      digitalWrite(motor2_dir, HIGH);
      delay(EMF_wait_buffer_msecs);
    }
    else
    {
      digitalWrite(motor2_dir, LOW);
      delay(EMF_wait_buffer_msecs);
    }
  }
}

void slow_stop_motor(int motor)
{
  if(motor == 1)
  {
    motor1_enabled = false;
    motor1_stopped = true; 
    digitalWrite(motor1_en, LOW);
  }
  else if (motor == 2)
  {
    motor2_enabled = false;
    motor2_stopped = true;
    digitalWrite(motor2_en, LOW);
  }
}

void enable_motor(int motor)
{
  if(motor == 1)
  {
    digitalWrite(motor1_en, HIGH);
    motor1_enabled = true;
  }
  else if (motor == 2)
  {
    digitalWrite(motor2_en, HIGH);
    motor2_enabled = true;
  }
}

void quick_stop_motor(int motor)
{
  if(motor == 1)
  {
    motor1_stopped = true;
  }
  else if (motor == 2)
  {
    motor2_stopped = true;
  }
}

void motor1_signal( const std_msgs::Int16& msg)
{
  int cmd = msg.data;
  if(msg.data < 0)
  {
    if(motor1_forward)
      change_motor_direction(1,false);
  }
  else if (msg.data > 0)
  {
    if(!motor1_forward)
      change_motor_direction(1,true);
  }
  else if (msg.data == 0)
  {
    quick_stop_motor(1);
  }
  analogWrite(motor1_pwm, abs(msg.data));
}

void motor2_signal( const std_msgs::Int16& msg)
{
  if(msg.data < 0)
  {
    if(motor2_forward)
      change_motor_direction(2,false);
  }
  else if (msg.data > 0)
  {
    if(motor2_forward)
      change_motor_direction(2,true);
  }
  else if (msg.data == 0)
  {
    if(motor2_stopped == false)
      quick_stop_motor(2);
  }
  analogWrite(motor2_pwm, abs(msg.data));
}

void motor1_state( const std_msgs::Bool& msg)
{
  if(msg.data)
  {
    enable_motor(1);
  }
  else
  {
    slow_stop_motor(1); 
  }
}

void motor2_state( const std_msgs::Bool& msg)
{
  if(msg.data)
  {
    enable_motor(2);
  }
  else
  {
    slow_stop_motor(2); 
  }
}
ros::Subscriber<std_msgs::Int16> sub_motor2_signal("tara_firmware/motor2/signal", &motor2_signal );
ros::Subscriber<std_msgs::Int16> sub_motor1_signal("tara_firmware/motor1/signal", &motor1_signal );

ros::Subscriber<std_msgs::Bool> sub_motor2_state("tara_firmware/motor2/change_state", &motor2_state );
ros::Subscriber<std_msgs::Bool> sub_motor1_state("tara_firmware/motor1/change_state", &motor1_state );
void setup()
{
  pinMode(motor1_pwm, OUTPUT);
  pinMode(motor2_pwm, OUTPUT);
  pinMode(motor1_en, OUTPUT);
  pinMode(motor2_en, OUTPUT);
  pinMode(motor1_dir, OUTPUT);
  pinMode(motor2_dir, OUTPUT);
  
  digitalWrite(motor1_en, LOW);
  digitalWrite(motor2_en, LOW);
  digitalWrite(motor1_dir, HIGH);
  digitalWrite(motor2_dir, HIGH);

  nh.initNode();
  nh.subscribe(sub_motor1_signal);
  nh.subscribe(sub_motor2_signal);
  nh.subscribe(sub_motor1_state);
  nh.subscribe(sub_motor2_state);
}

void loop()
{
  nh.spinOnce();
  delay(1);
}
