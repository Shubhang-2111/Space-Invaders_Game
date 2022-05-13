import random
import math
import pygame
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
running = True
pygame.display.set_caption("SpaceBattle")
gameIcon = pygame.image.load("spaceship.png")
pygame.display.set_icon(gameIcon)
playerImg = pygame.image.load("r.png")
background = pygame.image.load("5512626.jpg")
playerX = 370
playerY = 480
playerChangeX = 0

enemyImg = []
enemyX = []
enemyY = []
enemyChangeX = []
enemyChangeY = []
number = 7
for i in range(7):
    enemyImg.append(pygame.image.load("space-invaders.png"))
    enemyX.append(random.randint(30, 530))
    enemyY.append(random.randint(30, 200))
    enemyChangeX.append(-0.4)
    enemyChangeY.append(0)

bulletImg = pygame.image.load("bullet.png")
bulletX = 370
bulletY = 465
bulletChangeY = -1.5
bullet_state = "ready"
score = 0
font = pygame.font.Font('LuckyBoss.ttf', 32)
textX = 10
textY = 10
font_over = pygame.font.Font("LuckyBoss.ttf", 64)
# Background music
mixer.music.load("Blazer Rail.wav")
mixer.music.play(-1)


def enemy(x1, y1, j):
    screen.blit(enemyImg[j], (x1, y1))


def player(x, y):
    screen.blit(playerImg, (x, y))


def bullet(x, y):
    screen.blit(bulletImg, (x + 15, y + 30))
    global bullet_state
    bullet_state = "fired"


def isCollide(bX, bY, eX, eY):
    distance = math.sqrt(math.pow(bX - eX, 2) + math.pow(bY - eY, 2))
    if distance < 27:
        return True
    else:
        return False


def scores(tX, tY):
    s = font.render("Score is " + str(score), True, (255, 255, 255))
    screen.blit(s, (tX, tY))


def gameover():
    g = font_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(g, (300, 250))


while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerChangeX = 0.8
            if event.key == pygame.K_LEFT:
                playerChangeX = -0.8
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    fire_sound = mixer.Sound("shoot.wav")
                    fire_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            playerChangeX = 0

    playerX += playerChangeX
    if bulletY == enemyY and bulletX == enemyY:
        print("Collided")
    if playerX <= 0:
        playerX = 0
    elif playerX >= 720:
        playerX = 720
    for j in range(number):
        if enemyY[j] > 480:
            for i in range(6):
                enemyY[i] = 2000
                gameover()
        enemyX[j] += enemyChangeX[j]
        enemyY[j] += enemyChangeY[j]
        if enemyX[j] <= 0:
            enemyChangeX[j] = 0.2
            enemyChangeY[j] = 0.06
            enemyX[j] = 0
        elif enemyX[j] >= 720:
            enemyX[j] = 720
            enemyChangeX[j] = -0.2
        if isCollide(bulletX, bulletY, enemyX[j], enemyY[j]):
            explosion = mixer.Sound("explosion.wav")
            explosion.play()
            score += 1
            bulletY = 465
            bullet_state = "ready"
            enemyX[j] = random.randint(50, 750)
            enemyY[j] = random.randint(50, 380)
        enemy(enemyX[j], enemyY[j], j)
    if bulletY <= 0:
        bulletY = 465
        bullet_state = "ready"
    if bullet_state is "fired":
        bullet(bulletX, bulletY)
        bulletY += bulletChangeY

    player(playerX, playerY)
    scores(textX, textY)
    pygame.display.update()
