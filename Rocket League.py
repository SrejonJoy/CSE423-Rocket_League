from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
move_Flag_middle_left=False
move_Flag_middle_right=False
move_Flag_middle_up_left=False
move_Flag_middle_up_right=False
move_Flag_middle_up_middle=False
move_Flag_middle_down_right=False
move_Flag_middle_down_middle=False
move_Flag_middle_down_left=False
move_Flag_middle_down_left_half=False
restart=False
pause=False
ball_Y_Parameter=-210

total_count=50 
count=0
car1_move_power = 5
car2_move_power = 5
car1_right = True
car2_right = False
x_axis_move_Car_1 = 0
y_axis_move_Car_1 = 0
x_axis_move_Car_2 = 0
y_axis_move_Car_2 = 0
jump_speed = 5
gravity = 2
jump_speed2=5
gravity2 = 2
is_jumping = False
is_jumping2 =False
jump_height = 50
jump_height2 =50
current_jump_height = 0
current_jump_height2 = 0
key_states = {}
key_states2={}
boost_active2=False
boost_active = False
boost_available2=True
boost_available=True
boost_meter1=0
boost_meter2=0
car1_u=-220
car1_l=-248
car1_r= -210 
car1_d=-240# Flag to track if boost is active
car1_center_x=-229
car1_center_y=-230
car1_width=abs(car1_l-car1_r)
car1_height=abs(car1_u-car1_d)

car2_u=-220
car2_l=248
car2_r=210 
car2_d=-240# Flag to track if boost is active
car2_center_x=229
car2_center_y=-230
car2_width=abs(car2_l-car2_r)
car2_height=abs(car2_u-car2_d)
ball_x=0
ball_y=-220
ball_width=30
ball_height=30
x_axis_move_ball=0
y_axis_move_ball=0
ball_velocity_y = 0  
ball_velocity_x = 2  
ball_gravity = -0.2      
ball_damping = 0.8        
ground_y = -190   
left_bound = -250    
right_bound = 250 
ball_x_power=0
ball_y_power=0
x_axis_loop=0
car1_colour1=[[1.0,1.0,1.0],[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, 0.0, 1.0],[1.0, 1.0, 0.0]]
car2_colour1=[[1.0,1.0,1.0],[0.5, 0.0, 0.5],[1.0, 0.5, 0.0],[1.0, 0.0, 1.0],[0.0, 1.0, 1.0]]
car1_coulour=[1,1,1]
car2_coulour=[1,1,1]
car1_goals=0
car2_goals=0






def find_zone(x0,y0,x1,y1):
    dx = x1 -x0
    dy = y1 -y0
    zone=0

    if abs(dx)>abs(dy):
        if dx>=0 and dy>=0:
            zone=0
        elif dx<0 and dy>=0:
            zone=3
        elif dx<0 and dy<0:
            zone=4
        elif dx>=0 and dy<0:
            zone=7
    else:
        if dx>=0 and dy>=0:
            zone=1
        elif dx<0 and dy>=0:
            zone=2
        elif dx<0 and dy<0:
            zone=5
        elif dx>=0 and dy<0:
            zone=6
    return zone

def shift_zone(x0,y0,zone):
    if zone==0:
       x1=x0
       y1=y0
       y0=y1
       x0=x1
    elif zone==1:
       x1=x0
       y1=y0
       x0=y1
       y0=x1
    elif zone==2:
       x1=x0
       y1=y0
       x0=y1
       y0=-x1

    elif zone==3:
       x1=x0
       y1=y0
       x0=-x1
       y0=y1

    elif zone==4:
       x1=x0
       y1=y0
       x0=-x1
       y0=-y1

    elif zone==5:
       x1=x0
       y1=y0
       x0=-y1
       y0=-x1

    elif zone==6:
       x1=x0
       y1=y0
       x0=-y1
       y0=x1

    elif zone==7:
       x1=x0
       y1=y0
       x0=x0
       y0=-y1

    return (x0,y0)

####### Original Zone a shift kortesi ############

def original_zone(x0,y0,zone):
    if zone==0:
       x1=x0
       y1=y0
       y0=y1
       x0=x1
    elif zone==1:
       x1=x0
       y1=y0
       x0=y1
       y0=x1
    elif zone==2:
       x1=x0
       y1=y0
       x0=-y1
       y0=x1

    elif zone==3:
       x1=x0
       y1=y0
       x0=-x1
       y0=y1

    elif zone==4:
       x1=x0
       y1=y0
       x0=-x1
       y0=-y1

    elif zone==5:
       x1=x0
       y1=y0
       x0=-y1
       y0=-x1

    elif zone==6:
       x1=x0
       y1=y0
       x0=y1
       y0=-x1

    elif zone==7:
       x1=x0
       y1=y0
       x0=x0
       y0=-y1

    return (x0,y0)

move_Flag_middle_left,move_Flag_middle_right,move_Flag_middle_up_left,move_Flag_middle_up_right,move_Flag_middle_up_middle,move_Flag_middle_down_right,move_Flag_middle_down_middle,move_Flag_middle_down_left
############## MIDPOINT LINE DRAWING ALGORITHM ###########

def draw_line(x, y,size,colour):
    x0=x[0]
    x1=y[0]
    y0=x[1]
    y1=y[1]
    zone=find_zone(x0,y0,x1,y1)
    k=shift_zone(x0,y0,zone)
    l=shift_zone(x1,y1,zone)
    x0=k[0]
    y0=k[1]
    x1=l[0]
    y1=l[1]
    
    dx = x1 -x0

    dy = y1 -y0

    d=2*dy-dx

    incr_East =2*dy
    incr_NorthEast =2*(dy - dx)
    p = x0
    q = y0

    m=original_zone(p,q,zone)
    f0=m[0]
    f1=m[1]
    draw_points(f0, f1,size,colour)
    
    while (p < x1):
        if (d <= 0):
            d=d+incr_East
            p=p+1
        else:
            d=d+incr_NorthEast
            p=p+1
            q=q+1  
        
        m=original_zone(p,q,zone)
        f0=m[0]
        f1=m[1]
        draw_points(f0, f1,size,colour)

def draw_points(x, y, s,colour):
    glPointSize(s)
    glColor(colour[0],colour[1],colour[2]) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()


##########      MID POINT CIRCLE ALGORITHM     ################

def drawCircle(center_x, center_y, size, colour, radius):
    d = 1 - radius
    x = 0
    y = radius
    draw_points(x+center_x, y+center_y, size, colour)
    draw_points(y+center_x, x+center_y, size, colour)
    draw_points(-y+center_x, x+center_y, size, colour)
    draw_points(-x+center_x, -y+center_y, size, colour)
    draw_points(-x+center_x, y+center_y, size, colour)
    draw_points(-y+center_x, -x+center_y, size, colour)
    draw_points(x+center_x, -y+center_y, size, colour)
    draw_points(y+center_x, -x+center_y, size, colour)
    while x<y:
        if d<0:
            d=d+2*x+3
        else:
            d=d+2*x-2*y+5
            y=y-1
        x=x+1
        for zone in range(0,8):
            if zone==0:
                x1=x
                y1=y
                x0=y1
                y0=x1
                draw_points(x0+center_x, y0+center_y, size, colour)
            elif zone==1:
                x1=x
                y1=y
                x0=x1
                y0=y1
                draw_points(x0+center_x, y0+center_y, size, colour)
            elif zone==2:
                x1=x
                y1=y
                x0=-x1
                y0=y1
                draw_points(x0+center_x, y0+center_y, size, colour)
            elif zone==3:
                x1=x
                y1=y
                x0=-y1
                y0=x1
                draw_points(x0+center_x, y0+center_y, size, colour)
            elif zone==4:
                x1=x
                y1=y
                x0=-y1
                y0=-x1
                draw_points(x0+center_x, y0+center_y, size, colour)
            elif zone==5:
                x1=x
                y1=y
                x0=-x1
                y0=-y1
                draw_points(x0+center_x, y0+center_y, size, colour)
            elif zone==6:
                x1=x
                y1=y
                x0=x1
                y0=-y1
                draw_points(x0+center_x, y0+center_y, size, colour)
            elif zone==7:
                x1=x
                y1=y
                x0=y1
                y0=-x1
                draw_points(x0+center_x, y0+center_y, size, colour)
def terminate_game():
    import sys
    glutLeaveMainLoop() 

def restart1():
    global move_Flag_middle_left, move_Flag_middle_right, move_Flag_middle_up_left, move_Flag_middle_up_right
    global move_Flag_middle_up_middle, move_Flag_middle_down_right, move_Flag_middle_down_middle
    global move_Flag_middle_down_left, move_Flag_middle_down_left_half, key_states, key_states2
    global car1_move_power, car2_move_power, car1_right, car2_right
    global x_axis_move_Car_1, y_axis_move_Car_1, x_axis_move_Car_2, y_axis_move_Car_2
    global car1_u, car1_l, car1_r, car1_d, car1_center_x, car1_center_y, car1_width, car1_height
    global car2_u, car2_l, car2_r, car2_d, car2_center_x, car2_center_y, car2_width, car2_height
    global jump_speed, gravity, jump_speed2, gravity2, is_jumping, is_jumping2
    global jump_height, jump_height2, current_jump_height, current_jump_height2

    global ball_x, ball_y, ball_width, ball_height, x_axis_move_ball, y_axis_move_ball
    global ball_velocity_y, ball_velocity_x, ball_gravity, ball_damping
    global ground_y, left_bound, right_bound, ball_x_power, ball_y_power, x_axis_loop
    global boost_active2, boost_active, boost_available2, boost_available,ball_Y_Parameter,count,total_count
    global restart,pause,car1_coulour,car1_colour1,car2_coulour,car2_colour1,i1,i2,car1_goals,car2_goals
    move_Flag_middle_left=False
    move_Flag_middle_right=False
    move_Flag_middle_up_left=False
    move_Flag_middle_up_right=False
    move_Flag_middle_up_middle=False
    move_Flag_middle_down_right=False
    move_Flag_middle_down_middle=False
    move_Flag_middle_down_left=False
    move_Flag_middle_down_left_half=False
    restart=False
    pause=False
    ball_Y_Parameter=-210

    total_count=50 
    count=0
    car1_move_power = 5
    car2_move_power = 5
    car1_right = True
    car2_right = False
    x_axis_move_Car_1 = 0
    y_axis_move_Car_1 = 0
    x_axis_move_Car_2 = 0
    y_axis_move_Car_2 = 0
    jump_speed = 5
    gravity = 2
    jump_speed2=5
    gravity2 = 2
    is_jumping = False
    is_jumping2 =False
    jump_height = 50
    jump_height2 =50
    current_jump_height = 0
    current_jump_height2 = 0
    key_states = {}
    key_states2={}
    boost_active2=False
    boost_active = False
    boost_available2=True
    boost_available=True
    car1_u=-220
    car1_l=-248
    car1_r= -210 
    car1_d=-240# Flag to track if boost is active
    car1_center_x=-229
    car1_center_y=-230
    car1_width=abs(car1_l-car1_r)
    car1_height=abs(car1_u-car1_d)

    car2_u=-220
    car2_l=248
    car2_r=210 
    car2_d=-240# Flag to track if boost is active
    car2_center_x=229
    car2_center_y=-230
    car2_width=abs(car2_l-car2_r)
    car2_height=abs(car2_u-car2_d)
    ball_x=0
    ball_y=-220
    ball_width=30
    ball_height=30
    x_axis_move_ball=0
    y_axis_move_ball=0
    ball_velocity_y = 0  
    ball_velocity_x = 2  
    ball_gravity = -0.2      
    ball_damping = 0.8        
    ground_y = -190   
    left_bound = -250    
    right_bound = 250 
    ball_x_power=0
    ball_y_power=0
    x_axis_loop=0
    car1_colour1=[[1.0,1.0,1.0],[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, 0.0, 1.0],[1.0, 1.0, 0.0]]
    car2_colour1=[[1.0,1.0,1.0],[0.5, 0.0, 0.5],[1.0, 0.5, 0.0],[1.0, 0.0, 1.0],[0.0, 1.0, 1.0]]
    car1_coulour=[1,1,1]
    car2_coulour=[1,1,1]
    car1_goals=0
    car2_goals=0
    i1=0
    i2=0
# def hasCollided(box1_x,box1_y,box1_height,box1_width,box2_x,box2_y,box2_height,box2_width):
#     return (box1_x - box1_width/2) < (box2_x + box2_width/2)and(box1_x + box1_width/2) > (box2_x - box2_width/2) and(box1_y - box1_height/2) < (box2_y + box2_height/2)and(box1_y + box1_height/2) > (box2_y - box2_height/2)
def respawn():
    global move_Flag_middle_left, move_Flag_middle_right, move_Flag_middle_up_left, move_Flag_middle_up_right
    global move_Flag_middle_up_middle, move_Flag_middle_down_right, move_Flag_middle_down_middle
    global move_Flag_middle_down_left, move_Flag_middle_down_left_half, key_states, key_states2
    global car1_move_power, car2_move_power, car1_right, car2_right
    global x_axis_move_Car_1, y_axis_move_Car_1, x_axis_move_Car_2, y_axis_move_Car_2
    global car1_u, car1_l, car1_r, car1_d, car1_center_x, car1_center_y, car1_width, car1_height
    global car2_u, car2_l, car2_r, car2_d, car2_center_x, car2_center_y, car2_width, car2_height
    global jump_speed, gravity, jump_speed2, gravity2, is_jumping, is_jumping2
    global jump_height, jump_height2, current_jump_height, current_jump_height2

    global ball_x, ball_y, ball_width, ball_height, x_axis_move_ball, y_axis_move_ball
    global ball_velocity_y, ball_velocity_x, ball_gravity, ball_damping
    global ground_y, left_bound, right_bound, ball_x_power, ball_y_power, x_axis_loop
    global boost_active2, boost_active, boost_available2, boost_available,ball_Y_Parameter,count,total_count


    move_Flag_middle_left=False
    move_Flag_middle_right=False
    move_Flag_middle_up_left=False
    move_Flag_middle_up_right=False
    move_Flag_middle_up_middle=False
    move_Flag_middle_down_right=False
    move_Flag_middle_down_middle=False
    move_Flag_middle_down_left=False
    move_Flag_middle_down_left_half=False


    total_count=50 
    count=0
    car1_move_power = 5
    car2_move_power = 5
    car1_right = True
    car2_right = False
    x_axis_move_Car_1 = 0
    y_axis_move_Car_1 = 0
    x_axis_move_Car_2 = 0
    y_axis_move_Car_2 = 0
    jump_speed = 5
    gravity = 2
    jump_speed2=5
    gravity2 = 2
    is_jumping = False
    is_jumping2 =False
    jump_height = 50
    jump_height2 =50
    current_jump_height = 0
    current_jump_height2 = 0
    key_states = {}
    key_states2={}
    boost_active2=False
    boost_active = False
    boost_available2=True
    boost_available=True
    car1_u=-220
    car1_l=-248
    car1_r= -210 
    car1_d=-240# Flag to track if boost is active
    car1_center_x=-229
    car1_center_y=-230
    car1_width=abs(car1_l-car1_r)
    car1_height=abs(car1_u-car1_d)

    car2_u=-220
    car2_l=248
    car2_r=210 
    car2_d=-240# Flag to track if boost is active
    car2_center_x=229
    car2_center_y=-230
    car2_width=abs(car2_l-car2_r)
    car2_height=abs(car2_u-car2_d)

  
def goal():
    global move_Flag_middle_left, move_Flag_middle_right, move_Flag_middle_up_left, move_Flag_middle_up_right
    global move_Flag_middle_up_middle, move_Flag_middle_down_right, move_Flag_middle_down_middle
    global move_Flag_middle_down_left, move_Flag_middle_down_left_half, key_states, key_states2
    global car1_move_power, car2_move_power, car1_right, car2_right
    global x_axis_move_Car_1, y_axis_move_Car_1, x_axis_move_Car_2, y_axis_move_Car_2
    global car1_u, car1_l, car1_r, car1_d, car1_center_x, car1_center_y, car1_width, car1_height
    global car2_u, car2_l, car2_r, car2_d, car2_center_x, car2_center_y, car2_width, car2_height
    global jump_speed, gravity, jump_speed2, gravity2, is_jumping, is_jumping2
    global jump_height, jump_height2, current_jump_height, current_jump_height2

    global ball_x, ball_y, ball_width, ball_height, x_axis_move_ball, y_axis_move_ball
    global ball_velocity_y, ball_velocity_x, ball_gravity, ball_damping
    global ground_y, left_bound, right_bound, ball_x_power, ball_y_power, x_axis_loop
    global boost_active2, boost_active, boost_available2, boost_available,ball_Y_Parameter,count,total_count

    move_Flag_middle_left=False
    move_Flag_middle_right=False
    move_Flag_middle_up_left=False
    move_Flag_middle_up_right=False
    move_Flag_middle_up_middle=False
    move_Flag_middle_down_right=False
    move_Flag_middle_down_middle=False
    move_Flag_middle_down_left=False
    move_Flag_middle_down_left_half=False

    ball_Y_Parameter=-210

    total_count=50 
    count=0
    car1_move_power = 5
    car2_move_power = 5
    car1_right = True
    car2_right = False
    x_axis_move_Car_1 = 0
    y_axis_move_Car_1 = 0
    x_axis_move_Car_2 = 0
    y_axis_move_Car_2 = 0
    jump_speed = 5
    gravity = 2
    jump_speed2=5
    gravity2 = 2
    is_jumping = False
    is_jumping2 =False
    jump_height = 50
    jump_height2 =50
    current_jump_height = 0
    current_jump_height2 = 0
    key_states = {}
    key_states2={}
    boost_active2=False
    boost_active = False
    boost_available2=True
    boost_available=True
    car1_u=-220
    car1_l=-248
    car1_r= -210 
    car1_d=-240# Flag to track if boost is active
    car1_center_x=-229
    car1_center_y=-230
    car1_width=abs(car1_l-car1_r)
    car1_height=abs(car1_u-car1_d)

    car2_u=-220
    car2_l=248
    car2_r=210 
    car2_d=-240# Flag to track if boost is active
    car2_center_x=229
    car2_center_y=-230
    car2_width=abs(car2_l-car2_r)
    car2_height=abs(car2_u-car2_d)
    ball_x=0
    ball_y=-220
    ball_width=30
    ball_height=30
    x_axis_move_ball=0
    y_axis_move_ball=0
    ball_velocity_y = 0  
    ball_velocity_x = 2  
    ball_gravity = -0.2      
    ball_damping = 0.8        
    ground_y = -190   
    left_bound = -250    
    right_bound = 250 
    ball_x_power=0
    ball_y_power=0
    x_axis_loop=0

def hasCollided(box1_x,box1_y,box1_height,box1_width,box2_x,box2_y,box2_height,box2_width):
    # Check for collision
    collision = (box1_x - box1_width / 2) < (box2_x + box2_width / 2) and(box1_x + box1_width / 2) > (box2_x - box2_width / 2) and (box1_y - box1_height / 2) < (box2_y + box2_height / 2) and (box1_y + box1_height / 2) > (box2_y - box2_height / 2)
    
    if not collision:
        return "No Collision"  

    box1_center_x = box1_x
    box1_center_y = box1_y
    box2_center_x = box2_x
    box2_center_y = box2_y

    collision_part = ""

    # Vertical zones
    if box1_center_y > box2_center_y + box2_height / 4:
        collision_part += "Down "
    elif box1_center_y < box2_center_y - box2_height / 4:
        collision_part += "Up "
    else:
        collision_part += "Middle "

    # Horizontal zones
    if box1_center_x > box2_center_x + box2_width / 4:
        collision_part += "Left"
    elif box1_center_x < box2_center_x - box2_width / 4:
        collision_part += "Right"
    else:
        collision_part += "Middle"

    return collision_part

def convert_coordinate(x,y):
    a = x - (500/2)
    b = (500/2) - y 
    return a,b



def mouseListener(button, state, x, y):
    global pause	
    if button==GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):   
            c_X, c_y = convert_coordinate(x,y)
            if (c_X>=-250 and c_X<=-190) and (c_y>=205 and c_y<=250):
                print('Restart')
                restart1()
                
            elif (c_X>=-10 and c_X<=10) and (c_y>=215 and c_y<=235) :
                print("Pause")
                if pause==True:
                    pause=False
                else:
                    pause=True

            elif (c_X>=215 and c_X<=235) and (c_y>=215 and c_y<=235):
                print("Goodbye")
                terminate_game()

    glutPostRedisplay()
i1=0
i2=0
def keyboardListener(key, x, y):
    # global car1_colour1, car1_colour2, car1_colour3, car1_colour4, car2_colour1, car2_colour2,car2_colour3, car2_colour4
    global car1_coulour,car1_colour1,car2_coulour,car2_colour1,i1,i2,pause,car1_goals,car2_goals
    global y_axis_move_Car_1,key_states, is_jumping,boost_active,jump_height,jump_speed,car1_move_power,boost_available
    global y_axis_move_Car_2,key_states, is_jumping2,boost_active2,jump_height2,jump_speed2,car2_move_power,boost_available2
    key_states[key] = True
    if pause==False and car1_goals<3 and car2_goals<3:
        # if key == b'w':
        #     # print("W")
        #     # print(is_jumping)
        #     # print(y_axis_move_Car_1)
        if key == b'w' and not is_jumping and y_axis_move_Car_1<=0 : 
            # print('Space Pressed')
            is_jumping = True
            # print('Space Worked')
        if key == b'e' and boost_available==True:
            # Activate boost if possible
            boost_active = True  # Decrease boost counter
            jump_height +=3  # Increase jump height
            jump_speed += 3  # Increase jump speed
            car1_move_power+= 2

        if key == b'i' and not is_jumping2 and y_axis_move_Car_2<=0: 
            # print('Space Pressed')
            is_jumping2 = True
            # print('Space Worked')
        if key == b'o' and boost_available2==True:
            # Activate boost if possible
            boost_active2 = True  # Decrease boost counter
            jump_height2 +=3  # Increase jump height
            jump_speed2 += 3  # Increase jump speed
            car2_move_power+= 2
        if key==b'b': 
            i1+=1 
            if i1<4:
                car1_coulour=car1_colour1[i1]
            else:
                i1=0
                car1_coulour=car1_colour1[i1]
        if key==b'n':
            i2+=1 
            if i2<4:
                car2_coulour=car2_colour1[i2]
            else:
                i2=0
                car2_coulour=car2_colour1[i2]
    

def keyboardUp(key, x, y):
    global key_states
    key_states[key] = False      

    glutPostRedisplay()







move_Flag_middle_down_right_half=False
def display():
    
    global car2_height,car2_width,car2_center_y,car2_center_x,car2_r,car2_d,car2_u,car2_l,pause
    global car2_move_power,car2_right,x_axis_move_Car_2,y_axis_move_Car_2,jump_speed2,gravity2,is_jumping2,jump_height2 ,current_jump_height2
    global key_states2,boost_active2,boost_available2,car1_goals,car2_goals
    global ball_y_power,ball_x_power,y_axis_move_ball,x_axis_move_ball,ball_width,ball_height,ball_x,ball_y,car1_height,car1_width,car1_center_y,car1_center_x,car1_r,car1_d,car1_u,car1_l,car1_right,x_axis_move_Car_1, y_axis_move_Car_1, is_jumping, current_jump_height,jump_height,jump_speed,car1_right
    global ball_velocity_y, move_Flag_middle_right,ball_velocity_x, ball_gravity,ball_damping, ground_y,count,total_count,move_Flag_middle_left
    global ball_Y_Parameter,move_Flag_middle_down_left_half,move_Flag_middle_down_right_half
    global move_Flag_middle_left,move_Flag_middle_right,move_Flag_middle_up_left,move_Flag_middle_up_right,move_Flag_middle_up_middle,move_Flag_middle_down_right,move_Flag_middle_down_middle,move_Flag_middle_down_left
    if pause==False and car1_goals <3 and car2_goals<3:
    # print('jump_height',jump_height)
    # print('jump_speed',jump_speed)
    # Gravity and jump physicsddd
        if is_jumping:
            if current_jump_height < jump_height:
                # print('jump_height',jump_height)
                # print('cj',current_jump_height)
                y_axis_move_Car_1 += jump_speed
                current_jump_height += jump_speed
            else:
                is_jumping = False
        elif y_axis_move_Car_1 > 0:
            y_axis_move_Car_1 -= gravity
            current_jump_height -= gravity

        #######Second Car

        if is_jumping2:
            if current_jump_height2 < jump_height2:
                # print('jump_height',jump_height)
                # print('cj',current_jump_height)
                y_axis_move_Car_2 += jump_speed2
                current_jump_height2 += jump_speed2
            else:
                is_jumping2 = False
        elif y_axis_move_Car_2 > 0:
            y_axis_move_Car_2 -= gravity2
            current_jump_height2 -= gravity2



        if key_states.get(b'a', False) and car1_l>-248:
            car1_right=False
            x_axis_move_Car_1 -= car1_move_power
            
        if key_states.get(b'd', False) and car1_r<248:
            car1_right=True
            x_axis_move_Car_1 += car1_move_power


        if key_states.get(b'j', False) and car2_l>-248:
            car2_right=False
            x_axis_move_Car_2 -= car2_move_power
            
        if key_states.get(b'l', False) and car2_r<248:
            car2_right=True
            x_axis_move_Car_2 += car2_move_power
        

    
    #//clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0);	#//color black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #//load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    #//initialize the matrix
    glLoadIdentity()
    #//now give three info
    #//1. where is the camera (viewer)?
    #//2. where is the camera looking?
    #//3. Which direction is the camera's UP direction?
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)

    # draw_line([0,0],[0,155],1,[1,1,1])
    # draw_line([50,0],[50,155],1,[1,1,1])
    # # draw_line([-15,-25],[-40,90],2,[1,0,0])
    # drawCircle(50,0,1,[1,1,1],155)
    # (center_x, center_y, size, colour, radius)
    ########Boost Meter1 
    draw_line([-235,50],[-145,50],1,[0.933, 1.0, 0.0])
    draw_line([-235,70],[-145,70],1,[0.933, 1.0, 0.0])
    draw_line([-235,70],[-235,50],1,[0.933, 1.0, 0.0])
    draw_line([-145,50],[-145,70],1,[0.933, 1.0, 0.0])
    

    ##########Boost Meter 2
    draw_line([235,50],[145,50],1,[0.0, 1.0, 0.933])
    draw_line([235,70],[145,70],1,[0.0, 1.0, 0.933])
    draw_line([235,70],[235,50],1,[0.0, 1.0, 0.933])
    draw_line([145,50],[145,70],1,[0.0, 1.0, 0.933])

    ######## 3 BUTTONS ############
    ######left arrow##############
    draw_line([-235,225],[-200,225],1,[0.529, 0.808, 0.922])
    draw_line([-235,225],[-215,215],1,[0.529, 0.808, 0.922])
    draw_line([-235,225],[-215,235],1,[0.529, 0.808, 0.922])

    #########Pause Button #########
    if pause==False:
        draw_line([10,215],[10,235],1,[0.933, 1.0, 0.0])
        draw_line([-10,235],[-10,215],1,[0.933, 1.0, 0.0])
    else:
        draw_line([-10,235],[10,225],1,[1.0, 0.078, 0.576])
        draw_line([-10,215],[10,225],1,[1.0, 0.078, 0.576])
        draw_line([-10,235],[-10,215],1,[1.0, 0.078, 0.576])

    ######Boost Meter######


    ########CROSS BUTTON ###############
    draw_line([235,235],[215,215],1,[1,0,0])
    draw_line([215,235],[235,215],1,[1,0,0])
    ####GARI###########
    if car1_right==True:
        draw_line([-248+x_axis_move_Car_1,-240+y_axis_move_Car_1],[-210+x_axis_move_Car_1,-240+y_axis_move_Car_1],1,car1_coulour) #Garir nicher pasher daag
        draw_line([-248+x_axis_move_Car_1,-220+y_axis_move_Car_1],[-223+x_axis_move_Car_1,-220+y_axis_move_Car_1],1,car1_coulour) #uporer
        draw_line([-248+x_axis_move_Car_1,-220+y_axis_move_Car_1],[-248+x_axis_move_Car_1,-240+y_axis_move_Car_1],1,car1_coulour)#bamer 
        draw_line([-223+x_axis_move_Car_1,-220+y_axis_move_Car_1],[-210+x_axis_move_Car_1,-232+y_axis_move_Car_1],1,car1_coulour)#daner uporer
        draw_line([-210+x_axis_move_Car_1,-240+y_axis_move_Car_1],[-210+x_axis_move_Car_1,-232+y_axis_move_Car_1],1,car1_coulour)#daner nicher
        # draw_line([-210+x_axis_move_Car_1,-220+y_axis_move_Car_1],[-210+x_axis_move_Car_1,-240+y_axis_move_Car_1],1,car1_coulour)#Daner hitbox
        # draw_line([-248+x_axis_move_Car_1,-220+y_axis_move_Car_1],[-210+x_axis_move_Car_1,-220+y_axis_move_Car_1],1,car1_coulour)#Uporer hitbox
        #####Chaka#############
        drawCircle(-238+x_axis_move_Car_1,-245+y_axis_move_Car_1,1,car1_coulour,5)
        drawCircle(-220+x_axis_move_Car_1,-245+y_axis_move_Car_1,1,car1_coulour,5)
        car1_u=-220+y_axis_move_Car_1
        car1_r=-210+x_axis_move_Car_1
        car1_l=-248+x_axis_move_Car_1
        car1_d=-240+y_axis_move_Car_1
        # draw_points(car1_r, car1_d,5,[1,0,0])
        # draw_points(car1_r,car1_u,5,[0,1,0])
        # draw_points(car1_l, car1_d,5,[0,0,1])
        # draw_points(car1_l, car1_u,5,[0,1,1])
        # print(car1_r)
        # print(car1_l)
        car1_center_x=-229+x_axis_move_Car_1
        car1_center_y=-230+y_axis_move_Car_1
        # draw_points(car1_center_x, car1_center_y,5,[1,1,0])
        # print(car1_center_x,car1_center_y)
        # print('width:',car1_width,'Height:',car1_height)

    else:
        draw_line([-248+x_axis_move_Car_1,-240+y_axis_move_Car_1],[-210+x_axis_move_Car_1,-240+y_axis_move_Car_1],1,car1_coulour) #Garir nicher pasher daag
        draw_line([-235+x_axis_move_Car_1,-220+y_axis_move_Car_1],[-210+x_axis_move_Car_1,-220+y_axis_move_Car_1],1,car1_coulour) #uporer
        draw_line([-210+x_axis_move_Car_1,-220+y_axis_move_Car_1],[-210+x_axis_move_Car_1,-240+y_axis_move_Car_1],1,car1_coulour)#daner 
        draw_line([-235+x_axis_move_Car_1,-220+y_axis_move_Car_1],[-248+x_axis_move_Car_1,-232+y_axis_move_Car_1],1,car1_coulour)#daner uporer
        draw_line([-248+x_axis_move_Car_1,-240+y_axis_move_Car_1],[-248+x_axis_move_Car_1,-232+y_axis_move_Car_1],1,car1_coulour)#daner nicher
        # draw_line([-248+x_axis_move_Car_1,-220+y_axis_move_Car_1],[-248+x_axis_move_Car_1,-240+y_axis_move_Car_1],1,car1_coulour)#Daner hitboxs
        # draw_line([-248+x_axis_move_Car_1,-220+y_axis_move_Car_1],[-210+x_axis_move_Car_1,-220+y_axis_move_Car_1],1,car1_coulour)#Uporer hitbox

        #####Chaka#############
        drawCircle(-238+x_axis_move_Car_1,-245+y_axis_move_Car_1,1,car1_coulour,5)
        drawCircle(-220+x_axis_move_Car_1,-245+y_axis_move_Car_1,1,car1_coulour,5)
        # car1_u=-220+y_axis_move_Car_1
        # car1_r=-210+x_axis_move_Car_1
        # car1_l=-248+x_axis_move_Car_1
        # car1_d=-240+y_axis_move_Car_1
        # draw_points(car1_r, car1_d,5,[1,0,0])
        # draw_points(car1_r,car1_u,5,[0,1,0])
        # draw_points(car1_l, car1_d,5,[0,0,1])
        # draw_points(car1_l, car1_u,5,[0,1,1])
        # print(car1_r)
        # print(car1_l)
        car1_center_x=-229+x_axis_move_Car_1
        car1_center_y=-230+y_axis_move_Car_1
        # draw_points(car1_center_x, car1_center_y,5,[1,1,0])
        # print(car1_center_x,car1_center_y)
        # print('width:',car1_width,'Height:',car1_height)

    #####GARI 2     ###########
    if car2_right==False:
        draw_line([248+x_axis_move_Car_2,-240+y_axis_move_Car_2],[210+x_axis_move_Car_2,-240+y_axis_move_Car_2],1,car2_coulour) #Garir nicher pasher daag
        draw_line([248+x_axis_move_Car_2,-220+y_axis_move_Car_2],[223+x_axis_move_Car_2,-220+y_axis_move_Car_2],1,car2_coulour) #uporer
        draw_line([248+x_axis_move_Car_2,-220+y_axis_move_Car_2],[248+x_axis_move_Car_2,-240+y_axis_move_Car_2],1,car2_coulour)#bamer 
        draw_line([223+x_axis_move_Car_2,-220+y_axis_move_Car_2],[210+x_axis_move_Car_2,-232+y_axis_move_Car_2],1,car2_coulour)#daner uporer
        draw_line([210+x_axis_move_Car_2,-240+y_axis_move_Car_2],[210+x_axis_move_Car_2,-232+y_axis_move_Car_2],1,car2_coulour)#daner nicher
        # draw_line([210+x_axis_move_Car_2,-220+y_axis_move_Car_2],[210+x_axis_move_Car_2,-240+y_axis_move_Car_2],1,car2_coulour)#Daner hitbox
        # draw_line([248+x_axis_move_Car_2,-220+y_axis_move_Car_2],[210+x_axis_move_Car_2,-220+y_axis_move_Car_2],1,car2_coulour)#Uporer hitbox
        #####Chaka#############
        drawCircle(238+x_axis_move_Car_2,-245+y_axis_move_Car_2,1,car2_coulour,5)
        drawCircle(220+x_axis_move_Car_2,-245+y_axis_move_Car_2,1,car2_coulour,5)
        car2_u=-220+y_axis_move_Car_2
        car2_r=210+x_axis_move_Car_2
        car2_l=248+x_axis_move_Car_2
        car2_d=-240+y_axis_move_Car_2
        # draw_points(car2_r, car2_d,5,[1,0,0])
        # draw_points(car2_r,car2_u,5,[0,1,0])
        # draw_points(car2_l, car2_d,5,[0,0,1])
        # draw_points(car2_l, car2_u,5,[0,1,1])
        # print(car2_r)
        # print(car2_l)
        car2_center_x=229+x_axis_move_Car_2
        car2_center_y=-230+y_axis_move_Car_2
        # draw_points(car2_center_x, car2_center_y,5,[1,1,0])
        # print(car2_center_x,car2_center_y)
        # print('width:',car2_width,'Height:',car2_height)

    else:
        draw_line([248+x_axis_move_Car_2,-240+y_axis_move_Car_2],[210+x_axis_move_Car_2,-240+y_axis_move_Car_2],1,car2_coulour) #Garir nicher pasher daag
        draw_line([235+x_axis_move_Car_2,-220+y_axis_move_Car_2],[210+x_axis_move_Car_2,-220+y_axis_move_Car_2],1,car2_coulour) #uporer
        draw_line([210+x_axis_move_Car_2,-220+y_axis_move_Car_2],[210+x_axis_move_Car_2,-240+y_axis_move_Car_2],1,car2_coulour)#daner 
        draw_line([235+x_axis_move_Car_2,-220+y_axis_move_Car_2],[248+x_axis_move_Car_2,-232+y_axis_move_Car_2],1,car2_coulour)#daner uporer
        draw_line([248+x_axis_move_Car_2,-240+y_axis_move_Car_2],[248+x_axis_move_Car_2,-232+y_axis_move_Car_2],1,car2_coulour)#daner nicher
        # draw_line([248+x_axis_move_Car_2,-220+y_axis_move_Car_2],[248+x_axis_move_Car_2,-240+y_axis_move_Car_2],1,car2_coulour)#Daner hitboxs
        # draw_line([248+x_axis_move_Car_2,-220+y_axis_move_Car_2],[210+x_axis_move_Car_2,-220+y_axis_move_Car_2],1,car2_coulour)#Uporer hitbox

        #####Chaka#############
        drawCircle(238+x_axis_move_Car_2,-245+y_axis_move_Car_2,1,car2_coulour,5)
        drawCircle(220+x_axis_move_Car_2,-245+y_axis_move_Car_2,1,car2_coulour,5)
        car2_u=-220+y_axis_move_Car_2
        car2_r=210+x_axis_move_Car_2
        car2_l=248+x_axis_move_Car_2
        car2_d=-240+y_axis_move_Car_2
        # draw_points(car2_r, car2_d,5,[1,0,0])
        # draw_points(car2_r,car2_u,5,[0,1,0])
        # draw_points(car2_l, car2_d,5,[0,0,1])
        # draw_points(car2_l, car2_u,5,[0,1,1])
        # print(car2_r)
        # print(car2_l)
        car2_center_x=229+x_axis_move_Car_2
        car2_center_y=-230+y_axis_move_Car_2
        # draw_points(car2_center_x, car2_center_y,5,[1,1,0])
        # print(car2_center_x,car2_center_y)
        # print('width:',car2_width,'Height:',car2_height)

    #######BAll Drawing

    drawCircle(0+x_axis_move_ball,ball_Y_Parameter+y_axis_move_ball,1,[1,1,1],15)
    ball_x=0+x_axis_move_ball
    ball_y=ball_Y_Parameter+y_axis_move_ball
    ball_height=30
    ball_width=30

    ###GOAL POST
    # first goal post:
    draw_line([-220,-160],[-250,-160],1,[1,1,1])
    draw_line([-220,-250],[-220,-160],1,[1,1,1])

    # second goal post:
    draw_line([220,-160],[250,-160],1,[1,1,1])
    draw_line([220,-250],[220,-160],1,[1,1,1])

    draw_line([0,170],[0,165],1,[1,1,1])
    draw_line([0,155],[0,150],1,[1,1,1])

    if car1_goals==0:
            draw_line([-20,170],[-20,160],2,[1,1,1]) #daner
            draw_line([-40,170],[-40,160],2,[1,1,1]) #bamer
            draw_line([-25,180],[-35,180],2,[1,1,1]) #Uporer
            draw_line([-25,150],[-35,150],2,[1,1,1]) #nicher
            draw_line([-35,180],[-40,170],2,[1,1,1])
            draw_line([-25,180],[-20,170],2,[1,1,1])
            draw_line([-35,150],[-40,160],2,[1,1,1])
            draw_line([-25,150],[-20,160],2,[1,1,1])
    elif car1_goals==1:
            draw_line([-20,180],[-20,150],2,[1,1,1])
            draw_line([-20,180],[-30,165],2,[1,1,1])
    elif car1_goals==2:
            draw_line([-20,180],[-40,180],2,[1,1,1])
            draw_line([-20,165],[-40,165],2,[1,1,1]) 
            draw_line([-20,150],[-40,150],2,[1,1,1])
            draw_line([-20,180],[-20,165],2,[1,1,1])
            draw_line([-40,165],[-40,150],2,[1,1,1]) 
    elif car1_goals==3:
            draw_line([-20,180],[-40,180],2,[1,1,1])
            draw_line([-20,165],[-40,165],2,[1,1,1]) 
            draw_line([-20,150],[-40,150],2,[1,1,1])
            draw_line([-20,180],[-20,165],2,[1,1,1])
            draw_line([-20,165],[-20,150],2,[1,1,1]) 
    if car2_goals==0:
            draw_line([40,170],[40,160],2,[1,1,1]) #daner
            draw_line([20,170],[20,160],2,[1,1,1]) #bamer
            draw_line([35,180],[25,180],2,[1,1,1]) #Uporer
            draw_line([35,150],[25,150],2,[1,1,1]) #nicher
            draw_line([25,180],[20,170],2,[1,1,1])
            draw_line([35,180],[40,170],2,[1,1,1])
            draw_line([25,150],[20,160],2,[1,1,1])
            draw_line([35,150],[40,160],2,[1,1,1])
    elif car2_goals==1:
            draw_line([40,180],[40,150],2,[1,1,1])
            draw_line([40,180],[30,165],2,[1,1,1])
    elif car2_goals==2:
            draw_line([40,180],[20,180],2,[1,1,1])
            draw_line([40,165],[20,165],2,[1,1,1]) 
            draw_line([40,150],[20,150],2,[1,1,1])
            draw_line([40,180],[40,165],2,[1,1,1])
            draw_line([20,165],[20,150],2,[1,1,1])
    elif car2_goals==3:
            draw_line([40,180],[20,180],2,[1,1,1])
            draw_line([40,165],[20,165],2,[1,1,1]) 
            draw_line([40,150],[20,150],2,[1,1,1])
            draw_line([40,180],[40,165],2,[1,1,1])
            draw_line([40,165],[40,150],2,[1,1,1])  













        # print(ball_x,ball_y)
    col=hasCollided(ball_x,ball_y,ball_height,ball_width,car1_center_x,car1_center_y,car1_height,car1_width)
    col2=hasCollided(ball_x,ball_y,ball_height,ball_width,car2_center_x,car2_center_y,car2_height,car2_width)
    cars_col=hasCollided(car1_center_x,car1_center_y,car1_height,car1_width,car2_center_x,car2_center_y,car2_height,car2_width)
    if col!='No Collision':
        print(col)
        if col=='Up Left':
            # x_axis_move_ball+=car1_move_power*10
            # y_axis_move_ball-=car1_move_power*10
            # x_axis_move_Car_1 += -10
            # y_axis_move_Car_1 += 10
            # ball_x_power=+1
            # ball_y_power=-1
            if 0+x_axis_move_ball<235 :
                x_axis_move_ball+=0.5
                y_axis_move_ball+=2.5##BAll er first move
            x_axis_move_Car_1 -= 10 #Garir pichone jaoa
            ball_x_power=10 #Ball er x er dike jaoar power
            ball_y_power=0 #Ball er y er dike jaoar power
            move_Flag_middle_up_left=True #
            total_count=10


        elif col=='Up Right':
            if 0+x_axis_move_ball<235 and 0+x_axis_move_ball>-235 and ball_x_power>0:
                x_axis_move_ball-=car1_move_power*10
                y_axis_move_ball+=2.5 ##BAll er first move
            x_axis_move_Car_1 += 10 #Garir pichone jaoa
            ball_x_power=10 #Ball er x er dike jaoar power
            ball_y_power=0 #Ball er y er dike jaoar power
            move_Flag_middle_up_right=True #
            total_count=10

        elif col=='Up Middle':
            # y_axis_move_ball-=car1_move_power*10
            # ball_x_power=0
            # ball_y_power=-1
            pass

        elif col=='Down Left' :
            # x_axis_move_ball+=car1_move_power*10
            # y_axis_move_ball+=car1_move_power*10
            # x_axis_move_Car_1 += -10
            # y_axis_move_Car_1 += -10
            # ball_x_power=1
            # ball_y_power=1

            if 0+x_axis_move_ball<235 and 0+x_axis_move_ball>-235:
                x_axis_move_ball+=car1_move_power*10
                y_axis_move_ball+=car1_move_power*10##BAll er first move
            x_axis_move_Car_1 -= 10
            ball_x_power=1#Ball er x er dike jaoar power
            ball_y_power=1#Ball er y er dike jaoar power
            move_Flag_middle_down_left=True #
            total_count=10
            print("DHuklo")


        elif col=='Down Right' :
            # x_axis_move_ball-=car1_move_power*10
            # y_axis_move_ball+=car1_move_power*10
            # x_axis_move_Car_1 += 10
            # y_axis_move_Car_1 += -10
            # ball_x_power=-1
            # ball_y_power=1
            if 0+x_axis_move_ball<235 and 0+x_axis_move_ball>-235:
                x_axis_move_ball-=car1_move_power*10
                y_axis_move_ball+=car1_move_power*10 ##BAll er first move
            x_axis_move_Car_1 += 10
            # y_axis_move_Car_1 -= 10
            ball_x_power=1#Ball er x er dike jaoar power
            ball_y_power=1#Ball er y er dike jaoar power
            move_Flag_middle_down_right=True #
            total_count=10


        elif col=='Down Middle' :
            if 0+x_axis_move_ball<235 and ball_x_power>0:
                y_axis_move_ball+=car1_move_power*10 ##BAll er first move
            # y_axis_move_Car_1 -= 10 #Garir pichone jaoa
            ball_x_power=0 #Ball er x er dike jaoar power
            ball_y_power=10#Ball er y er dike jaoar power
            move_Flag_middle_down_middle=True #
            total_count=10


        elif col=='Middle Right' :
            if 0+x_axis_move_ball<235 and 0+x_axis_move_ball>-235 :
                x_axis_move_ball-=car1_move_power*10
                y_axis_move_ball+=car1_move_power*5 ##BAll er first move
            x_axis_move_Car_1 += 10 #Garir pichone jaoa
            ball_x_power=10 #Ball er x er dike jaoar power
            ball_y_power=0 #Ball er y er dike jaoar power
            move_Flag_middle_right=True #
            total_count=10
            
        elif col=='Middle Left' :
            if 0+x_axis_move_ball<235 :
                x_axis_move_ball+=car1_move_power*10
                y_axis_move_ball+=car1_move_power*5##BAll er first move
            x_axis_move_Car_1 -= 10 #Garir pichone jaoa
            ball_x_power=10 #Ball er x er dike jaoar power
            ball_y_power=0 #Ball er y er dike jaoar power
            move_Flag_middle_left=True #
            total_count=10
            

        elif col=='Middle Middle' :
            pass
    if col2!='No Collision':
        # print('COl2:',col2)
        if col2=='Up Left':
            # x_axis_move_ball+=car1_move_power*10
            # y_axis_move_ball-=car1_move_power*10
            # x_axis_move_Car_1 += -10
            # y_axis_move_Car_1 += 10
            # ball_x_power=+1
            # ball_y_power=-1
            if 0+x_axis_move_ball<235 :
                x_axis_move_ball+=0.5
                y_axis_move_ball+=2.5##BAll er first move
            x_axis_move_Car_2 -= 10 #Garir pichone jaoa
            ball_x_power=10 #Ball er x er dike jaoar power
            ball_y_power=0 #Ball er y er dike jaoar power
            move_Flag_middle_up_left=True #
            total_count=10


        elif col2=='Up Right':
            if 0+x_axis_move_ball<235 and 0+x_axis_move_ball>-235 and ball_x_power>0:
                x_axis_move_ball-=car2_move_power*10
                y_axis_move_ball+=2.5 ##BAll er first move
            x_axis_move_Car_2 += 10 #Garir pichone jaoa
            ball_x_power=10 #Ball er x er dike jaoar power
            ball_y_power=0 #Ball er y er dike jaoar power
            move_Flag_middle_up_right=True #
            total_count=10

        elif col2=='Up Middle':
            # y_axis_move_ball-=car1_move_power*10
            # ball_x_power=0
            # ball_y_power=-1
            pass

        elif col2=='Down Left' :
            # x_axis_move_ball+=car1_move_power*10
            # y_axis_move_ball+=car1_move_power*10
            # x_axis_move_Car_1 += -10
            # y_axis_move_Car_1 += -10
            # ball_x_power=1
            # ball_y_power=1

            if 0+x_axis_move_ball<235 and 0+x_axis_move_ball>-235:
                x_axis_move_ball+=car2_move_power*10
                y_axis_move_ball+=car2_move_power*10##BAll er first move
            x_axis_move_Car_2 -= 10
            ball_x_power=1#Ball er x er dike jaoar power
            ball_y_power=1#Ball er y er dike jaoar power
            move_Flag_middle_down_left=True #
            total_count=10
            # print("DHuklo")


        elif col2=='Down Right' :
            # x_axis_move_ball-=car1_move_power*10
            # y_axis_move_ball+=car1_move_power*10
            # x_axis_move_Car_1 += 10
            # y_axis_move_Car_1 += -10
            # ball_x_power=-1
            # ball_y_power=1
            if 0+x_axis_move_ball<235 and 0+x_axis_move_ball>-235:
                x_axis_move_ball-=car2_move_power*10
                y_axis_move_ball+=car2_move_power*10 ##BAll er first move
            x_axis_move_Car_2 += 10
            # y_axis_move_Car_1 -= 10
            ball_x_power=1#Ball er x er dike jaoar power
            ball_y_power=1#Ball er y er dike jaoar power
            move_Flag_middle_down_right=True #
            total_count=10


        elif col2=='Down Middle' :
            if 0+x_axis_move_ball<235 and ball_x_power>0:
                y_axis_move_ball+=car2_move_power*10 ##BAll er first move
            # y_axis_move_Car_1 -= 10 #Garir pichone jaoa
            ball_x_power=0 #Ball er x er dike jaoar power
            ball_y_power=10#Ball er y er dike jaoar power
            move_Flag_middle_down_middle=True #
            total_count=10


        elif col2=='Middle Right' :
            if 0+x_axis_move_ball<235 and 0+x_axis_move_ball>-235 :
                x_axis_move_ball-=car2_move_power*10
                y_axis_move_ball+=car2_move_power*5 ##BAll er first move
            x_axis_move_Car_2 += 10 #Garir pichone jaoa
            ball_x_power=10 #Ball er x er dike jaoar power
            ball_y_power=0 #Ball er y er dike jaoar power
            move_Flag_middle_right=True #
            total_count=10
            
        elif col2=='Middle Left' :
            if 0+x_axis_move_ball<235 :
                x_axis_move_ball+=car2_move_power*10
                y_axis_move_ball+=car2_move_power*5##BAll er first move
            x_axis_move_Car_2 -= 10 #Garir pichone jaoa
            ball_x_power=10 #Ball er x er dike jaoar power
            ball_y_power=0 #Ball er y er dike jaoar power
            move_Flag_middle_left=True #
            total_count=10
            

        elif col=='Middle Middle' :
            pass
    if cars_col!='No Collision':
        respawn()
    j=-235+boost_meter1 
    # print('j',j)  
    if j<-144:
        j=-235+boost_meter1
    else:
        j=-144
    draw_line([-235,50],[j,50],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,51],[j,51],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,52],[j,52],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,53],[j,53],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,54],[j,54],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,55],[j,55],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,56],[j,56],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,57],[j,57],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,58],[j,58],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,59],[j,59],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,60],[j,60],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,61],[j,61],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,62],[j,62],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,63],[j,63],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,64],[j,64],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,65],[j,65],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,66],[j,66],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,67],[j,67],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,68],[j,68],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,69],[j,69],0.6,[0.933, 1.0, 0.0])
    draw_line([-235,70],[j,70],0.6,[0.933, 1.0, 0.0])
    k=145+boost_meter2
    # print('k',k)  
    if k<234:
        k=145+boost_meter2
    else:
        k=234
    draw_line([145,50],[k,50],0.6,[0.0, 1.0, 0.933])
    draw_line([145,51],[k,51],0.6,[0.0, 1.0, 0.933])
    draw_line([145,52],[k,52],0.6,[0.0, 1.0, 0.933])
    draw_line([145,53],[k,53],0.6,[0.0, 1.0, 0.933])
    draw_line([145,54],[k,54],0.6,[0.0, 1.0, 0.933])
    draw_line([145,55],[k,55],0.6,[0.0, 1.0, 0.933])
    draw_line([145,56],[k,56],0.6,[0.0, 1.0, 0.933])
    draw_line([145,57],[k,57],0.6,[0.0, 1.0, 0.933])
    draw_line([145,58],[k,58],0.6,[0.0, 1.0, 0.933])
    draw_line([145,59],[k,59],0.6,[0.0, 1.0, 0.933])
    draw_line([145,60],[k,60],0.6,[0.0, 1.0, 0.933])
    draw_line([145,61],[k,61],0.6,[0.0, 1.0, 0.933])
    draw_line([145,62],[k,62],0.6,[0.0, 1.0, 0.933])
    draw_line([145,63],[k,63],0.6,[0.0, 1.0, 0.933])
    draw_line([145,64],[k,64],0.6,[0.0, 1.0, 0.933])
    draw_line([145,65],[k,65],0.6,[0.0, 1.0, 0.933])
    draw_line([145,66],[k,66],0.6,[0.0, 1.0, 0.933])
    draw_line([145,67],[k,67],0.6,[0.0, 1.0, 0.933])
    draw_line([145,68],[k,68],0.6,[0.0, 1.0, 0.933])
    draw_line([145,69],[k,69],0.6,[0.0, 1.0, 0.933])
    draw_line([145,70],[k,70],0.6,[0.0, 1.0, 0.933])
    glutSwapBuffers()


total_frame=150
frame=0
nframe=0
nto=90
total_count=10 
count=0

total_frame2=150
frame2=0
nframe2=0
nto2=90
def animate():
    global car2_height,car2_width,car2_center_y,car2_center_x,car2_r,car2_d,car2_u,car2_l
    global car2_move_power,car2_right,x_axis_move_Car_2,y_axis_move_Car_2,jump_speed2,gravity2,is_jumping2,jump_height2 ,current_jump_height2
    global key_states2,boost_active2,boost_available2,boost_meter1,boost_meter2
    global x_axis_loop,ball_x_power,ball_y_power,x_axis_move_ball,y_axis_move_ball,ball_width,ball_height,ball_x,ball_y,car1_height,car1_width,car1_center_y,car1_center_x,car1_r,car1_d,car1_u,car1_l,car1_right,x_axis_move_Car_1, y_axis_move_Car_1,jump_height,jump_speed,car1_move_power,boost_active,frame,total_frame,nframe,nto,boost_available
    global move_Flag_middle_down_left_half,count,total_count,move_Flag_middle_left,move_Flag_middle_right,move_Flag_middle_down_right_half
    global move_Flag_middle_left,move_Flag_middle_right,move_Flag_middle_up_left,move_Flag_middle_up_right,move_Flag_middle_up_middle,move_Flag_middle_down_right,move_Flag_middle_down_middle,move_Flag_middle_down_left
    global total_frame2,frame2,nframe2,nto2,car2_goals,car1_goals
    if pause==False and car1_goals<3 and car2_goals<3:
        if boost_active==True:
            frame+=1
            boost_meter1-=0.6
            if frame>total_frame:
                boost_active=False
                boost_available=False
                jump_height=50
                jump_speed=5
                car1_move_power=5
                total_frame=150
                frame=0
                
        else:
            nframe+=1
            boost_meter1+=1
            if nframe>nto:
                boost_available=True
                nframe=0
                nto=90
                boost_meter1=90

        ###Second Garir Boost Logic

        if boost_active2==True:
            frame2+=1
            boost_meter2-=0.6
            if frame2>total_frame2:
                boost_active2=False
                boost_available2=False
                jump_height2=50
                jump_speed2=5
                car2_move_power=5
                total_frame2=150
                frame2=0
                
        else:
            nframe2+=1
            boost_meter2+=1
            if nframe2>nto:
                boost_available2=True
                nframe2=0
                nto2=90
                boost_meter2=90
        
        

        # print("Aikhane Paisi Move Flag",move_Flag_middle_left)
        if count <total_count and move_Flag_middle_left==True and 0+x_axis_move_ball<235 and 0+x_axis_move_ball>-235 and ball_x_power>0:
                ball_x_power-=0.3
                x_axis_move_ball+=ball_x_power
                y_axis_move_ball+=ball_y_power
                count+=0.5
                # print(count,total_count)
                if count >=total_count or 0+x_axis_move_ball<220 and 0+x_axis_move_ball>-235:
                    count=0 
                    move_Flag_middle_left=False
        else:
            move_Flag_middle_left=False

        # else:
        #     print("move_Flag_middle_left false")
        


        ######Middle Right Logic
        # print(count)
        # print(move_Flag_middle_right)
        # print(0+x_axis_move_ball)
        # print(ball_x_power)
        if count <total_count and move_Flag_middle_right==True and 0+x_axis_move_ball<220 and 0+x_axis_move_ball>-235 and ball_x_power>0:
                ball_x_power-=0.3
                x_axis_move_ball-=ball_x_power
                y_axis_move_ball+=ball_y_power
                count+=0.5
                if count >=total_count or 0+x_axis_move_ball<220 and 0+x_axis_move_ball>-235:
                    count=0 
                    move_Flag_middle_right=False
        else:
            move_Flag_middle_right=False
        # else:
        #     print("move_Flag_middle_right false")
        
        ######Down Left Logic

        if count <total_count and move_Flag_middle_down_left==True:# 
                if 0+x_axis_move_ball<220 and ball_x_power>0:
                    ball_x_power-=0.03
                    x_axis_move_ball+=ball_x_power
                    # print(x_axis_move_ball)
                    # print(y_axis_move_ball)
                    y_axis_move_ball+=ball_y_power
                    count+=0.3
                    if count >=total_count or 0+x_axis_move_ball>220 and 0+x_axis_move_ball<-235:
                        count=0 
                        move_Flag_middle_down_left=False
                        move_Flag_middle_down_left_half=True
                        ball_x_power=1.25
                        ball_y_power=2
                else:
                    move_Flag_middle_down_left==False
                    # print('ber hoilo')
                    # print(x_axis_move_ball)
                    # print(y_axis_move_ball)
        # else:
        #     print('move_Flag_middle_down_left false' )



        

        if move_Flag_middle_down_left_half==True and ball_Y_Parameter+y_axis_move_ball>-235 and 0+x_axis_move_ball<210 :
                x_axis_move_ball+=ball_x_power
                y_axis_move_ball-=ball_y_power
                count+=0.3
                # print('eshesche')
                # print(count)
                if count >=total_count or 0+x_axis_move_ball>240 and 0+x_axis_move_ball<-235:
                        count=0 
                        move_Flag_middle_down_left_half=False
        else:
            move_Flag_middle_down_left_half=False

        # else:
        #     print('move_Flag_middle_down_left_half false')

        # if ball_x==250 or ball_x==-250:
        #     x_axis_move_ball-=ball_x_power
        #     print('ashlo')


        #Down Right 
        if count <total_count and move_Flag_middle_down_right==True:
                if 0+x_axis_move_ball>-235 and ball_x_power>0: #and 0+x_axis_move_ball<235 and ball_x_power>0:
                    # print(count)
                    # print("X XIS",0+x_axis_move_ball)
                    # print('BAll Power',ball_x_power)
                    ball_x_power-=0.03
                    x_axis_move_ball-=ball_x_power
                    y_axis_move_ball+=ball_y_power
                    count+=0.3
                    # print(count,total_count)
                    if count >=total_count or 0+x_axis_move_ball>220 and 0+x_axis_move_ball<-235:
                        count=0 
                        move_Flag_middle_down_right=False
                        move_Flag_middle_down_right_half=True
                        ball_x_power=1.25
                        ball_y_power=2
                else:
                    move_Flag_middle_down_right==False
                    # print('ber hoilo')
                    # print(x_axis_move_ball)
                    # print(y_axis_move_ball)
                    # x_axis_move_ball=-210
        
        # else:
        #     print('move_Flag_middle_down_right false')
        if move_Flag_middle_down_right_half==True and ball_Y_Parameter+y_axis_move_ball>-235 and 0+x_axis_move_ball<210:
                x_axis_move_ball-=ball_x_power
                y_axis_move_ball-=ball_y_power
                count+=0.3
                # print(count,total_count)
                if count >=total_count or 0+x_axis_move_ball>240 and 0+x_axis_move_ball<-235:
                        count=0 
                        move_Flag_middle_down_right_half=False
        else:
            move_Flag_middle_down_right_half=False
        # else:
        #     print('move_Flag_middle_down_right_half false')

        ######Down Middle ############
        if count <total_count and move_Flag_middle_down_middle==True and 0+x_axis_move_ball<235 and (ball_x_power>0 or ball_y_power>0):
                ball_y_power-=0.8
                # x_axis_move_ball-=ball_x_power
                y_axis_move_ball+=ball_y_power
                count+=0.3
                # print(count,total_count)
                if count >=total_count or 0+x_axis_move_ball>220 and 0+x_axis_move_ball<-235:
                    count=0 
                    move_Flag_middle_down_middle=False
        else:
            move_Flag_middle_down_middle=False

        #####Up LEft Logic
        if count <total_count and move_Flag_middle_up_left==True and 0+x_axis_move_ball<220 and 0+x_axis_move_ball>-235 and ball_x_power>0:
                    ball_x_power-=0.3
                    x_axis_move_ball+=ball_x_power
                    y_axis_move_ball+=ball_y_power
                    count+=0.5
                    # print(count,total_count)
                    if count >=total_count or 0+x_axis_move_ball>240 and 0+x_axis_move_ball<-235:
                        count=0 
                        move_Flag_middle_up_left=False
        else:
            move_Flag_middle_up_left=False


        #####UP RIGHT
        if count <total_count and move_Flag_middle_up_right==True and 0+x_axis_move_ball<235 and 0+x_axis_move_ball>-235 and ball_x_power>0:
                ball_x_power-=0.3
                x_axis_move_ball-=ball_x_power
                y_axis_move_ball+=ball_y_power
                count+=0.5
                if count >=total_count or 0+x_axis_move_ball>240 and 0+x_axis_move_ball<-240:
                    count=0 
                    move_Flag_middle_up_right=False
                # print('dhukse')
        else:
            move_Flag_middle_up_right=False
        # else:
        #     # print('move_Flag_middle_up_right false')
        # print(move_Flag_middle_up_right,move_Flag_middle_down_left,move_Flag_middle_down_right,move_Flag_middle_up_left, move_Flag_middle_down_left_half,move_Flag_middle_down_right_half,move_Flag_middle_down_middle,move_Flag_middle_up_middle,move_Flag_middle_left,move_Flag_middle_right)
        if move_Flag_middle_up_right==False and  move_Flag_middle_up_left==False and move_Flag_middle_down_left_half==False and move_Flag_middle_down_right_half==False and move_Flag_middle_down_middle==False and move_Flag_middle_up_middle==False and move_Flag_middle_left==False and move_Flag_middle_right==False:
            # print("ashtese")
            if ball_Y_Parameter+y_axis_move_ball>-235:
                y_axis_move_ball-=1
                # print('komtese')
        # else:d
        #     print('dhuklona')
        ####### Check goal or not ########
        if 0+x_axis_move_ball<=-250:
            x_axis_move_ball=-240
        if 0+x_axis_move_ball>=250:
            x_axis_move_ball=240
        if x_axis_move_ball>220 and (ball_Y_Parameter+y_axis_move_ball==-160 or  ball_Y_Parameter+y_axis_move_ball>-162) :
            x_axis_move_ball=210
        if 0+x_axis_move_ball<-220 and (ball_Y_Parameter+y_axis_move_ball==-160 or  ball_Y_Parameter+y_axis_move_ball>-162):
            x_axis_move_ball=-210
            
        if 0+x_axis_move_ball<-220 and ball_Y_Parameter+y_axis_move_ball<-160:
            print('GOAL')
            car2_goals+=1
            goal()
            if car2_goals==3:
                print('Car2 winner')

        if 0+x_axis_move_ball>220 and ball_Y_Parameter+y_axis_move_ball<-160:
            print('GOAL 2')
            car1_goals+=1
            goal()
            if car1_goals==3:
                print('Car1 winner')
    # print(0+x_axis_move_ball,ball_Y_Parameter+y_axis_move_ball)
    
    

    
            
    # print(boost_available)

    
    
                
    

    
    
    # jump_height=50
    # jump_speed=5
    #//codes for any changes in Models, Camera
    glutPostRedisplay()


def init():
    #//clear the screen
    glClearColor(0,0,0,0)
    #//load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    #//initialize the matrix
    glLoadIdentity()
    #//give PERSPECTIVE parameters
    gluPerspective(104,	1,	1,	1000.0)
    # **(important)**aspect ratio that determines the field of view in the X direction (horizontally). The bigger this angle is, the more you can see of the world - but at the same time, the objects you can see will become smaller.
    #//near distance
    #//far distance


glutInit()
glutInitWindowSize(500,500)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color

# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"OpenGL Coding Practice")
init()

glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutKeyboardUpFunc(keyboardUp)
glutMouseFunc(mouseListener)	

glutMainLoop()		#The main loop of OpenGL
