from turtle import st
from cv2 import circle
import glfw
from OpenGL.GL import *
import math
import random


W, H = 1200, 800
paddle_points = [(-W//20,-(H//2)+5),(-W//20,-(H//2)+25),(W//20,-(H//2)+25),(W//20,-(H//2)+5)]

PointerSize = 1
TX, TY = 2,2
tx, ty = TX, TY


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
            p1_x = -(W//2) + (j)*brick_width + PointerSize//2
            p1_y = (H//2) - (i)*brick_height - PointerSize//2
            p2_x = p1_x + PointerSize
            p2_y = p1_y
            row_bricks.append([[p1_x,p1_y],[p2_x,p2_y]])
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



def check_brick_collision(circle_x, circle_y, circle_radius, rect_x1, rect_y1, rect_x2, rect_y2):
    closest_x = max(rect_x1, min(circle_x, rect_x2))
    closest_y = max(rect_y1, min(circle_y, rect_y2))
    distance_x = circle_x - closest_x
    distance_y = circle_y - closest_y
    distance_squared = distance_x**2 + distance_y**2
    return distance_squared <= circle_radius**2


def update_ball_position(brick_points,ball_center,ball_radius):
    global tx,ty
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
            ty = TY*-1
        elif closest_y == rect_y2:
            print("bottom")
            ty = TY*1
        if closest_x == rect_x1:
            print("left")
            tx = TX*-1
        elif closest_x == rect_x2:
            print("right")
            tx = TX
        return True
    return False

def adjust_ball_angle(paddle_x, paddle_y, paddle_width, paddle_height, ball_x, ball_y, ball_radius, tx, ty):
    paddle_center_x = paddle_x + paddle_width / 2
    hit_position = (ball_x - paddle_center_x) / (paddle_width / 2)
    influence = 0.75
    tx = influence * hit_position * abs(ty)
    ty = -abs(ty)  
    return tx, ty

def update_ball_angle(ball_x, ball_y, ball_radius, paddle_x, paddle_y, paddle_width, paddle_height, tx, ty):
    if check_brick_collision(ball_x, ball_y, ball_radius, paddle_x, paddle_y, paddle_x + paddle_width, paddle_y + paddle_height):
        tx, ty = adjust_ball_angle(paddle_x, paddle_y, paddle_width, paddle_height, ball_x, ball_y, ball_radius, tx, ty)
    return round(tx), round(ty)


def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)


def check_bricks_collision(bricks_list,bricks_display_list,ball_center_x,ball_center_y,ball_radius):
    for i in range(len(bricks_list)-1,-1,-1):
        for j in range(len(bricks_list[i])):
            if bricks_display_list[i][j]:
                brick_points = bricks_list[i][j]
                if update_ball_position(brick_points,(ball_center_x,ball_center_y),ball_radius):        
                    print("Collision",i,j)
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
    bricks_list = construct_bricks(brick_rows=5, brick_width=W//20)
    glViewport(0, 0, W, H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-W/2, W/2-1, -H/2, H/2-1, -1,1)


bricks_list = construct_bricks(brick_rows=5, brick_width=W//20)
bricks_color_list = bricks_color(5,20)
bricks_display_list = bricks_display(5,20)


def myEvent(Window):
            
        r,x_c,y_c  = 10,0,0
        
        global tx,ty
        
        total_score = 0
        paddle_points = [(-W//20,-(H//2)+5),(-W//20,-(H//2)+25),(W//20,-(H//2)+25),(W//20,-(H//2)+5)]
        print(paddle_points)

        while not glfw.window_should_close(Window):     
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                
            glfw.poll_events()
            draw_bricks(bricks_list,bricks_color_list,bricks_display_list)
            draw_paddle(paddle_points)
            draw_circle(r,x_c,y_c)
            
            x_c += tx
            y_c += ty
            tx, ty = update_ball_angle(x_c, y_c, r, paddle_points[1][0],paddle_points[1][1],paddle_points[2][0],paddle_points[2][1], tx, ty)

            if check_collision(x_c,y_c,r,paddle_points[1][0],paddle_points[1][1],paddle_points[2][0],paddle_points[2][1]):
                ty *= -1
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
                break
            if check_bricks_collision(bricks_list,bricks_display_list,x_c,y_c,r):
                total_score += 1
                print()
                print(f"Current Score = {total_score}")
                print()
            glfw.swap_buffers(Window)
            glfw.poll_events()
        




def main():
    # Initialize GLFW
    if not glfw.init():
        return
    
    monitor = glfw.get_primary_monitor()
    W,H = glfw.get_monitor_workarea(monitor)[2:4]
  
    glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)
    Window = glfw.create_window(W, H, "Game", None, None)
    if not Window:
        glfw.terminate()
        return
    
    framebuffer_size_callback(Window, W, H)
    glfw.set_framebuffer_size_callback(Window, framebuffer_size_callback)


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