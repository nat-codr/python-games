# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.
# https://freesound.org/data/previews/4/4391_4948-lq.mp3
# https://freesound.org/data/previews/4/4389_4948-lq.mp3
# CodeSkulptor runs in Chrome 18+, Firefox 11+, and Safari 6+.
# Some features may work in other browsers, but do not expect
# full functionality.  It does NOT run in Internet Explorer.
screenWidth=700
screenHeight=500
paddleWidth=20
paddleVelocity=5

import simplegui
import random
soundTopBottom = simplegui.load_sound('https://freesound.org/data/previews/4/4391_4948-lq.mp3')
soundPaddle = simplegui.load_sound('https://freesound.org/data/previews/4/4389_4948-lq.mp3')
soundMiss = simplegui.load_sound('https://freesound.org/data/previews/420/420668_6544098-lq.mp3')
class GameManager:
    def __init__(self):
        self.p1Score = 0
        self.p2Score = 0
        

class Ball:
    def __init__(self):
        self.radius = 10
        self.center=[0,0]
        self.velocity=[0,0]
    
    def draw(self, canvas):
        canvas.draw_circle(self.center,self.radius, 2, 'White', 'White')
        
    def update(self):
        if self.center[1] <= self.radius or self.center[1] >= screenHeight - self.radius:
            self.velocity[1] = self.velocity[1] * -1
            soundTopBottom.play()
            
        self.center[0] = self.center[0] + self.velocity[0]
        self.center[1] = self.center[1] + self.velocity[1]
    
    def randomizeVelocity(self):
        return random.randrange(2, 6)
    
    def spawnLeft(self):
        x = self.randomizeVelocity()
        y = self.randomizeVelocity()
        self.velocity = [x * -1,y]
    
    
    def spawnRight(self):
        x = self.randomizeVelocity()
        y = self.randomizeVelocity()
        self.velocity = [x,y]
        
class Paddle:
    def __init__(self, pwidth):
        self.width= pwidth
        self.length=100
        self.velocity=0
        self.center=[0,0]

    def getTopEdge(self):
        return self.center[1] - self.length/2
    
    def getBottomEdge(self):
        return self.center[1] + self.length/2
    
    def getLeftEdge(self):
        return self.center[0] - self.width/2
    
    def getRightEdge(self):
        return self.center[0] + self.width/2
        
    def update(self):
        
        # check to see if paddle is at the top of the screen
        if self.velocity < 0 and self.center[1] - self.length * 0.5 <= 0:
            return
        # check to see if paddle is at the bottom of the screen
        if self.velocity > 0 and self.center[1] + self.length * 0.5 >= screenHeight:
            return
 
        self.center[1] = self.center[1] + self.velocity
        
    def draw(self, canvas):
        upperLeftCorner=[self.getLeftEdge(), self.getTopEdge()]
        upperRightCorner=[self.getRightEdge(), self.getTopEdge()]
        lowerLeftCorner=[self.getLeftEdge(), self.getBottomEdge()]
        lowerRightCorner=[self.getRightEdge(), self.getBottomEdge()]
        
        canvas.draw_polygon([upperLeftCorner,upperRightCorner,lowerRightCorner,lowerLeftCorner], 2, 'White', 'White')
        canvas.draw_line([screenWidth / 2, screenHeight], [screenWidth / 2, 0], 10, 'White')
        canvas.draw_text(str (gm.p1Score), [screenWidth / 4, 50], 50, 'White')
        canvas.draw_text(str (gm.p2Score), [screenWidth / 4 * 3, 50], 50, 'White')
        

# Handler to draw on canvas
def draw_handler(canvas):
    
    ballYCoordinate = b.center[1]
    ballXCoordinate = b.center[0]
    
    ballTouchingP2Paddle = ballYCoordinate >= p2.getTopEdge() and ballYCoordinate <= p2.getBottomEdge() and ballXCoordinate + b.radius >= p2.getLeftEdge()
    ballTouchingP1Paddle = ballYCoordinate >= p1.getTopEdge() and ballYCoordinate <= p1.getBottomEdge() and ballXCoordinate - b.radius <= p1.getRightEdge()
    
    P2PaddleMiss = not(ballYCoordinate >= p2.getTopEdge() and ballYCoordinate <= p2.getBottomEdge()) and ballXCoordinate + b.radius >= p2.getLeftEdge()
    P1PaddleMiss = not(ballYCoordinate >= p1.getTopEdge() and ballYCoordinate <= p1.getBottomEdge()) and ballXCoordinate - b.radius <= p1.getRightEdge()

    if ballTouchingP2Paddle or ballTouchingP1Paddle:
        # ball is touching right/left paddle so reflect the ball horizontally
        b.velocity[0] = b.velocity[0] * -1
        b.velocity[0] = b.velocity[0] * 1.05
        b.velocity[1] = b.velocity[1] * 1.05
        soundPaddle.play()
        
    if P2PaddleMiss:
        b.center = [screenWidth / 2, screenHeight / 2]
        b.spawnLeft()
        gm.p1Score += 1
        soundMiss.play()
        
    if P1PaddleMiss:
        b.center = [screenWidth / 2, screenHeight / 2]
        b.spawnRight()
        gm.p2Score += 1
        soundMiss.play()
        
    p1.update()
    p2.update()
    b.update()
    
    b.draw(canvas)

    p1.draw(canvas)
    p2.draw(canvas)
    #canvas.draw_text(message, [50,112], 48, "Red")
    
def keydown_handler(key):
    
    if key==simplegui.KEY_MAP["up"]:
        p2.velocity = paddleVelocity * -1
        
    if key==simplegui.KEY_MAP["down"]:
        p2.velocity = paddleVelocity

    if key==simplegui.KEY_MAP["w"]:
        p1.velocity = paddleVelocity * -1

    if key==simplegui.KEY_MAP["s"]:
        p1.velocity = paddleVelocity

def button_handler():
    start_game()

def keyup_handler(key):
    if key==simplegui.KEY_MAP["up"]:
        if p2.velocity < 0:
            p2.velocity = 0
    if key==simplegui.KEY_MAP["down"]:
        if p2.velocity > 0:
            p2.velocity = 0
    if key==simplegui.KEY_MAP["w"]:
        if p1.velocity < 0:
            p1.velocity = 0 
    if key==simplegui.KEY_MAP["s"]:
        if p1.velocity > 0:
            p1.velocity = 0
    
def start_game():
    global b
    global gm
    global p1
    global p2
    
    b = Ball()
    b.center=[screenWidth / 2,screenHeight / 2]
    b.radius=15
    gm = GameManager()
    b.spawnLeft()
    

    p1 = Paddle(paddleWidth)
    p2 = Paddle(paddleWidth)
    p1.center=[paddleWidth * 0.5,screenHeight * 0.5]
    p2.center=[screenWidth - paddleWidth * 0.5,screenHeight * 0.5]

    
# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", screenWidth, screenHeight)
#frame.add_button("Click me", click)
frame.set_draw_handler(draw_handler)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
button1 = frame.add_button('Restart', button_handler)
start_game()

# Start the frame animation
frame.start()