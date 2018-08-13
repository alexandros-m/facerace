import cv2
import pygame
import random
import time

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
displayWidth = 400
displayHeight = 400
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
clock = pygame.time.Clock()
pygame.display.set_caption('Face Race')

black=(0,0,0)
white=(255,255,255)
darkGrey = (38, 39, 40)
grey = (130, 130, 130)
red = (255,0,0)
green = (0,255,0)
lightBlue = (85, 149, 252)

closeBoolean = False

enemiesY = 0


class Sprite(object):
    def __init__(self, image):
        self.image = image
    def display(self,x,y):
        self.x = x
        self.y = y
        dimensions = self.image.get_rect().size
        self.w = dimensions[0]
        self.h = dimensions[1]
        self.rect = pygame.Rect(x,y,self.w,self.h)
        gameDisplay.blit(self.image,(x,y))

def textobjects(txt, font, color):
    textsurface = font.render(txt, True, color)
    return textsurface, textsurface.get_rect()

def textOrButton(txt,x,y,w,h,ic,ac,tc,font='Consolas',fontSize=50,bold=True,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay,ac,(x,y,w,h))
        if click[0] ==1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))
    smalltext = pygame.font.SysFont(font,fontSize,bold)
    textsurf, textrect = textobjects(txt, smalltext, tc)
    textrect.center = ((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textsurf, textrect)

def generateEnemies():
    firstRandomX = random.randint(0, displayWidth-60)
    secondRandomX = random.randint(0, displayWidth-60)
    firstRect = pygame.Rect(firstRandomX, 0, 60, 60)
    secondRect = pygame.Rect(secondRandomX, 0, 60, 60)
    while bool(firstRect.colliderect(secondRect)):
        secondRandomX = random.randint(0, displayWidth-60)
        secondRect = pygame.Rect(secondRandomX, 0, 60, 60)
    return (firstRandomX, secondRandomX)

def detectFaces():
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    objects = faceCascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in objects:
        return (x,y,w,h,img)

def close():
    pygame.quit()
    cap.release()
    cv2.destroyAllWindows()
    exit()

def calcCarPosition(aTup):
    faceX = aTup[0]
    carX = displayWidth - faceX
    return carX

def play():
    global enemiesY
    carX = displayWidth / 2
    enemiesTup = generateEnemies()
    enemySpeed = 4
    score = 0

    while not closeBoolean:
        gameDisplay.fill(grey)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
        

        if enemiesY > displayHeight:
            enemiesTup = generateEnemies()
            enemiesY = 0
            enemySpeed += 1.5
            score += 1
    
        textOrButton('Score: '+str(score), -18, -12, 100, 50, grey,
        grey, black, fontSize=15)

        enemiesY += enemySpeed
        
        faceTup = detectFaces()

        if faceTup != None:
            carX = calcCarPosition(faceTup)
            webcamView = faceTup[4]
            faceX = faceTup[0]
            faceY = faceTup[1]
            faceW = faceTup[2]
            faceH = faceTup[3]
            cv2.rectangle(webcamView, (faceX,faceY), (faceX+faceW,faceY+faceH), (0,255,0), 2)
            cv2.imshow('Computer view', webcamView)
        else:
            ret, webcamView = cap.read()
            cv2.imshow('Computer view', webcamView)

        pygame.draw.rect(gameDisplay, green, (carX,displayHeight-60,60,60))
        pygame.draw.rect(gameDisplay, red, (enemiesTup[0],enemiesY,60,60))
        pygame.draw.rect(gameDisplay, red, (enemiesTup[1],enemiesY,60,60))

        carRect = pygame.Rect(carX,displayHeight-60,60,60)
        firstEnemyRect = pygame.Rect(enemiesTup[0],enemiesY,60,60)
        secondEnemyRect = pygame.Rect(enemiesTup[1],enemiesY,60,60)

        if bool(carRect.colliderect(firstEnemyRect) or carRect.colliderect(secondEnemyRect)):
            enemiesY = 0
            gameDisplay.fill(grey)
            textOrButton('Score:'+str(score), displayWidth/2-150, 0, 300, 150, grey,
            grey, red)
            pygame.display.update()
            time.sleep(1)
            return

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    while True:
        try:
            play()
        except KeyboardInterrupt:
            close()