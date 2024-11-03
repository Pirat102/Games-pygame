import pygame, sys, random, time
from pygame.math import Vector2

BLOCK_SIZE = 40
CELL_NUMBER = 20
WH = BLOCK_SIZE * CELL_NUMBER


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        
        
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    
        
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        
        for i, block in enumerate(self.body):
            # We still nedd a rect for the positioning
            x_pos = int(block.x * BLOCK_SIZE)
            y_pos = int(block.y * BLOCK_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, BLOCK_SIZE, BLOCK_SIZE)
            
            # What direction is the face heading
            if i == 0:
                screen.blit(self.head, block_rect)
            elif i == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
                
            else:
                previous_block = self.body[i + 1] - block
                next_block = self.body[i - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)
                    
                
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down
        
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            
            if self.direction != [0, 0]:
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy
        
    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()      

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0, 0)

class FRUIT:
    def __init__(self):
        self.randomize_position(None)

    def randomize_position(self, snake_body):
        while True:
            self.x = random.randrange(0, CELL_NUMBER)
            self.y = random.randrange(0, CELL_NUMBER)
            self.pos = Vector2(self.x, self.y)
            if snake_body is None or self.pos not in snake_body:
                break
      
            
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * BLOCK_SIZE), int(self.pos.y * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, "red", fruit_rect)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()
        
    def check_collision(self):
        if self.snake.body[0] == self.fruit.pos:
            self.snake.add_block()
            self.fruit.randomize_position(self.snake.body)
            self.snake.play_crunch_sound()

        
    
    def check_fail(self):
        if self.snake.direction != [0, 0]:
            if not 0 <= self.snake.body[0].x < CELL_NUMBER or not 0 <= self.snake.body[0].y < CELL_NUMBER:
                self.snake.reset()

            for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    self.snake.reset()
                    
    def game_over(self):
        pygame.quit()
        sys.exit()
        
   # def draw_grid(self):
        for x in range(0, WH, BLOCK_SIZE):
            for y in range(0, WH, BLOCK_SIZE):
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, "#3c3c3b", rect, 1)
                
    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(CELL_NUMBER):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
                        
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(BLOCK_SIZE * CELL_NUMBER - 60)
        score_y = int(BLOCK_SIZE * CELL_NUMBER - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 10, apple_rect.height)
        
        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

#pygame.mixer.init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((WH, WH))
clock = pygame.time.Clock()
apple = pygame.image.load("Graphics/apple.png").convert_alpha()
game_font = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 120)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_game.game_over()
        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and main_game.snake.direction.y == 0:
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_s and main_game.snake.direction.y == 0:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_a and main_game.snake.direction.x == 0:
                main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_d and main_game.snake.direction.x == 0:
                main_game.snake.direction = Vector2(1, 0)

    screen.fill((175,215,70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60) # limits FPS to 60



