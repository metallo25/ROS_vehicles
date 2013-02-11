#!/usr/bin/env python
import roslib; roslib.load_manifest('drone_teleop')
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from std_msgs.msg import Float64
from turtlesim.msg import Velocity
import sys, select, termios, tty
import time
msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
up/down:       move forward/backward
left/right:    move left/right
w/s:           increase/decrease altitude
a/d:           turn left/right
t/l:           takeoff/land
r:             reset (toggle emergency state)
anything else: stop

please don't have caps lock on.
CTRL+c to quit
"""

xpos=0
ypos=0
move_bindings = {
		68:('linear', 'y', 0.1), #left
		67:('linear', 'y', -0.1), #right
		65:('linear', 'x', 0.1), #forward
		66:('linear', 'x', -0.1), #back
		'w':('linear', 'z', 0.1),
		's':('linear', 'z', -0.1),
		'a':('angular', 'z', 1),
		'd':('angular', 'z', -1),
	       }

def callback(RecMsg):
    
    global xpos #X coordinate of the vanishing point
    global ypos	#y coordinate of the vanishing point given out by dronecanny.cppp	
    xpos = RecMsg.linear
    ypos = RecMsg.angular
    

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key

if __name__=="__main__":
    	settings = termios.tcgetattr(sys.stdin)
	count=1
	vxxy=1
	Err=0.
	k=0.
	count2=0
	count1=0
	count3=0
	count4=0
	count5=0
	e=1
	rospy.init_node('drone_teleop')
	pub = rospy.Publisher('cmd_vel', Twist)
	land_pub = rospy.Publisher('/ardrone/land', Empty)
	reset_pub = rospy.Publisher('/ardrone/reset', Empty)
	takeoff_pub = rospy.Publisher('/ardrone/takeoff', Empty)
      	rospy.Subscriber('/drocanny/vanishing_points',Velocity,callback)
        toggle_pub=rospy.Publisher('/ardrone/togglecam', Empty)
	print msg
	time.sleep(5)	
	toggle_pub.publish(Empty())
	time.sleep(5)
	#takeoff_pub.publish(Empty())
	time.sleep(5)
	twist=Twist()
	while(True):
			
			time.sleep(0.1)	
			Err=0-xpos #getting the error	
			twist.linear.y=0.01*(ypos)	
			twist.linear.x=0.1				
			twist.angular.z=Err*0.01
			print twist.linear.y
			#print Err*0.01
			pub.publish(twist)
			time.sleep(0.1)
			twist.linear.x=0.0
			pub.publish(twist)
			
			
			
			
			
			
	
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)





