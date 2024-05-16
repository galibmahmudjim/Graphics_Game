import re
import glfw
from OpenGL.GL import *
import math
import random




#Base
colors= [[255,255,255],
[255,0,0],
[0,255,0],
[0,0,255],
[255,255,0],
[0,255,255],
[255,0,255],
[127,127,127]]
def get_zone(x0, y0, x1, y1):
    dx= x1-x0
    dy= y1-y0

    if dx>=0 and dy>=0:
        if dx > dy:
            return 0
        return 1

    elif dx>=0 and dy<0:
        if dx > abs(dy):
            return 7
        return 6

    elif dx<0 and dy>=0:
        if abs(dx) > dy :
            return 3
        return 2

    else:
        if abs(dx)>abs(dy):
            return 4
        return 5
def return_back(zone, x, y): # zone3 to all zones
    if zone == 0:
        return -x, y
    elif zone == 1:
        return y, -x
    elif zone == 2:
        return -y, -x 
    elif zone == 3:
        return x, y 
    elif zone == 4:
        return x, -y 
    elif zone == 5:
        return -y, x 
    elif zone == 6:
        return y, x 
    else:
        return -x, -y
def allZone_to_3(zone, x, y): #all zone to zone3
    if zone == 0:
        return -x, y
    elif zone == 1:
        return -y, x
    elif zone == 2:
        return -y, -x 
    elif zone == 3:
        return x, y 
    elif zone == 4:
        return x, -y 
    elif zone == 5:
        return y, -x 
    elif zone == 6:
        return y, x 
    else:
        return -x, -y
def draw_axes():
    glColor3ub(127, 127, 127)
    glBegin(GL_LINES)
    glVertex2f(-W/2, 0)
    glVertex2f(W/2-1, 0)
    glVertex2f(0, -H/2)
    glVertex2f(0, H/2-1)
    glEnd()
def draw_pixel(x, y, zone):
    x, y = return_back(zone, x, y)
    glVertex2f(x, y)
def draw_pixel_2(x,y):
    glVertex2f(x, y)
def draw_line_3(x0, y0, x1, y1, zone):
    dx = x1 - x0
    dy = y1 - y0
    x = x0
    y = y0
    d = -2 * dx + dy
    del_w = -2 * dy
    del_nw = -2 * (dx + dy)
    draw_pixel(x, y, zone)
    while (x > x1):
        if (d < 0):
            d += del_nw
            x -= 1
            y += 1
        else:
            d += del_w
            x -= 1
        draw_pixel(x, y, zone)
def draw_8_way(x,y,x_c,y_c):
   glColor3ub(255,255,255)
   glVertex2i(x_c+x,y_c+y)
   glVertex2i(x_c-x,y_c+y)
   glVertex2i(x_c+x,y_c-y)
   glVertex2i(x_c-x,y_c-y)
   glVertex2i(x_c+y,y_c+x)
   glVertex2i(x_c-y,y_c+x)
   glVertex2i(x_c+y,y_c-x)
   glVertex2i(x_c-y,y_c-x)
def draw_circle(r,x_c,y_c):
    glBegin(GL_POINTS)
    for i in range(r):
        x = -i+1
        y=0
        d= 5-4*(i+1)
        draw_8_way(x,y,x_c,y_c)
        while(x<y):
            if(d<0):
                d+=4*(3-2*y)
                y-=1
            else:
                d+= 4*(2*x-2*y+5)
                x+=1
                y-=1
            draw_8_way(x,y,x_c,y_c)
    glEnd()
#...........................


#constants
W, H = 1200, 800
FPS = 60
paddle_points = [(-W//20,-(H//2)+5),(-W//20,-(H//2)+25),(W//20,-(H//2)+25),(W//20,-(H//2)+5)]
PointerSize = 1
T = 3
TX, TY = 2,2
tx, ty = TX, TY

testing_flag = False

def construct_bricks(brick_width=W//20,brick_rows = 5):
    global W,H,PointerSize
    row_brick_number = 20
    brick_height = brick_width//2
    PointerSize = brick_height
    bricks_list = []
    for i in range(brick_rows):
        row_bricks = []
        for j in range(row_brick_number):
            one_brick = []
            p1_x = -(W//2) + (j)*brick_width + PointerSize/2
            p1_y = (H//2) - (i)*brick_height - PointerSize/2
            
            p2_x = p1_x + PointerSize
            p2_y = p1_y
            one_brick.append((p1_x,p1_y))
            one_brick.append((p2_x,p2_y))
            row_bricks.append(one_brick)

        bricks_list.append(row_bricks)
    return bricks_list

def draw_brick(brick_points,color):
    global PointerSize
    start_y = brick_points[0][1]
    
    start_x = brick_points[0][0]
    end_x = brick_points[1][0]
    
    red,green,blue = color
    
    y = start_y
    zone= get_zone(start_x, y, end_x, y)    
    x0, y0 = allZone_to_3(zone, start_x, y)      
    x1, y1 = allZone_to_3(zone, end_x, y)      
    glPointSize(PointerSize)
    glColor3ub(red,green,blue)
    glBegin(GL_POINTS)

    draw_line_3(x0, y0, x1, y1, zone)
    glEnd()
    glPointSize(1)

def draw_bricks(bricks_list,bricks_color_list,bricks_display_list):
    for i in range(len(bricks_list)):
        for j in range(len(bricks_list[i])):
            if bricks_display_list[i][j]:
                brick_points = bricks_list[i][j]
                color = bricks_color_list[i][j]
                draw_brick(brick_points,color)

def bricks_color(row,col)->list:
    color_list = []
    for i in range(row):
        temp_list = []
        for j in range(col):
            color = (random.randint(100,200),random.randint(100,200),random.randint(100,200))
            temp_list.append(color)
        color_list.append(temp_list)
    return color_list


def bricks_display(row,col):
    display_list = []
    for i in range(row):
        temp_list = []
        for j in range(col):
            temp_list.append(True)
        display_list.append(temp_list)
    return display_list


def draw_paddle(paddle_points):
    global testing_flag
    start_y = paddle_points[0][1]
    end_y = paddle_points[1][1]
    
    start_x = paddle_points[0][0]
    end_x = paddle_points[3][0]
    
    
    y = start_y
    glBegin(GL_POINTS)
    while y<=end_y:
        zone= get_zone(start_x, y, end_x, y)    
        x0, y0 = allZone_to_3(zone, start_x, y)      
        x1, y1 = allZone_to_3(zone, end_x, y)      

        glColor3ub(255,0,0)

        draw_line_3(x0, y0, x1, y1, zone)
        y+=1
    glEnd()
    
    if testing_flag:
        testing_flag = False

def move_paddle_right(paddle_points,move_amount=30):
    new_paddle_points = []
    if paddle_points[3][0]+move_amount<=(W//2)-1:
        for key,value in enumerate(paddle_points):
            new_paddle_points.append((value[0]+move_amount,value[1]))
    else:
        move_amount = ((W//2)) - paddle_points[3][0]        
        for key,value in enumerate(paddle_points):
            new_paddle_points.append((value[0]+move_amount,value[1]))
    return new_paddle_points        
def move_paddle_left(paddle_points,move_amount=30):
    new_paddle_points = []
    if paddle_points[0][0] - move_amount>= -(W//2):
        for key,value in enumerate(paddle_points):
            new_paddle_points.append((value[0]-move_amount,value[1]))
    else:
        move_amount = (-(W//2)) -  paddle_points[0][0]
        for key,value in enumerate(paddle_points):
            new_paddle_points.append((value[0]+move_amount,value[1]))
    return new_paddle_points

def check_collision(ball_center_x,ball_center_y,ball_radius,paddle_x1,paddle_y1,paddle_x2,paddle_y2):
    closest_x = clamp(ball_center_x, paddle_x1, paddle_x2)
    closest_y = clamp(ball_center_y, paddle_y1, paddle_y2)

    distance = ((closest_x - ball_center_x) ** 2 + (closest_y - ball_center_y) ** 2) ** 0.5

    if distance <= ball_radius:
        return True
    else:
        return False
def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def adjust_ball_angle(x1, y1, x2, y2, ball_x, ball_y, ball_radius):
    global tx, ty
    paddle_width = x2 - x1
    paddle_center_x = x1 + paddle_width / 2
    hit_position = (ball_x - paddle_center_x) / ((paddle_width-10)/ 2)
    influence = TX
    tx = round(abs(influence * hit_position) * math.copysign(1, tx) )
    ty = round(abs(TY))  


def check_brick_collision(circle_x, circle_y, circle_radius, rect_x1, rect_y1, rect_x2, rect_y2):
    closest_x = max(rect_x1, min(circle_x, rect_x2))
    closest_y = max(rect_y1, min(circle_y, rect_y2))
    distance_x = circle_x - closest_x
    distance_y = circle_y - closest_y
    distance_squared = distance_x**2 + distance_y**2
    distance_rectangle = math.sqrt((rect_x2-rect_x1)**2 + (rect_y2-rect_y1)**2)/2.0 + circle_radius
    distance_from_rectengle_center = math.sqrt(((rect_x1+rect_x2)/2.0 - circle_x)**2 + ((rect_y1+rect_y2)/2.0 - circle_y)**2)

    distance = math.sqrt(distance_squared) - circle_radius

    
    if distance_from_rectengle_center<=distance_rectangle and (distance_from_rectengle_center) >=(distance_rectangle-5):
            
            return False
    elif distance<=0:
            print(tx,ty)
            print(distance_from_rectengle_center,distance_rectangle)
            return True





def update_ball_position(brick_points,ball_center,ball_radius):
    global tx,ty, TX, TY
    p1,p2 = brick_points
    circle_x, circle_y = ball_center
    circle_radius = ball_radius
    rect_x1, rect_y1 = p1[0]-PointerSize//2,p1[1]-PointerSize//2
    rect_x2, rect_y2 = p2[0]+PointerSize//2,p2[1]-PointerSize//2
    if check_brick_collision(circle_x, circle_y, circle_radius, rect_x1, rect_y1, rect_x2, rect_y2):
        closest_x = max(rect_x1, min(circle_x, rect_x2))
        closest_y = max(rect_y1, min(circle_y, rect_y2))
        if closest_y == rect_y1:
            print("top")
            ty = abs(ty)*-1
        elif closest_y == rect_y2:
            print("bottom")
            ty = abs(ty)*1
        if closest_x == rect_x1:
            print("left")
            tx = abs(tx) * -1
        elif closest_x == rect_x2:
            print("right")
            tx = abs(tx)*1
        return True
    return False

def check_bricks_collision(bricks_list,bricks_display_list,ball_center_x,ball_center_y,ball_radius):
    for i in range(len(bricks_list)-1,-1,-1):
        for j in range(len(bricks_list[i])):
            if bricks_display_list[i][j]:
                brick_points = bricks_list[i][j]
                if update_ball_position(brick_points,(ball_center_x,ball_center_y),ball_radius):        
                    bricks_display_list[i][j] = False
                    return True
    return False

def key_callback(window, key, scancode, action, mods):
    global paddle_points,testing_flag
    if action == glfw.REPEAT or action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            testing_flag = True
            paddle_points = move_paddle_right(paddle_points)
        elif key==glfw.KEY_LEFT:
            testing_flag = True
            paddle_points = move_paddle_left(paddle_points)
        elif key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window,True)



def framebuffer_size_callback(window, width, height):
    global W, H, paddle_points,bricks_list,bricks_color_list,bricks_display_list
    W, H = width, height
    initialize()
    glViewport(0, 0, W, H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-W/2, W/2-1, -H/2, H/2-1, -1,1)


bricks_display_list = bricks_display(5,20)
bricks_list,bricks_color_list,paddle_points = [],[],[]
def initialize():
    global bricks_list,bricks_color_list,bricks_display_list,paddle_points, tx, ty, TX, TY
    bricks_list = construct_bricks(brick_rows=5, brick_width=W//20)
    bricks_color_list = bricks_color(5,20)
    paddle_points = [(-W//20,-(H//2)+5),(-W//20,-(H//2)+25),(W//20,-(H//2)+25),(W//20,-(H//2)+5)]
    frame_rate = FPS
    seconds_to_travel = T
    frames_to_travel = seconds_to_travel * frame_rate
    ty = round(H // frames_to_travel * math.copysign(1, ty))
    tx = round(ty * math.copysign(1, tx))
    TX, TY = tx, ty

def myEvent(Window):
            
        r,x_c,y_c  = 10,0,0
        
        global tx,ty
        
        total_score = 0
        initialize()
        x=0
        while not glfw.window_should_close(Window):     
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                
            glfw.poll_events()
            draw_bricks(bricks_list,bricks_color_list,bricks_display_list)
            draw_paddle(paddle_points)
            draw_circle(r,x_c,y_c)
            x_c += tx
            y_c += ty

            if check_collision(x_c,y_c,r,paddle_points[1][0],paddle_points[1][1],paddle_points[2][0],paddle_points[2][1]):
                 adjust_ball_angle(paddle_points[1][0],paddle_points[1][1],paddle_points[2][0],paddle_points[2][1], x_c, y_c, r)
                 
            if (x_c+r)>(W/2-1):
                tx *= -1
            if (x_c-r)<(-W/2):
                tx *= -1
            if (y_c+r)>(H/2-1):
                ty *= -1
            if (y_c-r)<(-H/2):
                ty *= -1
                print()
                print("Game Over")
                print(f"Your total score is = {total_score}")
                print()
                # break
            if check_bricks_collision(bricks_list,bricks_display_list,x_c,y_c,r):
                total_score += 1
                print()
                print(f"Current Score = {total_score}")
                print()



            glfw.swap_buffers(Window)
            glfw.poll_events()
        




def main():
    global W,H,FPS
    if not glfw.init():
        return
    
    monitor = glfw.get_primary_monitor()
    mode = glfw.get_video_mode(monitor)
    glfw.window_hint(glfw.RED_BITS, mode.bits.red)
    glfw.window_hint(glfw.GREEN_BITS, mode.bits.green)
    glfw.window_hint(glfw.BLUE_BITS, mode.bits.blue)
    glfw.window_hint(glfw.REFRESH_RATE, mode.refresh_rate)
    W, H = mode.size.width, mode.size.height
    FPS = mode.refresh_rate


    Window = glfw.create_window(mode.size.width, mode.size.height, "Polygon", None, None)

    if not Window:
        glfw.terminate()
        return
    glfw.set_framebuffer_size_callback(Window, framebuffer_size_callback)
    width, height = glfw.get_framebuffer_size(Window)

    framebuffer_size_callback(Window, width, height)

    glfw.make_context_current(Window)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-W/2, W/2-1, -H/2, H/2-1, -1,1)
    glfw.set_key_callback(Window,key_callback)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    myEvent(Window)
    glfw.swap_buffers(Window)
    glfw.poll_events()


    

    glfw.terminate()

main()