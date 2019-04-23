#include <ros.h>
#include <std_msgs/Int16.h>
#include <std_msgs/Bool.h>
#include <std_msgs/Float32.h>

ros::NodeHandle nh;

/* Right motor */
const int motor1_l_pwm = 5;
const int motor1__l_en = 3;
const int motor1_r_en = 4;
const int motor1_r_pwm = 6;

boolean motor1_stopped = true;
boolean motor1_enabled = false;

/* Left motor */
const int motor2_l_pwm = 10;
const int motor2__l_en = 8;
const int motor2_r_en = 9;
const int motor2_r_pwm = 11;

boolean motor2_stopped = true;
boolean motor2_enabled = false;

const int EMF_wait_buffer_msecs = 50;

void slow_stop_motor(int motor)
{
  if(motor == 1)
  {
    motor1_enabled = false;
    motor1_stopped = true; 
    digitalWrite(motor1_r_en, LOW);    
    digitalWrite(motor1_l_en, LOW);
  }
  else if (motor == 2)
  {
    motor2_enabled = false;
    motor2_stopped = true;
    digitalWrite(motor2_r_en, LOW);
    digitalWrite(motor2_l_en, LOW);
  }
}

void enable_motor(int motor)
{
  if(motor == 1)
  {
    digitalWrite(motor1_r_en, HIGH);
    digitalWrite(motor1_l_en, HIGH);
    motor1_enabled = true;
  }
  else if (motor == 2)
  {
    digitalWrite(motor2_r_en, HIGH);
    digitalWrite(motor2_l_en, HIGH);
    motor2_enabled = true;
  }
}

void quick_stop_motor(int motor)
{
  if(motor == 1)
  {
    motor1_stopped = true;
    analogWrite(motor1_l_pwm, 0);
    analogWrite(motor1_r_pwm, 0);
  }
  else if (motor == 2)
  {
    analogWrite(motor2_r_pwm, 0);
    analogWrite(motor2_l_pwm, 0);
    motor2_stopped = true;
  }
}

void motor1_signal( const std_msgs::Float32& msg)
{
  if(msg.data < 0)
  {
    motor1_forward = false;
    digitalWrite(motor1_l_en, LOW);
    analogWrite(motor1_l_pwm, 0);
    analogWrite(motor1_r_pwm, abs(msg.data));
  }
  else if(msg.data > 0)
  {
    motor1_forward = true;
    digitalWrite(motor1_r_en, LOW);
    analogWrite(motor1_r_pwm, 0);
    analogWrite(motor1_l_pwm, abs(msg.data));
  }
  else if (msg.data == 0)
  {
    quick_stop_motor(1);
  }
}

void motor2_signal( const std_msgs::Float32& msg)
{
  if(msg.data < 0)
  {
    motor2_forward = false;
    digitalWrite(motor2_l_en, LOW);
    analogWrite(motor2_l_pwm, 0);
    analogWrite(motor2_r_pwm, abs(msg.data));
  }
  else if(msg.data > 0)
  {
    motor2_forward = true;
    digitalWrite(motor2_r_en, LOW);
    analogWrite(motor2_r_pwm, 0);
    analogWrite(motor2_l_pwm, abs(msg.data));
  }
  else if (msg.data == 0)
  {
    quick_stop_motor(2);
  }
}

void motor1_state( const std_msgs::Bool& msg)
{
  if(msg.data)
  {
    digitalWrite(motor1_l_en, HIGH);
    digitalWrite(motor1_r_en, HIGH);
  }
  else
  {
    digitalWrite(motor1_r_en, LOW);
    digitalWrite(motor1_l_en, LOW);
  }
}

void motor2_state( const std_msgs::Bool& msg)
{
  if(msg.data)
  {
    digitalWrite(motor2_l_en, HIGH);
    digitalWrite(motor2_r_en, HIGH);
  }
  else
  {
    digitalWrite(motor2_r_en, LOW);
    digitalWrite(motor2_l_en, LOW);
  }
}
ros::Subscriber<std_msgs::Float32> sub_motor2_signal("tara_firmware/motor2/signal", &motor2_signal );
ros::Subscriber<std_msgs::Float32> sub_motor1_signal("tara_firmware/motor1/signal", &motor1_signal );

ros::Subscriber<std_msgs::Bool> sub_motor2_state("tara_firmware/motor2/change_state", &motor2_state );
ros::Subscriber<std_msgs::Bool> sub_motor1_state("tara_firmware/motor1/change_state", &motor1_state );

void setup()
{
  
  pinMode(motor1_r_pwm, OUTPUT);
  pinMode(motor2_r_pwm, OUTPUT);
  pinMode(motor1_l_pwm, OUTPUT);
  pinMode(motor2_l_pwm, OUTPUT);
  pinMode(motor1_l_en, OUTPUT);
  pinMode(motor1_r_en, OUTPUT);
  pinMode(motor2_r_en, OUTPUT);
  pinMode(motor2_l_en, OUTPUT);
    
  digitalWrite(motor1_l_en, HIGH);
  digitalWrite(motor1_r_en, HIGH);

  digitalWrite(motor2_r_en, HIGH);
  digitalWrite(motor2_l_en, HIGH);
  
  motor1_enabled = true;
  motor2_enabled = true;
  
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
