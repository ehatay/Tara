import rospy
from std_msgs.msg import Int16, Bool
from Tkinter import *

class motor_test_ui:
    def __init__(self, master):
        self.master = master
        self.master.title("TARA motor test tool")
        
        self.motor1_enabled = False
        self.motor2_enabled = False

        self.motor1_dir = True # True for forward, False for backward
        self.motor2_dir = True

        self.motor1_signal_pub = rospy.Publisher('tara_firmware/motor1/signal', Int16, queue_size = 1)
        self.motor2_signal_pub = rospy.Publisher('tara_firmware/motor2/signal', Int16, queue_size = 1)
        self.motor1_state_pub = rospy.Publisher('tara_firmware/motor1/change_state', Bool, queue_size = 1)
        self.motor2_state_pub = rospy.Publisher('tara_firmware/motor2/change_state', Bool, queue_size = 1)

        main_frame = Frame(width=800, height=600)
        main_frame.pack()

        left_frame = Frame(main_frame, width=800, height=600)
        left_frame.pack(side=LEFT)

        right_frame = Frame(main_frame, width=400, height=600)
        right_frame.pack_propagate(0)
        right_frame.pack(side=RIGHT)

        self.motor1_label = Label(left_frame, text="Motor1")
        self.motor1_label.pack()

        self.motor1_frame = Frame(left_frame, width=300, height=270, bd=2, background="light slate blue", colormap="new", relief=SUNKEN)
        self.motor1_frame.pack_propagate(0)
        self.motor1_frame.pack(fill=X, padx=5, pady=5)

        motor1_keypad = Frame(self.motor1_frame)
        motor1_keypad.place(in_=self.motor1_frame, anchor="c", relx=.5, rely=.5)
        
        motor1_forward_button = Button(motor1_keypad, text="Direction", command=lambda: self.change_direction(1))
        motor1_forward_button.pack()

        self.motor1_state_label = Label(self.motor1_frame)
        self.motor1_state_label.pack(side=RIGHT)

        self.motor1_enable_button = Button(motor1_keypad, text="Enable", command=lambda: self.change_motor_state(1))    
        self.motor1_enable_button.pack()

        self.motor2_label = Label(left_frame, text="Motor2")
        self.motor2_label.pack()

        self.motor2_frame = Frame(left_frame, width=300,background="cornsilk2", height=270, bd=2,  colormap="new", relief=SUNKEN)
        self.motor2_frame.pack_propagate(0)
        self.motor2_frame.pack(fill=X, padx=5, pady=5)
        
        motor2_keypad = Frame(self.motor2_frame)
        motor2_keypad.place(in_=self.motor2_frame, anchor="c", relx=.5, rely=.5)
        
        motor2_forward_button = Button(motor2_keypad, text="Direction", command=lambda: self.change_direction(2))
        motor2_forward_button.pack()

        self.motor2_state_label = Label(self.motor2_frame)
        self.motor2_state_label.pack(side=RIGHT)

        self.motor2_enable_button = Button(motor2_keypad, text="Enable", command=lambda: self.change_motor_state(2))    
        self.motor2_enable_button.pack()
        
        self.close_button = Button(main_frame, text="Close", command=self.quit)
        self.close_button.pack(side = BOTTOM)
        
        
        base_keypad = Frame(right_frame)
        base_keypad.place(in_=right_frame, anchor="c", relx=.5, rely=.5)
        
        base_forward_button = Button(base_keypad, text="FORW ", command=lambda: self.base_move(1))
        base_forward_button.pack()

        base_backward_button = Button(base_keypad, text="BACKW", command=lambda: self.base_move(2))
        base_backward_button.pack()
        
        base_left_button = Button(base_keypad, text="LEFT ", command=lambda: self.base_move(3))
        base_left_button.pack()
        
        base_right_button = Button(base_keypad, text="RIGHT", command=lambda: self.base_move(4))
        base_right_button.pack()        
        
        base_stop_button = Button(base_keypad, text="STOP ", command=lambda: self.base_move(0))
        base_stop_button.pack()        
        
        self.update_state_text(1)
        self.update_state_text(2)
        

    def base_move(self, state):
        cmd1 = Int16()
        cmd2 = Int16()
        speed = 40
        if(state == 0): # STOP
            cmd1.data = 0
            cmd2.data = 0
        elif(state == 1): # FORWARD
            cmd1.data = speed
            cmd2.data = speed
        elif(state == 2): # BACKWARD
            cmd1.data = -speed
            cmd2.data = -speed
        elif(state == 3): # LEFT
            cmd1.data = speed
            cmd2.data = -speed
        elif(state == 4): # RIGHT
            cmd1.data = -speed
            cmd2.data = speed
        else:
            return
        self.motor1_signal_pub.publish(cmd1)
        self.motor2_signal_pub.publish(cmd2)
    
    def update_state_text(self, motor_num):
        if(motor_num == 1):
            text = ""
            if(self.motor1_enabled):
                text += "State: Enabled\n"
            else:
                text += "State: Disabled\n"
            if(self.motor1_dir):
                text += "Dir: Forward\n"
            else:
                text += "Dir: Backward\n"
            self.motor1_state_label['text'] = text
        elif(motor_num == 2):
            text = ""
            if(self.motor2_enabled):
                text += "State: Enabled\n"
            else:
                text += "State: Disabled\n"
            if(self.motor2_dir):
                text += "Dir: Forward\n"
            else:
                text += "Dir: Backward\n"
            self.motor2_state_label['text'] = text     

    def change_direction(self, motor_num):
        if(motor_num == 1):
            if(self.motor1_dir):
                print("Motor1 backward")
            else:
                print("Motor1 forward")
            self.motor1_dir = not self.motor1_dir
            mult = 1 if self.motor1_dir else -1
            self.motor1_signal_pub.publish(Int16(mult * 10))
        elif(motor_num == 2):
            if(self.motor2_dir):
                print("Motor2 backward")
            else:
                print("Motor2 forward")
            self.motor2_dir = not self.motor2_dir
            mult = 1 if self.motor2_dir else -1
            self.motor2_signal_pub.publish(Int16(mult * 10))
        self.update_state_text(motor_num)

    def change_motor_state(self, motor_num):
        if(motor_num == 1):
            if(self.motor1_enabled):
                self.motor1_enable_button['text'] = "Enable"
                print("Disabling Motor 1")
                self.motor1_enabled = False
            else:
                self.motor1_enable_button['text'] = "Disable"
                self.motor1_enabled = True
                print("Enabling Motor 2")
            self.motor1_state_pub.publish(Bool(self.motor1_enabled))
        elif(motor_num == 2):
            if(self.motor2_enabled):
                self.motor2_enable_button['text'] = "Enable"
                print("Disabling Motor 2")
                self.motor2_enabled = False 
            else:
                self.motor2_enable_button['text'] = "Disable"
                print("Enabling Motor 2")
                self.motor2_enabled = True
            self.motor2_state_pub.publish(Bool(self.motor2_enabled))
        self.update_state_text(motor_num)

    def quit(self):
        print("Exiting motor test tool...")
        self.master.quit()

rospy.init_node('Motor_test_tool')
root = Tk()
my_gui = motor_test_ui(root)
root.mainloop()
