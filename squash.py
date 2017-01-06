#License MIT 2017 Ahmad Retha

import os
import pygame
import pygame.mixer

##
# Game mode
#
WIDTH = 480
HEIGHT = 640
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WIDTH, 25)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Squash')
clock = pygame.time.Clock()
pygame.key.set_repeat(50, 50)
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

##
# Game consts
#
FONT = pygame.font.Font(None, 40)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0 ,0, 255)
GRAY  = (100, 100, 100)
MODE_PLAY = 1
MODE_QUIT = 0
FRAME_RATE = 120

##
# Game Sounds and delay for losing
#
LOSE_DELAY = 500
LOSE_SOUND = pygame.mixer.Sound('beep-2.wav')
FAIL_SOUND = pygame.mixer.Sound('beep-3.wav')
LEFT_SOUND = pygame.mixer.Sound('beep-7.wav')
RIGHT_SOUND = pygame.mixer.Sound('beep-8.wav')
#LEFT_SOUND = pygame.mixer.Sound('beep-21.wav') #--too quiet!
#RIGHT_SOUND = pygame.mixer.Sound('beep-22.wav')

##
# Game Vars
#
BUDGE = 5
BALL_SPEED = 3
BALL_RADIUS = 4
PADDLE_SPEED = 3
PADDLE_SIZE = 70
PADDLE_THICKNESS = 4
LEFT_PLAYER = True
RIGHT_PLAYER = False
muted = False
speed_x = BALL_SPEED
speed_y = -BALL_SPEED
score_left = 0
score_right = 0
playerTurn = LEFT_PLAYER
current_mode = MODE_PLAY

##
# Action on player score
#
def score():
    global playerTurn, score_left, score_right, leftPaddle, rightPaddle, ball, speed_y
    if playerTurn == LEFT_PLAYER:
        score_left += 1                
        leftPaddle.x = WIDTH/4 - PADDLE_SIZE/2
        leftPaddle.y = HEIGHT - PADDLE_THICKNESS
        rightPaddle.x = WIDTH/4 * 3 - PADDLE_SIZE/2
        rightPaddle.y = HEIGHT/4 * 3 - PADDLE_THICKNESS
        ball.x = WIDTH/4 * 3
    else:
        score_right += 1
        leftPaddle.x = WIDTH/4 - PADDLE_SIZE/2
        leftPaddle.y = HEIGHT/4 * 3 - PADDLE_THICKNESS
        rightPaddle.x = WIDTH/4 * 3 - PADDLE_SIZE/2
        rightPaddle.y = HEIGHT - PADDLE_THICKNESS
        ball.x = WIDTH/4
    ball.y = HEIGHT/4 * 3 - PADDLE_THICKNESS - 2 * BALL_RADIUS
    speed_y = -abs(speed_y)
    return not playerTurn

##
# Game Objects
#
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, maxX, maxY, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.width = width
        self.height = height
        self.maxX = maxX
        self.maxY = maxY
        self.x = x
        self.y = y

    def move(self, moveX, moveY):
        self.y = self.y + moveY
        self.x = self.x + moveX

    def update(self):
        if self.y < self.maxY/2:
            self.y = self.maxY/2
        elif self.y > self.maxY:
            self.y = self.maxY
        if self.x < 0:
            self.x = 0
        elif self.x > self.maxX:
            self.x = self.maxX
        self.rect.topleft = [self.x, self.y]

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, x, y, radius):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([2*radius, 2*radius])
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.radius = radius
        self.x = x
        self.y = y

    def update(self):
        self.rect.topleft = [self.x, self.y]
        self.draw(screen)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, [self.x, self.y], self.radius)

leftPaddle = Paddle(GREEN, PADDLE_SIZE, PADDLE_THICKNESS, WIDTH - PADDLE_SIZE, HEIGHT - PADDLE_THICKNESS, WIDTH/4 - PADDLE_SIZE/2, HEIGHT/4 * 3 - PADDLE_THICKNESS)
rightPaddle = Paddle(BLUE, PADDLE_SIZE, PADDLE_THICKNESS, WIDTH - PADDLE_SIZE, HEIGHT - PADDLE_THICKNESS, WIDTH/4 * 3 - PADDLE_SIZE/2, HEIGHT - PADDLE_THICKNESS) 
ball = Ball(BLACK, WIDTH/4 - BALL_RADIUS, HEIGHT/4 * 3 - PADDLE_THICKNESS - 2 * BALL_RADIUS, BALL_RADIUS)
spriteGroup = pygame.sprite.Group()
spriteGroup.add(leftPaddle)
spriteGroup.add(rightPaddle)
spriteGroup.add(ball)

##
# Game loop
#
while current_mode == MODE_PLAY:
    ##
    # Handle keyboard
    #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            current_mode = MODE_QUIT
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                current_mode = MODE_QUIT
            elif event.key == pygame.K_m:
                muted = not muted

    keysPressed = pygame.key.get_pressed()
    if keysPressed[pygame.K_UP] and keysPressed[pygame.K_LEFT]:
        rightPaddle.move(-PADDLE_SPEED, -PADDLE_SPEED)
    elif keysPressed[pygame.K_UP] and keysPressed[pygame.K_RIGHT]:
        rightPaddle.move(PADDLE_SPEED, -PADDLE_SPEED)
    elif keysPressed[pygame.K_DOWN] and keysPressed[pygame.K_LEFT]:
        rightPaddle.move(-PADDLE_SPEED, PADDLE_SPEED)
    elif keysPressed[pygame.K_DOWN] and keysPressed[pygame.K_RIGHT]:
        rightPaddle.move(PADDLE_SPEED, PADDLE_SPEED)
    elif keysPressed[pygame.K_UP]:
        rightPaddle.move(0, -PADDLE_SPEED)
    elif keysPressed[pygame.K_DOWN]:
        rightPaddle.move(0, PADDLE_SPEED)
    elif keysPressed[pygame.K_LEFT]:
        rightPaddle.move(-PADDLE_SPEED, 0)
    elif keysPressed[pygame.K_RIGHT]:
        rightPaddle.move(PADDLE_SPEED, 0)
    if keysPressed[pygame.K_w] and keysPressed[pygame.K_a]:
        leftPaddle.move(-PADDLE_SPEED, -PADDLE_SPEED)
    elif keysPressed[pygame.K_w] and keysPressed[pygame.K_d]:
        leftPaddle.move(PADDLE_SPEED, -PADDLE_SPEED)
    elif keysPressed[pygame.K_s] and keysPressed[pygame.K_a]:
        leftPaddle.move(-PADDLE_SPEED, PADDLE_SPEED)
    elif keysPressed[pygame.K_s] and keysPressed[pygame.K_d]:
        leftPaddle.move(PADDLE_SPEED, PADDLE_SPEED)
    elif keysPressed[pygame.K_w]:
        leftPaddle.move(0, -PADDLE_SPEED)
    elif keysPressed[pygame.K_s]:
        leftPaddle.move(0, PADDLE_SPEED)
    elif keysPressed[pygame.K_a]:
        leftPaddle.move(-PADDLE_SPEED, 0)
    elif keysPressed[pygame.K_d]:
        leftPaddle.move(PADDLE_SPEED, 0)

    ##
    # Draw arena, score and player turn color
    #
    screen.fill(WHITE)
    pygame.draw.line(screen, RED, [0, HEIGHT/2], [WIDTH, HEIGHT/2], 2)
    pygame.draw.line(screen, RED, [WIDTH/2, HEIGHT/2], [WIDTH/2, HEIGHT], 2)
    pygame.draw.rect(screen, RED, (0, HEIGHT/2, WIDTH/4, HEIGHT/4), 2)
    pygame.draw.rect(screen, RED, (WIDTH/4 * 3 - 1, HEIGHT/2, WIDTH/4, HEIGHT/4), 2)
    if playerTurn == RIGHT_PLAYER:
        pygame.draw.circle(screen, leftPaddle.color, [WIDTH/4, 20], 15)
    else:
        pygame.draw.circle(screen, rightPaddle.color, [WIDTH/4 * 3, 20], 15)
    text = FONT.render("%s:%s" % (str(score_left), str(score_right)), 1, GRAY)
    textpos = text.get_rect(centerx=WIDTH/2)
    screen.blit(text, textpos)

    ##
    # Move ball and update scores
    #
    if ball.y > HEIGHT:
        if not muted:
            LOSE_SOUND.play()
        playerTurn = score()
        pygame.time.delay(LOSE_DELAY)
    elif ball.y < 0:
        speed_y = -speed_y
    if ball.x > WIDTH:
        speed_x = -speed_x
    elif ball.x < 0:
        speed_x = abs(speed_x)
    ball.y = ball.y + speed_y
    ball.x = ball.x + speed_x

    ##
    # Bounce ball off paddles and paddles off each other
    #
    if leftPaddle.rect.colliderect(ball.rect):
        if playerTurn == LEFT_PLAYER:
            if not muted:
                FAIL_SOUND.play()
            playerTurn = score()
            pygame.time.delay(LOSE_DELAY)
        else:
            ball.y = leftPaddle.y - 2 * BALL_RADIUS
            speed_y = -speed_y
            playerTurn = not playerTurn
            if not muted:
                LEFT_SOUND.play()
    elif rightPaddle.rect.colliderect(ball.rect):
        if playerTurn == RIGHT_PLAYER:
            if not muted:
                FAIL_SOUND.play()
                pygame.time.delay(LOSE_DELAY)
            playerTurn = score()
        else:
            ball.y = rightPaddle.y - 2 * BALL_RADIUS
            speed_y = -speed_y
            playerTurn = not playerTurn
            if not muted:
                RIGHT_SOUND.play()
    if leftPaddle.rect.colliderect(rightPaddle):
        if leftPaddle.rect.bottom >= rightPaddle.rect.top:
            leftPaddle.move(0, -BUDGE)
            rightPaddle.move(0, BUDGE)
        elif rightPaddle.rect.bottom >= leftPaddle.rect.top:
            rightPaddle.move(0, -BUDGE)
            leftPaddle.move(0, BUDGE)
        elif leftPaddle.rect.right >= rightPaddle.rect.left:
            leftPaddle.move(-BUDGE, 0)
            rightPaddle.move(BUDGE, 0)
        elif rightPaddle.rect.right >= leftPaddle.rect.left:
            rightPaddle.move(-BUDGE, 0)
            leftPaddle.move(BUDGE, 0)

    ##
    # Draw paddles and ball
    #
    spriteGroup.draw(screen)
    spriteGroup.update()

    ##
    # Tick-tock
    #
    pygame.display.update()
    clock.tick(FRAME_RATE)

pygame.quit()
