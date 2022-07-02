import pygame
import sys
import random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0 , 0)
        self.new_block = False

        self.head_up = pygame.image.load('snake_game/graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('snake_game/graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('snake_game/graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('snake_game/graphics/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('snake_game/graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('snake_game/graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('snake_game/graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('snake_game/graphics/tail_left.png').convert_alpha()
        
        self.body_vertical = pygame.image.load('snake_game/graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('snake_game/graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('snake_game/graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('snake_game/graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('snake_game/graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('snake_game/graphics/body_bl.png').convert_alpha()
        
        self.crunch_sound = pygame.mixer.Sound('snake_game/sound/Sound_crunch.wav')
        self.crash_sound = pygame.mixer.Sound('snake_game/sound/1_snake_game_resources_ding.mp3')
        self.bg_sound = pygame.mixer.Sound('snake_game/sound/bg_music_1.mp3')

    def draw_snake(self): 
        self.update_head_graphics()
        self.update_tail_graphics()
        # to draw a snake ---> 1)create a rect 2)draw the rect
        for index,block in enumerate(self.body):
            x_pos1 = (block.x * cellsize)
            y_pos1 = (block.y * cellsize)
            block_rect = pygame.Rect(x_pos1 , y_pos1 , cellsize , cellsize)            
        # what direction is the face heading
            if index == 0:  
                screen.blit(self.head , block_rect)
            elif index == (len(self.body) - 1):
                screen.blit(self.tail , block_rect)
            else :
                previous = self.body[index + 1] - block
                next = self.body[index - 1] - block
                if previous.x == next.x :
                    screen.blit(self.body_vertical , block_rect)
                elif previous.y == next.y :
                    screen.blit(self.body_horizontal , block_rect)
                else:
                    if previous.x == -1 and next.y == -1 or next.x == -1 and previous.y == -1:
                        screen.blit(self.body_tl , block_rect)
                    elif previous.x == -1 and next.y == 1 or next.x == -1 and previous.y == 1:
                        screen.blit(self.body_bl , block_rect)
                    elif previous.x == 1 and next.y == -1 or next.x == 1 and previous.y == -1:
                        screen.blit(self.body_tr , block_rect)
                    elif previous.x == 1 and next.y == 1 or next.x == 1 and previous.y == 1:
                        screen.blit(self.body_br , block_rect)
            
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1 , 0): self.head = self.head_left
        elif head_relation == Vector2(-1 , 0): self.head = self.head_right
        elif head_relation == Vector2(0 , 1): self.head = self.head_up
        elif head_relation == Vector2(0 , -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down
        
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0 , body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[ : -1]
            body_copy.insert(0 , body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0 , 0)
    
    def play_sound(self):
        self.crunch_sound.play()

    def play_crash(self):
        self.crash_sound.play()

    def bg(self):
        self.bg_sound.play()    

class FRUIT:
    def __init__(self):
        self.randomize()
        # position of fruit
#         self.x = random.randint(0 , cellnumber - 1)
#         self.y = random.randint(0 , cellnumber - 1)
# self.pos=pygame.math.Vector2(self.x,self.y)--> we have imported vector2 so that we dont have to write pygame.math everytime
#         self.pos = Vector2(self.x,self.y)

    def draw_fruit(self):
        # to draw a fruit ---> 1)create a rect 2)draw the rect
        x_pos2 = (self.pos.x * cellsize)
        y_pos2 = (self.pos.y * cellsize)
        fruit_rect = pygame.Rect(x_pos2 , y_pos2 , cellsize , cellsize)
        screen.blit(apple , fruit_rect)
        # pygame.draw.rect(screen , (0,0,255) , fruit_rect)

    def randomize(self):
        self.x = random.randint(0 , cellnumber - 1)
        self.y = random.randint(0 , cellnumber - 1)
        self.pos = Vector2(self.x,self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.snake.bg()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
        # 1)reposition the fruit 2)add another block to the snake
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_sound()

# to prevent fruit to be on the snake body
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        # 1) snake outside the screen 2) snake hits itself
        if not 0 <= (self.snake.body[0].x) < cellnumber or not 0 <= (self.snake.body[0].y) < cellnumber:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
 
    def game_over(self):
        self.snake.play_crash()
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167,209,61)

        for row in range(cellnumber):
            if row % 2 == 0:
                for col in range(cellnumber):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cellsize , row*cellsize , cellsize , cellsize)
                        pygame.draw.rect(screen , grass_color , grass_rect) 
            else:
                for col in range(cellnumber):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*cellsize , row*cellsize , cellsize , cellsize)
                        pygame.draw.rect(screen , grass_color , grass_rect) 

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, False , (0,0,0))
        score_x = int(cellsize*cellnumber - 40)
        score_y = int(cellsize*cellnumber - 40)
        score_rect = score_surface.get_rect(center = (score_x , score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left , apple_rect.top , (apple_rect.width + score_rect.width+6) , apple_rect.height)

        pygame.draw.rect(screen , (167,209,61) , bg_rect)
        screen.blit(score_surface , score_rect)
        screen.blit(apple , apple_rect)
        pygame.draw.rect(screen , (0,0,0) , bg_rect , 2)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.display.set_caption("MasterofDeath's Snake And Apple Game")
pygame.init()
cellsize = 40
cellnumber = 20
screen = pygame.display.set_mode(((cellsize*cellnumber),(cellsize*cellnumber)))
clock = pygame.time.Clock()
apple = pygame.image.load("snake_game/graphics/apple.png").convert_alpha()
game_font = pygame.font.Font('snake_game/font/PoetsenOne-Regular.ttf' , 20)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE , 150)

main_game = MAIN()

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0 , -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0 , 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1 , 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1 , 0)

    screen.fill((175,215,70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)