import pygame
import time
import random

pygame.init()

# breidd og hæð á glugga
display_width = 800 #breidd á glugga
display_height = 600 #hæð á glugga

#litir
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

# Bolta stærð
ball_size = 8
#litur á kubbum
block_color = (53,115,255)

# breidd á geimskipi
spaceship_width = 64 #breidd á bíl

#búa til glugga
win = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Lokaverkefni") #heiti glugga
clock = pygame.time.Clock()

# geimvera
tie_fighter = pygame.image.load("enemy.png")#.convert()
#geimvera.set_colorkey(white)

# loftsteinn
loftsteinn = pygame.image.load("meteor.png")

# mynd af geimskipi
spaceshipImg = pygame.image.load('space.png') #mynd af bíl

# Sprening
explode = pygame.image.load('explode.png')

# Bakgrunnur
bg = pygame.image.load("bg.jpg")

# fall sem teiknar bolta á skjáinn
def skjota(x,y):
    pygame.draw.circle(win, red, (int(x),int(y)),6,0)

#teikna kubba
def meteor(meteorx, meteory, meteorw, meteorh, color):
    #pygame.draw.rect(win, color, [meteorx, meteory, meteorw, meteorh])
    win.blit(loftsteinn, [meteor_startx, meteor_starty])

#teikna bíl
def spaceship(x,y):
    win.blit(spaceshipImg,(x,y))

#teikna stafi
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#fall til þess að hætta
def haetta(t):
    text = font.render(t, True, white)
    text_rect = text.get_rect()
    text_x = win.get_width() / 2 - text_rect.width / 2
    text_y = win.get_height() / 2 - text_rect.height / 2
    win.blit(text, [text_x, text_y])
    pygame.display.flip()
    time.sleep(5)
    quit()

# Breytur
done = False
skot = False
nytt = True
stig = 0

# byrjunarhnit bolta
ball_x = -50
ball_y = 700

# Leturgerðin sem við notum og stærðin er 36
font = pygame.font.Font(None, 36)

enemyhnitx = []
enemyhnity = []

# Enemy byrjunar y hnit
ey = 25

# Skothljóð
skothljod = pygame.mixer.Sound('sfx.wav')

# Sprengihljod
sprengihljod = pygame.mixer.Sound('sfx2.wav')

# Fly by hljóð
flyby = pygame.mixer.Sound('sfx3.wav')

# býr til hnit fyrir enemies og skrifar þau í listann
for i in range(10, 790, 60): # byrjar í hniti 10 og fer up í 680 og hefur 40 á milli
    enemyhnitx.append(i) # x hnit 1 línu
    enemyhnitx.append(i) # x hnit 2 línu
    enemyhnity.append(ey) # y hnit 1 línu
    enemyhnity.append(ey+50) # y hnit 2 línu
    
#aðalforrit
while not done:
    x_hnit = 370
    y_hnit = 500

    x_change = 0 #hraði bíls

    ball_change_x = 3
    ball_change_y = -3

    ball_x = x_hnit + 30
    ball_y = 450

    #upphafshnit
    meteor_startx = random.randrange(0, display_width-100)
    meteor_starty = -600
    meteor_speed = 4
    meteor_width = 100
    meteor_height = 100

    thingCount = 1

    dodged = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_SPACE:
                    skot = True
                    skothljod.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        # Logic
        x_hnit += x_change
        ball_y += ball_change_y

        # Birta bakgrunn
        win.blit(bg, (0,0))
        # Birta lofstein
        meteor(meteor_startx, meteor_starty, meteor_width, meteor_height, block_color)
        meteor_starty += meteor_speed
        # Birta geimflaug
        spaceship(x_hnit,y_hnit)
         
        # ef skot er True
        if skot == True:
            if nytt: # ef nýtt er True
                ball_x=x_hnit+30 # skilgreina ball_x
                ball_y=y_hnit+30 # skilgreina ball_y
            skjota (ball_x,ball_y) # kalla í skjóta fallið og birta
            ball_y-=5 # skilgreina ball_x 
            nytt=False # breyta nytt í false

        # Teikna enemies
        for i in range(0,len(enemyhnitx)):
            #pygame.draw.rect(win,red,(enemyhnitx[i],enemyhnity[i],22,50)) #teiknar kassa
            win.blit(tie_fighter, [enemyhnitx[i], enemyhnity[i]])
            enemyhnity[i]=enemyhnity[i]+0.5
            
        # athugar hvort boltinn hittir geimveru
        for i in range (0,len(enemyhnitx)): # framkvæmir jafn oft og listinn enemyhnitx er langur
            if not len(enemyhnitx)==i: #Athugar hvort að' hann er kominn út á enda og þá fer hún ekki lengra
                # athugar hvort skotið hafi hitt tie fighter
                if enemyhnity[i]<ball_y and (enemyhnity[i])+50>ball_y and enemyhnitx[i]<ball_x + 15 and (enemyhnitx[i])+50>ball_x:
                    del enemyhnitx[i] # eyðir x hniti tie fighter sem var hitt
                    del enemyhnity[i] # eyðir y hniti tie fighter sem var hitt
                    stig+=1 # hækkar stig um 1 þar sem tie fighter hefur verið hitt
                    skot = False
                    nytt = True
                    ball_x = -100
                    ball_y = 800
                    
        # athugar hvort að botlinn hittir lofstein
        if ball_y < meteor_starty+meteor_height:
            if ball_x > meteor_startx and ball_x < meteor_startx + meteor_width or ball_x+ball_size > meteor_startx and ball_x + ball_size < meteor_startx+meteor_width:
                sprengihljod.play()
                win.blit(explode, (meteor_startx,meteor_starty))
                meteor_starty = 0 - meteor_height
                meteor_startx = random.randrange(0,display_width)
                meteor_speed -= 0.1
                skot = False
                nytt = True

        # ef að lofsteinn fer af skjánum
        if meteor_starty > display_height:
            meteor_starty = 0 - meteor_height
            meteor_startx = random.randrange(0,display_width)
            meteor_speed += 0.1

        # ef að spilari hittir lofstein
        if y_hnit < meteor_starty+100:
            if x_hnit > meteor_startx and x_hnit < meteor_startx + meteor_width or x_hnit+spaceship_width > meteor_startx and x_hnit + spaceship_width < meteor_startx+meteor_width:
                haetta("Game Over")

        # athugar hvort geimflaugin hittir tie fighter
        for i in range (0,len(enemyhnitx)): # framkvæmir jafn oft og listinn enemyhnitx er langur
            if not len(enemyhnitx)==i: #Athugar hvort að' hann er kominn út á enda og þá fer hún ekki lengra
                # athugar hvort skotið hafi hitt tie fighter
                if enemyhnity[i]<y_hnit and (enemyhnity[i])+35>y_hnit and enemyhnitx[i]<x_hnit + 15 and (enemyhnitx[i])+35>x_hnit:
                    haetta("Game Over")
                    pygame.display.flip()

        # Búa til fleiri geimverur ef að hinar fara af skjánum    
        if enemyhnity[-1] >= 400:
            flyby.play()
            # býr til hnit fyrir enemies og skrifar þau í listann
            for i in range(10, 790, 60): # byrjar í hniti 10 og fer up í 680 og hefur 40 á milli
                enemyhnitx.append(i) # x hnit 1 línu
                enemyhnitx.append(i) # x hnit 2 línu
                enemyhnity.append(ey) # y hnit 1 línu
                enemyhnity.append(ey-80) # y hnit 2 línu

        # ef að skotið fer af skjánum
        if ball_y < 0:
            skot = False
            nytt = True

        # ef að stig eru orðin 100 eða meira
        if stig >= 100:
            haetta("Þú vannst!")
        
        # texti
        text = font.render("STIG", True, white)
        text2 = font.render(str(stig), True, white)
        text_rect = text.get_rect()
        text_rect = text2.get_rect()

        # birta textan
        win.blit(text, [670, 10])
        win.blit(text2, [750, 10])

        # uppfæra skjáinn
        pygame.display.update()
        clock.tick(60)
        
pygame.quit()
quit()
