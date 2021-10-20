import cv2
import pygame as pg
from pygame.locals import *
from pygame import *
import random as rd
from pygame.math import Vector2
import numpy as np

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.cap.set(3,900) #szerokosc
        self.cap.set(4,900) #wysokosc
        self.cap.set(10,100) #jasnosc
        self.x = self.y = self.h = 0

    def camera_read(self):
        success, img = self.cap.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray,1.2,4)
        # cv2.line(img,(0,100),(1000,100),(255,0,0),5)
        # cv2.line(img,(0,450),(1000,450),(255,0,0),5)
        # cv2.line(img,(860,550),(960,550),(255,0,0),5)
        # cv2.line(img,(0,550),(100,550),(255,0,0),5)
        for (x,y,w,h) in faces:
            cv2.circle(img,(round(x+.5*h),round(y+.5*h)),5,(0,0,255),10)
            self.x=x
            self.y=y
            self.h=h
        cv2.imshow("Video",img)
        if cv2.waitKey(1) & 0xFF== ord('q'):
            self.cap.release()
        

class Snake:
    def __init__(self,name,parent_screen,blocc,blockmenu) -> None:
        self.game_over = False
        self.parent_screen = parent_screen
        self.name = name
        self.block = blocc
        self.blockmenu = blockmenu
        self.snakeimage = pg.image.load("snake-graphics.png").convert()
        self.snakeimage = pg.transform.scale(self.snakeimage,(250,200))

        self.snakehead_right = self.snakeimage.subsurface((200,0,50,50))
        self.snakehead_up = self.snakeimage.subsurface((150,0,50,50))
        self.snakehead_down = self.snakeimage.subsurface((200,50,50,50))
        self.snakehead_left = self.snakeimage.subsurface((150,50,50,50))

        self.apple_texture = self.snakeimage.subsurface((0,150,50,50))

        self.snaketail_right = self.snakeimage.subsurface((200,100,50,50))
        self.snaketail_up = self.snakeimage.subsurface((150,100,50,50))
        self.snaketail_down = self.snakeimage.subsurface((200,150,50,50))
        self.snaketail_left = self.snakeimage.subsurface((150,150,50,50))

        self.snakebody_horizontal = self.snakeimage.subsurface((50,0,50,50))
        self.snakebody_vertical = self.snakeimage.subsurface((100,50,50,50))

        self.snakecorner_up_right = self.snakeimage.subsurface((0,50,50,50))
        self.snakecorner_up_left = self.snakeimage.subsurface((100,100,50,50))
        self.snakecorner_down_left = self.snakeimage.subsurface((100,0,50,50))
        self.snakecorner_down_right = self.snakeimage.subsurface((0,0,50,50))
        self.score = 0
        self.speed = 6
        self.length = 1
        self.body = [Vector2(350,450),Vector2(400,450),Vector2(450,450),Vector2(450,450)]
        self.direction = Vector2(-50,0)
        self.apple = Vector2(rd.randint(1,16)*50,rd.randint(1,16)*50)
        self.new_block = False
        while(self.body[0][0]==self.apple.x and self.body[0][1]==self.apple.y):#??????????
                self.apple.x = rd.randint(1,16)*50
                self.apple.y = rd.randint(1,16)*50
        self.font_style = pg.font.SysFont(None,60)

    def message(self,t_message,color,x,y) -> None:
        mesg = self.font_style.render(t_message,True,color)
        self.parent_screen.blit(mesg,(x,y))



    def draw(self) -> None:
        self.parent_screen.fill((0,0,0))
        for x in range(0,900,50):
            self.parent_screen.blit(self.block,(x,0))
            self.parent_screen.blit(self.block,(x,850))
            self.parent_screen.blit(self.block,(0,x))
            self.parent_screen.blit(self.block,(850,x))
            self.parent_screen.blit(self.blockmenu,(0,900))
        self.parent_screen.blit(self.snakeimage,(self.apple.x,self.apple.y),(0,150,50,50))
        self.draw_snake()
        self.message("Your score: {score}".format(score = self.score),(255,0,255),330,930)
        if(self.check_walls_collision() or self.check_snake_collision()):
                self.message("YOU LOST!","red",480,430)
                self.direction = Vector2(0,0)
                self.game_over = True
        pg.display.update()

    def apple_eaten(self) -> None:
        if(self.body[0][0]==self.apple.x and self.body[0][1]==self.apple.y):
            self.score+=10
            for block in self.body:
                while(block.x==self.apple.x and block.y==self.apple.y):
                    self.apple.x = rd.randint(1,16)*50
                    self.apple.y = rd.randint(1,16)*50
            self.length+=1
            self.new_block = True
    
    def check_walls_collision(self) -> bool:
        if(self.body[0].x>800 or self.body[0].x<50 or self.body[0].x<50 or self.body[0].x>800):
            return True
        else:
            return False

    def check_snake_collision(self) -> bool:
        for block in self.body[2:]:
            if block.x == self.body[0].x and block.y == self.body[0].y:
                return True
        return False

    def draw_snake(self) -> None:
        for index,vect in enumerate(self.body):
            if index == 0:
                self.update_head_graphics(index,vect)
            elif index == self.length+1:
                self.update_tail_graphics(index,vect)
            elif index > 0 and index < self.length+1:
                next_block = self.body[index + 1] - vect
                previous_block = self.body[index - 1] - vect
                if previous_block.x == next_block.x:
                    self.parent_screen.blit(self.snakebody_vertical,(vect.x,vect.y),((0,0,50,50)))
                elif previous_block.y == next_block.y:
                    self.parent_screen.blit(self.snakebody_horizontal,(vect.x,vect.y),((0,0,50,50)))
                else:
                    if previous_block.x == -50 and next_block.y == -50 or previous_block.y == -50 and next_block.x == -50:
                        self.parent_screen.blit(self.snakecorner_up_left,(vect.x,vect.y),((0,0,50,50)))
                    elif previous_block.x == 50 and next_block.y == -50 or previous_block.y == -50 and next_block.x == 50:
                        self.parent_screen.blit(self.snakecorner_up_right,(vect.x,vect.y),((0,0,50,50)))
                    elif previous_block.x == 50 and next_block.y == 50 or previous_block.y == 50 and next_block.x == 50:
                        self.parent_screen.blit(self.snakecorner_down_right,(vect.x,vect.y),((0,0,50,50)))
                    elif previous_block.x == -50 and next_block.y == 50 or previous_block.y == 50 and next_block.x == -50:
                        self.parent_screen.blit(self.snakecorner_down_left,(vect.x,vect.y),((0,0,50,50)))



    def update_head_graphics(self,index,vector):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(50,0): self.parent_screen.blit(self.snakehead_left,(vector[0],vector[1]),((0,0,50,50)))
        elif head_relation == Vector2(-50,0): self.parent_screen.blit(self.snakehead_right,(vector[0],vector[1]),((0,0,50,50)))
        elif head_relation == Vector2(0,50): self.parent_screen.blit(self.snakehead_up,(vector[0],vector[1]),((0,0,50,50)))
        elif head_relation == Vector2(0,-50): self.parent_screen.blit(self.snakehead_down,(vector[0],vector[1]),((0,0,50,50)))

    def update_tail_graphics(self,index,vector):
        tail_relation = self.body[self.length+1] - self.body[self.length]
        if tail_relation == Vector2(50,0): self.parent_screen.blit(self.snaketail_left,(vector[0],vector[1]),((0,0,50,50)))
        elif tail_relation == Vector2(-50,0): self.parent_screen.blit(self.snaketail_right,(vector[0],vector[1]),((0,0,50,50)))
        elif tail_relation == Vector2(0,50): self.parent_screen.blit(self.snaketail_up,(vector[0],vector[1]),((0,0,50,50)))
        elif tail_relation == Vector2(0,-50): self.parent_screen.blit(self.snaketail_down,(vector[0],vector[1]),((0,0,50,50)))

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]


class Game:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((900,1000))
        self.screen.fill((0,0,0))
        self.block = pg.image.load("square.jpg").convert()
        self.block = pg.transform.scale(self.block,(50,50))
        self.blockmenu = pg.transform.scale(self.block,(900,100))
        self.snake = Snake("Rudolf",self.screen,self.block,self.blockmenu)
        self.camera = Camera()
        clock = pg.time.Clock()
        pg.display.set_caption("Head-Snache")
        self.snake.draw()
        self.running = True
        self.snake.direction = Vector2(0,0)
        while self.running:
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    if self.snake.game_over != True:
                        if event.key == K_DOWN or self.camera.y + round(.5*self.camera.h)>= 350:
                            if self.snake.direction != Vector2(0,-50):
                                self.snake.direction = Vector2(0,50)
                        elif event.key == K_UP or self.camera.y  + round(.5*self.camera.h) <= 300:
                            if self.snake.direction != Vector2(0,50):
                                self.snake.direction = Vector2(0,-50)
                        elif event.key == K_LEFT or self.camera.x  + round(.5*self.camera.h) <= 400:
                            if self.snake.direction != Vector2(50,0):
                                self.snake.direction = Vector2(-50,0)
                        elif event.key == K_RIGHT or self.camera.x  + round(.5*self.camera.h) >= 560:
                            if self.snake.direction != Vector2(-50,0) and self.snake.direction != Vector2(0,0):
                                self.snake.direction = Vector2(50,0)
                    if event.key == K_ESCAPE:
                        self.running = False
                    if event.key == K_r:
                        del self.snake
                        self.snake = Snake("Rudolf",self.screen,self.block,self.blockmenu)
                        self.snake.direction = Vector2(0,0)
                if event.type == QUIT:
                    self.running = False
            if self.snake.direction != Vector2(0,0):   
                self.snake.move_snake()
            self.camera.camera_read()
            self.snake.apple_eaten()
            self.snake.draw()
            clock.tick(self.snake.speed)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    game = Game()