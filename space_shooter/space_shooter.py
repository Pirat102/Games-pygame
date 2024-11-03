import pygame, sys, random

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.original_surf = player_surface
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = (WIDTH / 2, HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 400
        self.rotation = [0, -90, 90, 180]
        self.rotated = False
        
        #cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
        
        
    def laser_time(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >=self.cooldown_duration:
                self.can_shoot = True
        
    def update(self, dt):
        ## tracking user input    
        keys = pygame.key.get_pressed()
        ## Narrows
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        ## WSAD
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        ## Moving player + normalizing speed of diagonal
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
    
        # Boundary check using clamp
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT - 50))

        ## Shooting
        recent_keys = pygame.key.get_just_pressed()    
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surface, self.rect.midtop, (all_sprites, laser_sprites))
            laser_sound.play()
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        self.laser_time()
        
        # ## Rotation
        # if recent_keys[pygame.K_d]:
        #     self.image = pygame.transform.rotate(self.original_surf, self.rotation[1])
        # elif recent_keys[pygame.K_a]:
        #     self.image = pygame.transform.rotate(self.original_surf, self.rotation[2])
        # elif recent_keys[pygame.K_w]:
        #     self.image = pygame.transform.rotate(self.original_surf, self.rotation[0])
        # elif recent_keys[pygame.K_s]:
        #     self.image = pygame.transform.rotate(self.original_surf, self.rotation[3])
        
class Star(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = star_surf
        self.rect = self.image.get_frect(center = (random.randint(0, WIDTH), random.randint(0, HEIGHT)))    

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
   
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 3500
        self.direction = pygame.Vector2(random.uniform(-0.3, 0.3),1)
        self.speed = random.randint(200, 500)
        self.rotation_speed = random.randint(0, 70)
        self.rotation = 0
        
        
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotate(self.original_surf, self.rotation)
        self.rect = self.image.get_frect(center = self.rect.center)
        
class Explosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
        
    
    def update(self, dt):
        self.frame_index += 35 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()
        
    
def collisions():
    global running
    collision = pygame.sprite.spritecollide(player, meteor_sprites, False, pygame.sprite.collide_mask)
    if collision:
        running = False
        
    for laser in laser_sprites:
        laser_hits = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        
        if laser_hits:
            Explosion(images, laser.rect.midtop,all_sprites)
            explosion_sound.play()
            laser.kill()
           
def display_score():
    current_time = pygame.time.get_ticks()  // 10
    text_surf = font.render(str(current_time), True, (230, 233, 230))
    text_rect = text_surf.get_frect(center = (WIDTH / 2, HEIGHT - 50))
    display_surface.blit(text_surf, text_rect.inflate(0, -10))
    pygame.draw.rect(display_surface, "darkgray", text_rect.inflate(15, 10), 3, 5, 10, 10, 15, 15)
   
# General setup
WIDTH, HEIGHT = 1280, 720
pygame.init()
clock = pygame.Clock()
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# import
meteor_surface = pygame.image.load('space_shooter/images/meteor.png').convert_alpha()
laser_surface = pygame.image.load('space_shooter/images/laser.png').convert_alpha()
star_surf = pygame.image.load('space_shooter/images/star.png').convert_alpha()
font = pygame.font.Font('space_shooter/images/Oxanium-Bold.ttf', 30)
player_surface = pygame.image.load('space_shooter/images/player.png').convert_alpha()
images = [pygame.image.load(f"space_shooter/images/explosion/{i}.png").convert_alpha() for i in range(21)]

## sound
laser_sound = pygame.mixer.Sound('space_shooter/audio/laser.wav')
laser_sound.set_volume(0.1)
explosion_sound = pygame.mixer.Sound('space_shooter/audio/explosion.wav')
explosion_sound.set_volume(0.1)
game_music = pygame.mixer.Sound('space_shooter/audio/game_music.wav')
game_music.set_volume(0.07)
game_music.play()

# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites)
player = Player(all_sprites)

# custom events
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 100)
  
running = True
while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            meteor = Meteor(meteor_surface, (random.randint(0, WIDTH),-100), (all_sprites, meteor_sprites))
        

    all_sprites.update(dt)
    collisions()
    display_surface.fill("#3a2e3f")
    all_sprites.draw(display_surface)
    display_score()
    pygame.display.update()
    
pygame.quit()
sys.exit()
   

        
 
        
    
  
    
         



