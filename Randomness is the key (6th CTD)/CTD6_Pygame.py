import pygame
import button
import time
import random
import math
from pygame.locals import *
from pygame import mixer

pygame.init()
mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bag Game!")

gameplay = 0
bagchoice = -1
numchoice = -1
pcbagchoice = -1
pcnumchoice = -1
turn = 0
bags = [10,10,10]
invalid = 0
 
font = pygame.font.SysFont("arialblack", 40)
text_color = (255,255,255)
text_color_outline = (0,89,255)
textbox_color = pygame.Color('gray15')
textactive = False
username = ""
usernamerect = pygame.Rect(250,200,300,50)

def drawtext(text, font, text_color, x, y):
    img = font.render(text,True,text_color)
    screen.blit(img, (x,y))

logoimg = pygame.image.load('logo.png').convert_alpha()
startbut = pygame.image.load('startbutton.png').convert_alpha()
exitbut = pygame.image.load('exitbutton.png').convert_alpha()
infobut = pygame.image.load('infobutton.png').convert_alpha()
enterbut = pygame.image.load('enterbutton.png').convert_alpha()
backimg = pygame.image.load('backgroundimage.png').convert()
textbg = pygame.image.load('textbg.png').convert_alpha()
bagchoose = pygame.image.load('bag choose.png').convert_alpha()
numchoose = pygame.image.load('num choose.png').convert_alpha()
userenter = pygame.image.load('name enter.png').convert_alpha()
bagimg = pygame.image.load('pouchimg.png').convert_alpha()
choice1 = pygame.image.load('choice1.png').convert_alpha()
choice2 = pygame.image.load('choice2.png').convert_alpha()
choice3 = pygame.image.load('choice3.png').convert_alpha()
choice4 = pygame.image.load('choice4.png').convert_alpha()
choice5 = pygame.image.load('choice5.png').convert_alpha()
infotext = pygame.image.load('infotext.png').convert_alpha()
backbut = pygame.image.load('backarrow.png').convert_alpha()
invalidimg = pygame.image.load('invalid move.png').convert_alpha()

start_button = button.button(200,375,startbut,1)
exit_button = button.button(300,475,exitbut,1)
info_button = button.button(400,375,infobut,1)
enter_button = button.button(300,250,enterbut,1)
backarrow = button.button(0,0,backbut,0.5)
bag1 = button.button(100,50,bagimg,1)
bag2 = button.button(300,50,bagimg,1)
bag3 = button.button(500,50,bagimg,1)
but1 = button.button(25,350,choice1,1)
but2 = button.button(175,350,choice2,1)
but3 = button.button(325,350,choice3,1)
but4 = button.button(475,350,choice4,1)
but5 = button.button(625,350,choice5,1)
invalidbut = button.button(0,250,invalidimg,2)

mixer.music.load('music.mp3')
mixer.music.play(-1)

clock = pygame.time.Clock()
FPS = 30
bg_width = backimg.get_width()
tiles = math.ceil((800 / bg_width)) + 1
scroll = 0

def playermove(bags,bagnum,choicenum,bagchoice,turn,invalid):
    if bags[bagnum] < choicenum or bags[bagnum] == 0 or bags[bagnum] - choicenum < 0:
        bagchoice = -1
        invalid = 1
        return bags,turn,bagchoice,invalid
    else:
        bags[bagnum] = bags[bagnum] - choicenum
        turn += 1
        bagchoice = -1
        invalid = 0
        return bags,turn,bagchoice,invalid

def pcplay(bags,pcbagchoice,pcnumchoice):
    bagnum = random.randint(0,2)
    choicenum = random.randint(1,5)
    if bags[bagnum] == 0:
        pcplay(bags,pcbagchoice,pcnumchoice)
    else:
        while True:
            choicenum = random.randint(1,5)
            if bags[bagnum] >= choicenum:
                bags[bagnum] = bags[bagnum] - choicenum
                return bags,bagnum,choicenum
    return bags,bagnum,choicenum

def wincondition(bags):
    if bags[0] == 0 and bags[1] == 0 and bags[2] == 0:
        return True
    return False

def restartgame(bags,turn,username):
    bags = [10,10,10]
    turn = 0
    username = ""
    return bags, turn, username

gameOn = True
while gameOn:
    clock.tick(FPS)
    
    for i in range(0,tiles):
        screen.blit(backimg,(i*bg_width + scroll,0))
    scroll -= 5

    if abs(scroll) > bg_width:
        scroll = 0

    if gameplay == 0:
        screen.blit(logoimg,(0,20))
        if start_button.draw(screen):
            print("Start")
            gameplay = 3
        elif exit_button.draw(screen):
            mixer.music.load('exitsound.mp3')
            mixer.music.play(0)
            time.sleep(2)
            gameOn = False
        elif info_button.draw(screen):
            print("Info")
            gameplay = 2
    elif gameplay == 1:
        if wincondition(bags) is False:
            if turn % 2 == 0:
                if bagchoice == -1:
                    if turn > 0:
                        if pcnumchoice == 1:
                            drawtext("PC has pulled {} ball from bag {}".format(pcnumchoice,pcbagchoice + 1),font,text_color,50,450)
                        else:
                            drawtext("PC has pulled {} balls from bag {}".format(pcnumchoice,pcbagchoice + 1),font,text_color,50,450)
                    screen.blit(bagchoose,(50,350))
                    drawtext("{}".format(bags[0]),font,text_color,165,250)
                    drawtext("{}".format(bags[1]),font,text_color,365,250)
                    drawtext("{}".format(bags[2]),font,text_color,565,250)

                    if bag1.draw(screen):
                        print("Bag1")
                        bagchoice = 0
                    elif bag2.draw(screen):
                        print("Bag2")
                        bagchoice = 1
                    elif bag3.draw(screen):
                        print("Bag3")
                        bagchoice = 2
                else:
                    screen.blit(numchoose,(50,100))
                    if but1.draw(screen):
                        print("1")
                        bags,turn,bagchoice,invalid = playermove(bags,bagchoice,1,bagchoice,turn,invalid)
                        if invalid == 1:
                            gameplay = 4
                        print(bags)
                    if but2.draw(screen):
                        print("2")
                        bags,turn,bagchoice,invalid = playermove(bags,bagchoice,2,bagchoice,turn,invalid)
                        if invalid == 1:
                            gameplay = 4
                        print(bags)
                    if but3.draw(screen):
                        print("3")
                        bags,turn,bagchoice,invalid = playermove(bags,bagchoice,3,bagchoice,turn,invalid)
                        if invalid == 1:
                            gameplay = 4
                        print(bags)
                    if but4.draw(screen):
                        print("4")
                        bags,turn,bagchoice,invalid = playermove(bags,bagchoice,4,bagchoice,turn,invalid)
                        if invalid == 1:
                            gameplay = 4
                        print(bags)
                    if but5.draw(screen):
                        print("5")
                        bags,turn,bagchoice,invalid = playermove(bags,bagchoice,5,bagchoice,turn,invalid)
                        if invalid == 1:
                            gameplay = 4
                        print(bags)
            else:
                bags, pcbagchoice, pcnumchoice = pcplay(bags,pcbagchoice,pcnumchoice)
                print(bags)
                turn += 1
        else:
            screen.blit(textbg,(0,0))
            if turn % 2 == 1:
                drawtext("{}".format(username),font,text_color,330,200)
                drawtext("Has Won!",font,text_color,300,310)
            else:
                drawtext("{}".format(username),font,text_color,330,200)
                drawtext("Has Lost :(",font,text_color,295,310)
            if backarrow.draw(screen):
                bags, turn, username = restartgame(bags,turn,username) 
                wincondition(bags)
                gameplay = 0  
    elif gameplay == 2:
        screen.blit(infotext,(0,0))
        if backarrow.draw(screen):
            bags, turn, username = restartgame(bags,turn,username) 
            wincondition(bags)
            gameplay = 0           
    elif gameplay == 3:
        if backarrow.draw(screen):
            bags, turn, username = restartgame(bags,turn,username) 
            wincondition(bags)
            gameplay = 0  
        
        screen.blit(userenter,(50,110))
        
        text_surface = font.render(username,True,text_color)
        
        if textactive:
            pygame.draw.rect(screen,text_color,usernamerect,5)
        else:
            pygame.draw.rect(screen,textbox_color,usernamerect,5)
        
        screen.blit(text_surface,(usernamerect.x + 5,usernamerect.y -8))

        usernamerect.w = max(300, text_surface.get_width() + 10)

        if enter_button.draw(screen):
            gameplay = 1

        for event in pygame.event.get():   
            if event.type == pygame.KEYDOWN:
                if textactive is True:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[0:-1]
                    else:
                        username += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if usernamerect.collidepoint(event.pos):
                    textactive = True
                else:
                    textactive = False
            elif event.type == QUIT:
                mixer.music.load('exitsound.mp3')
                mixer.music.play(0)
                time.sleep(2)
                gameOn = False
    elif gameplay == 4:
        if invalidbut.draw(screen):
            gameplay = 1
    for event in pygame.event.get():   
        if event.type == QUIT:
            mixer.music.load('exitsound.mp3')
            mixer.music.play(0)
            time.sleep(2)
            gameOn = False

    pygame.display.flip()