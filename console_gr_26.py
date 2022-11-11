import math
from random import *

import radio
import microbit

# definition of functions
def get_message():
    """Wait and return a message from another micro:bit
    
    Returns
    -------
    message: message sent by another micro:bit (str)
    """
    message = None 
    while message == None:
        microbit.sleep(250) 
        message = radio.receive()
    return message

# settings 
group_id = 26

# setup radio to recieve orders 
radio.on()
radio.config(group=group_id)

# create empty board + available pieces
board =[[1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1]]

bricks = [[9,9],[9,0]],[[9,9],[0,9]],[[9,9],[9,9]],[[9,9],[0,0]]

x = 3
y = 0

def moveBrick(delta_x, delta_y, x, y):
    """
    Move the brick
    
    Returns
    -------
    move: return true if the function is executed
    """
    move=False
    if (delta_x==-1) and x > 0:
        if not ((board[y][x-1]>0 and brick[0][0]>0) or (board[y][x+1-1]>0 and brick[0][1]>0) or (board[y+1][x-1]>0 and brick[1][0]>0) or (board[y+1][x+1-1]>0 and brick[1][1]>0)):
            move=True
    elif delta_x==1 and x<5:
        if not ((board[y][x+1]>0 and brick[0][0]>0) or (board[y][x+1+1]>0 and brick[0][1]>0) or (board[y+1][x+1]>0 and brick[1][0]>0) or (board[y+1][x+1+1]>0 and brick[1][1]>0)):
            move=True
    elif delta_y==1 and y<4:   
        if not ((board[y+1][x]>0 and brick[0][0]>0) or (board[y+1][x+1]>0 and brick[0][1]>0) or (board[y+1+1][x]>0 and brick[1][0]>0) or (board[y+1+1][x+1]>0 and brick[1][1]>0)):
            move=True
    if move:     
        x+=delta_x
        y+=delta_y
    return move

def checkBoard():
    """
    Check if the board is full
    
    Returns
    -------
    removeLine: return true if the board is full
    """
    removeLine=False
    for i in range(0, 5):
        if (board[i][1]+board[i][2]+board[i][3]+board[i][4]+board[i][5])==45:
            removeLine = True
            for j in range(i,0,-1):
                board[j] = board[j-1]
            board[0]=[1,0,0,0,0,0,1]  
    return removeLine

def max(v_1, v_2):
    """
    Return the higher number
    
    Returns
    -------
    returns the max number
    """
    return (v_1 if (v_1 > v_2) else v_2) 

# loop until game is over
nb_dropped_pieces = 0
game_is_over  = False

while not game_is_over:
    # show score (number of pieces dropped)
    microbit.display.show(nb_dropped_pieces)

    # create a new piece in the top left corner 
    x=3
    y=0
    brick = choice(bricks)
    nb_dropped_pieces += 1
    game_is_over = False

    if not game_is_over:
        # ask orders until the current piece is dropped 
        piece_dropped = False

        while not piece_dropped:
            # send state of the board to gamepad (as a string)
            strx = ""
            for i in range(0,7):
                for j in range(0,7):
                    strx += str(board[i][j])
            for i in range(0,2):
                for j in range(0,2):
                    strx += str(brick[i][j])
            strx += str(x) +  str(y)
            strx = math.log(int(strx), 10)
            radio.send(str(strx))

            # wait until gamepad sends an order
            order = get_message()
            order.split()

            # execute order (drop or move piece)
            if order[0] == 'move':
                moveBrick(int(order[1]), int(order[2]), x, y)
            elif order[0] == 'drop':
                piece_dropped = True
                while(moveBrick(0,1, x, y)):
                    microbit.sleep(250)

                board[y][x]=max(brick[0][0],board[y][x])
                board[y][x+1]=max(brick[0][1],board[y][x+1])
                board[y+1][x]=max(brick[1][0],board[y+1][x])
                board[y+1][x+1]=max(brick[1][1],board[y+1][x+1])

        if checkBoard() == False and y==0:
            game_is_over = True

        # wait a few milliseconds and clear screen
        microbit.display.clear()

# tell that the game is over
microbit.display.scroll('Game is over', delay=100)
microbit.display.scroll('Score: ' + str(nb_dropped_pieces), delay=100)
