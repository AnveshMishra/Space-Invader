import pygame
import random
import math
from pygame import mixer

#initialize 
pygame.init()

#create screen
screen=pygame.display.set_mode((800,600))

#Title and Icon 

pygame.display.set_caption("Space Invaders")
icon=pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

#background image
background_img=pygame.image.load("background.png")

#sound
mixer.music.load("background.wav")
mixer.music.play(-1)


#player 
player_img=pygame.image.load("space-invaders.png")
player_x=370
player_y=480
player_x_change=0

#enemy
enemy_img= []
enemy_x= []
enemy_y= []
enemy_x_change= []
enemy_y_change= []
num_of_enemy=6

for i in range(num_of_enemy):
    enemy_img.append(pygame.image.load("enemy.png"))
    enemy_x.append(random.randint(0,736))
    enemy_y.append(random.randint(50,150))
    enemy_x_change.append(4)
    enemy_y_change.append(35)

#bullet
#bullet_img=pygame.image.load("bullet.png")
bullet_y_change=10
bullet_x=0
bullet_y=480
bullet_state="ready"

#Score
score_val=0
font=pygame.font.Font("freesansbold.ttf",32)
text_x=10
text_y=10

#game over text
game_over_font=pygame.font.Font("freesansbold.ttf",64)

#<---FUNCTIONS---->

def player(x,y):
    screen.blit(player_img,(x,y))

def enemy(x,y,i):
    for i in range(num_of_enemy):
        screen.blit(enemy_img[i],(x,y))

def fire_bullet(x,y):
    #bullet_state="fire"
    bullet_img=pygame.image.load("bullet.png")
    screen.blit(bullet_img,(x+16,y+8))

def check_collision(bullet_x,bullet_y,enemy_x,enemy_y):
    distance=math.sqrt(math.pow(bullet_x-enemy_x,2)+math.pow(bullet_y-enemy_y,2))
    if distance<27:
        return True
    else:
        return False

def show_score(x,y):
    score=font.render("Score: "+str(score_val),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over():
    game_over=game_over_font.render("G A M E - O V E R",True,(255,255,255))
    screen.blit(game_over,(150,250))

#Game Loop
running=True
while running:
    
    #RGB_Red_Green_BLUE
    screen.fill((0,0,0))

    screen.blit(background_img,(0,0))
    
    #<-----EVENTS----->

    for event in pygame.event.get():
        
        #<----QUIT__EVENT---->
        
        if event.type==pygame.QUIT:
            running=False
        
        #<----KEYBOARD__BINDINGS---->

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                player_x_change=-5
            if event.key==pygame.K_RIGHT:
                player_x_change=5
            if event.key==pygame.K_SPACE:
                if bullet_state=="ready":
                    fire_bullet(player_x,bullet_y)
                    bullet_x=player_x
                    bullet_state="fire"
                    bullet_sound=mixer.Sound("laser.wav")
                    bullet_sound.play()

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT:
                player_x_change=0
    
    player_x+=player_x_change

    enemy_x+=enemy_x_change
    
    if player_x<0:
        player_x=0
    elif player_x>736:
        player_x=736


    for i in range(num_of_enemy):
        if enemy_y[i]>440:
            for j in range(num_of_enemy):
                enemy_y[j]=2000
            game_over()
            break
        
        
        enemy_x[i]+=enemy_x_change[i]
        if enemy_x[i]<0:
            enemy_x_change[i]=4
            enemy_y[i]+=enemy_y_change[i]
        
        elif enemy_x[i]>736:
            enemy_x_change[i]=-4
            enemy_y[i]+=enemy_y_change[i]
        
        enemy(enemy_x[i],enemy_y[i],i)
        
        if check_collision(bullet_x,bullet_y,enemy_x[i],enemy_y[i]):
            collison_sound=mixer.Sound("explosion.wav")
            collison_sound.play()
            score_val+=1
            bullet_y=480
            bullet_state="ready"
            enemy_x[i]=random.randint(0,736)
            enemy_y[i]=random.randint(50,150)
        



    if bullet_state is "fire":
        fire_bullet(bullet_x,bullet_y)
        bullet_y-=bullet_y_change
    if bullet_y<=0:
        bullet_y=480
        bullet_state="ready"
    
    
    show_score(text_x,text_y)

    player(player_x,player_y)

    #enemy(enemy_x,enemy_y)

    pygame.display.update()