import pygame
import random
import math

from pygame import mixer


#Screen
pygame.init()
screen=pygame.display.set_mode((800,600))

#Background
background=pygame.image.load('back.png')
backgroundmusic=mixer.Sound('background.wav')
backgroundmusic.play(-1)


#Title and Icon
pygame.display.set_caption('Uzay Yolu')
icon=pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#Score
scorevalue=0
font=pygame.font.SysFont('freesansbold.tff',32)
textX=10
textY=10
def showscore(x,y):
    score=font.render("Score:" + str(scorevalue), True, (255,255,255))
    screen.blit(score, (x,y))


#Gameover
overtext=pygame.font.SysFont('freesansbold.tff',64)
def gameover():
    gameovertext=overtext.render('GAME OVER', True, (255,255,255))
    screen.blit(gameovertext, (270,250))

#Bullet
bulletimg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletXchange=0
bulletYchange=0.5
bulletstate='ready'

score=0

def firebullet(x,y):
    global bulletstate
    bulletstate='fire'
    screen.blit(bulletimg,(x+16,y+10))

def collision(enemyX,enemyY,bulletX,bulletY):
    distance= math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance<40:
        return  True
    else:
        return  False

#Player
playerimg=pygame.image.load('player.png')
playerX=370
playerY=480
playerXchange=0
def player(x,y):
    screen.blit(playerimg,(x,y))
#Enemy
enemyimg=[]
enemyX=[]
enemyY=[]
enemyXchange=[]
enemyYchange=[]
numofenemies=6

for i in range(numofenemies):



 enemyimg.append(pygame.image.load('enemy.png'))
 enemyX.append(random.randint(0,736))
 enemyY.append(random.randint(50,150))
 enemyXchange.append(0.3)
 enemyYchange.append(60)


def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

#Game Loop
running=True
while running:
    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            running= False
        if event.type== pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerXchange=-0.4

            if event.key==pygame.K_RIGHT:
                playerXchange = 0.4

            if event.key==pygame.K_SPACE:
               if bulletstate=='ready':
                bulletsound=mixer.Sound('laser.wav')
                bulletsound.play()
                bulletX=playerX
                firebullet(bulletX,bulletY)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_RIGHT or event.key== pygame.K_LEFT:
                playerXchange = 0


    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for i in range(numofenemies):
     if enemyY[i] > 440:
        for j in range(numofenemies):
            enemyY[j] = 2000
        gameover()
        break

     enemyX[i]+=enemyXchange[i]
     if scorevalue<5:
      if enemyX[i]>736:
        enemyXchange[i]=-0.1
        enemyY[i]+=enemyYchange[i]
      elif enemyX[i]<0:
        enemyXchange[i]=0.1
        enemyY[i] += enemyYchange[i]
     elif scorevalue>=5 and scorevalue<15:
         if enemyX[i] > 736:
             enemyXchange[i] = -0.3
             enemyY[i] += enemyYchange[i]
         elif enemyX[i] < 0:
             enemyXchange[i] = 0.3
             enemyY[i] += enemyYchange[i]
     else:
         if enemyX[i] > 736:
             enemyXchange[i] = -0.6
             enemyY[i] += enemyYchange[i]
         elif enemyX[i] < 0:
             enemyXchange[i] = 0.6
             enemyY[i] += enemyYchange[i]


     col = collision(enemyX[i], enemyY[i], bulletX, bulletY)
     if col:
         explosound = mixer.Sound('explosion.wav')
         explosound.play()
         bulletY = 500
         bulletX = 0
         bulletstate = 'ready'
         scorevalue += 1
         enemyX[i] = random.randint(0, 736)
         enemyY[i] = random.randint(50, 150)
     enemy(enemyX[i], enemyY[i], i)

    playerX+=playerXchange
    if playerX>736:
        playerX=736
    elif playerX<0:
        playerX=0
    player(playerX,playerY)


    if bulletY<=0:
        bulletstate='ready'
        bulletY=480

    if bulletstate=='fire':
        firebullet(bulletX,bulletY)
        bulletY-=bulletYchange


    showscore(textX,textY)

    pygame.display.update()