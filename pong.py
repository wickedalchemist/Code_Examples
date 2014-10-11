###
# See http://www.codeskulptor.org/#user28_1EBswB5vyRaW5l4.py for interactive game
###
###################
#
#PONG: Use up/down arrow and w/s keys to move padels of right/left side of canvas. 
# Ball increases in velocity over time, and resets to inital (slower) velocity when scored  
# Use reset button at the left of the frame to start a new game. 
# The ball initiates with a random velocity and direction
#
###################

# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - 
#pos and vel encode vertical info for paddles

#window parameters
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

#set initial ball and paddle positions/vel
LEFT = False
RIGHT = True
ball_pos=[WIDTH/2, HEIGHT/2]
score1=0
score2=0
paddle1_pos=[HALF_PAD_WIDTH,HEIGHT/2]
paddle2_pos=[(WIDTH-1)-HALF_PAD_WIDTH,HEIGHT/2]
paddle1_vel=0
paddle2_vel=0

def spawn_ball(direction):
    '''
     define fuction to initiate ball movement direction 
     and random velocity 
    '''
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos=[WIDTH/2, HEIGHT/2]
    if direction == 'RIGHT':
        ball_vel=[random.randrange(2,4), -random.randrange(1,3)]
    if direction == 'LEFT':
        ball_vel=[-1*random.randrange(2,4), -1*random.randrange(1,3)]        
        
# define event handlers
def new_game():
    '''
    Initiate a new game, reset scores, 
    and call spawn_ball function (above)
    '''
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1=0
    score2=0
    spawn_ball('RIGHT')
    
def restart():
    '''
    Resart game by calling new_game function (above)
    '''
    new_game()

def draw(c):
    '''
    Function to control ball/paddle position/velocity to draw on canvas
    '''
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 2, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 2, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 2, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # collide and reflect off of left/right hand side of canvas
    # change velocity if successfully reflect, else score
    if ball_pos[0] <= BALL_RADIUS:
        if (ball_pos[1] <= paddle1_pos[1]+PAD_HEIGHT/2) and (ball_pos[1] >= paddle1_pos[1]-PAD_HEIGHT/2):
            ball_vel[0] = - 1.10*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]
        else: 
            score2=score2+1
            spawn_ball('RIGHT')
            
    if ball_pos[0] >= (WIDTH-1)-BALL_RADIUS:
        if (ball_pos[1] <= paddle2_pos[1]+PAD_HEIGHT/2) and (ball_pos[1] >= paddle2_pos[1]-PAD_HEIGHT/2):
            ball_vel[0]=-1.1*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]
        else:
            score1=score1+1
            spawn_ball('RIGHT')
        
    #Top and Bottom wall reflections    
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1]=-ball_vel[1]
    if ball_pos[1] >= (HEIGHT-1)-BALL_RADIUS:
        ball_vel[1]=-ball_vel[1]

    # Draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 3, "Red", "White")
            
    # update paddle's vertical position, keeping paddle on the screen
    if (paddle1_pos[1]-PAD_HEIGHT/2) <= 0:   
       paddle1_pos=[paddle1_pos[0],PAD_HEIGHT/2]    
    if paddle1_pos[1] > 0:
       paddle1_pos=[paddle1_pos[0],paddle1_pos[1]+paddle1_vel]    
    if paddle1_pos[1]+PAD_HEIGHT/2 >= HEIGHT-1:   
       paddle1_pos=[paddle1_pos[0],(HEIGHT-1)-PAD_HEIGHT/2]    
    if paddle1_pos[1] < HEIGHT-PAD_WIDTH/2:
       paddle1_pos=[paddle1_pos[0],paddle1_pos[1]+paddle1_vel]    
    
    if paddle2_pos[1]-PAD_HEIGHT/2 <= 0:   
       paddle2_pos=[paddle2_pos[0],PAD_HEIGHT/2]    
    if paddle2_pos[1] > 0:
       paddle2_pos=[paddle2_pos[0],paddle2_pos[1]+paddle2_vel]    
    if paddle2_pos[1]+PAD_HEIGHT/2 >= HEIGHT-1:   
       paddle2_pos=[paddle2_pos[0],(HEIGHT-1)-PAD_HEIGHT/2]    
    if paddle2_pos[1] < HEIGHT-PAD_WIDTH/2:
       paddle2_pos=[paddle2_pos[0],paddle2_pos[1]+paddle2_vel]    
      
    # draw paddles
    c.draw_line([paddle1_pos[0],paddle1_pos[1]+PAD_HEIGHT/2],[paddle1_pos[0],paddle1_pos[1]-PAD_HEIGHT/2],PAD_WIDTH, 'Red')
    c.draw_line([paddle2_pos[0],paddle2_pos[1]+PAD_HEIGHT/2],[paddle2_pos[0],paddle2_pos[1]-PAD_HEIGHT/2],PAD_WIDTH, 'Red')
    
    # draw scores
    #Left player score
    c.draw_text(str(score1), [(WIDTH/2)-50,50], 30, 'White') 
    #Right player score
    c.draw_text(str(score2), [(WIDTH/2)+20,50], 30, 'White') 
    
def keydown(key):
    '''
    Associate paddle movements with keydown action
    '''
    global paddle1_vel, paddle2_vel
    acc = 3
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
            
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
     
def keyup(key):
    '''
    Associate paddle movements with keyup action
    '''
    global paddle1_vel, paddle2_vel    
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel =0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
resart_bottom = frame.add_button('Restart', restart)

# start frame
new_game()
frame.start()
