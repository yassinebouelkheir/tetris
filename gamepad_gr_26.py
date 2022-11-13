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

# setup radio to recieve/send messages
radio.on()
radio.config(group=group_id)

# create empty board + available pieces
board =[[1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1]]

brick = [0,0],[0,0]

x = 3
y = 0

def hideBrick():
    """
    hide the brick
    """
    global x, y, board, brick
    if x > 0:
        microbit.display.set_pixel(x-1,y,board[y][x])
    if x < 5:
        microbit.display.set_pixel(x+1-1,y,board[y][x+1])
    if x > 0 and y < 4:
        microbit.display.set_pixel(x-1,y+1,board[y+1][x])
    if x < 5 and y < 4:
        microbit.display.set_pixel(x+1-1,y+1,board[y+1][x+1])
        
def showBrick():
    """
    show the brick on the board
    """
    global x, y, board, brick
    if x > 0:
        microbit.display.set_pixel(x-1,y,max(brick[0][0],board[y][x]))
    if x < 5:
        microbit.display.set_pixel(x+1-1,y,max(brick[0][1],board[y][x+1]))
    if x > 0 and y < 4:
        microbit.display.set_pixel(x-1,y+1,max(brick[1][0],board[y+1][x]))
    if x < 5 and y < 4:   
        microbit.display.set_pixel(x+1-1,y+1,max(brick[1][1],board[y+1][x+1]))

def updateParameters(params):
    """
    updateParameters 
    """
    global x, y, brick, board
    param = params.split()

    brick[0][0] = int(param[0])
    brick[0][1] = int(param[1])
    brick[1][0] = int(param[2])
    brick[1][1] = int(param[3])
    x = int(param[4])
    y = int(param[5])
    if params[6] == 1:
        for i in range(0, 5):
            if (board[i][1]+board[i][2]+board[i][3]+board[i][4]+board[i][5])==45:
                for j in range(i,0,-1):
                    board[j] = board[j-1]
                board[0]=[1,0,0,0,0,0,1]
        for i in range(0, 5):
            for j in range(0, 5):
                microbit.display.set_pixel(i,j,board[j][i+1])


showBrick()
# create empty board + available pieces
while True:
    # get view of the board
    view = get_message()
    print(view)

    # show view of the board
    hideBrick()
    updateParameters(view)
    showBrick()
    
    # wait for button A or B to be pressed
    while not (microbit.button_a.is_pressed() or microbit.button_b.is_pressed()):
        microbit.sleep(50)

    if microbit.button_a.is_pressed():
        # send current direction
        direction = 1
        if microbit.accelerometer.get_x()> 350 :
            direction = '1 0'
        if microbit.accelerometer.get_y()< -350 :
            direction = '0 -1'
        if microbit.accelerometer.get_x()< -350 :
            direction = '-1 0'
        if microbit.accelerometer.get_y()>350 :
            direction = '0 1'
        radio.send("move " + str(direction))

    elif microbit.button_b.is_pressed():
        # notify that the piece should be dropped
        radio.send("drop")
        board[y][x]=max(brick[0][0],board[y][x])
        board[y][x+1]=max(brick[0][1],board[y][x+1])
        board[y+1][x]=max(brick[1][0],board[y+1][x])
        board[y+1][x+1]=max(brick[1][1],board[y+1][x+1])
