from settings import *
from math import atan2, degrees

## Ground objects / Floor
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

## Objects that player can collide with
class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        
## I don't really get it // Need to check it        
class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        ## Player connection
        self.player = player
        self.distance = 140
        self.player_direction = pygame.Vector2(1,0)
        
        #sprite setup
        super().__init__(groups)
        self.gun_surf = pygame.image.load(join("Vampire survivor", "images", "gun", "gun.png")).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)
        
    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.player_direction = (mouse_pos - player_pos).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

        
    
    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance
        
## I don't really get it // Need to check it          
class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000
        
        self.direction = direction
        self.speed = 1200
        
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
    
class Enemies(pygame.sprite.Sprite):
    def __init__(self, pos, frames, player, groups, collision_sprites):
        super().__init__(groups)
        self.player = player
        
        #image
        self.frames, self.frames_index = frames, 0
        self.image = self.frames[self.frames_index]
        self.animation_speed = 6
        self.speed = 300
        
        ## Timer
        self.death_time = 0
        self.death_duration = 400
        
        ## Rect
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        ## Converting to Vector2 for easier math
        self.direction = pygame.Vector2()
        
        
 
    ## Enemies following player    
    def move(self, dt):
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()
        
        # Movement of enemies. 
        ## It's moving hitbox first and checking for collision
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')

        ## Hitbox position = acutall rect
        self.rect.center = self.hitbox_rect.center         

    ## Checking collision with sprites in CollisionSprites group.
    ## If collided, drawing player outside the colission, from the side he collided
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                ## Checking if players is in another Sprite rectangle.
                ## If that's the case, move player accordingly of the collision direction
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom


    def destroy(self):
        self.death_time = pygame.time.get_ticks()
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        self.image = surf
        surf.set_colorkey("black")
        
        
    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()
            

    ## Animations + updates
    def update(self, dt):
        if self.death_time == 0:
            self.frames_index += self.animation_speed * dt    
            self.image = self.frames[int(self.frames_index) % len(self.frames)] 
            self.move(dt)
        else:
            self.death_timer()
    
    ## SO MUCH CODE. I COULD JUST USE .normalize()
    
    # def move(self, dt):
    #     player_pos = pygame.Vector2(self.player.rect.center)
    #     enemy_pos = pygame.Vector2(self.rect.center)
    #     if self.rect.center != player_pos:
        
    #         ## Calculating distance to the player, then converting it to pixel movement
    #         ## It's like player input, enemies are choosing direction to go [0, -1, 1 for x and y]
    #         distance = player_pos - enemy_pos
    #         self.direction.x = 1 if distance.x > 0 else (-1 if distance.x < 0 else 0)
    #         self.direction.y = 1 if distance.y > 0 else (-1 if distance.y < 0 else 0)
    #         self.direction = self.direction.normalize() if self.direction.length() > 0 else self.direction
            
    #         ## Movement of enemies. 
    #         ## It's moving hitbox first and checking for collision
    #         self.hitbox_rect.x += self.direction.x * self.speed * dt
    #         self.collision('horizontal')
    #         self.hitbox_rect.y += self.direction.y * self.speed * dt
    #         self.collision('vertical')
   
    #         ## Hitbox position = acutall rect
    #         self.rect.center = self.hitbox_rect.center
            
                        

    
 