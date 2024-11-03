from settings import *
from player import Player
from sprites import *
from groups import AllSprites
from pytmx.util_pygame import load_pygame

from random import randint, choice
import sys



class Game:
    def __init__(self):
        ## Setup
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Surviror")
        
        ## Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
    
        ## Shooting timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100
        
        ## Enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 1000)
        self.spawn_positions = []
        
        ## Audio
        self.shoot_sound = pygame.mixer.Sound(join("Vampire survivor", "audio", "shoot.wav"))
        self.shoot_sound.set_volume(0.2)
        self.music = pygame.mixer.Sound(join("Vampire survivor", "audio", "music.wav"))
        self.music.set_volume(0.08)
        self.music.play(-1)
        self.impact = pygame.mixer.Sound(join("Vampire survivor", "audio", "impact.ogg"))

        
        ## Setup
        self.load_images()
        self.setup()        
   
    def load_images(self):
        self.bullet_surf = pygame.image.load(join("Vampire survivor", "images", "gun", "bullet.png")).convert_alpha()
        
        folders = list(walk(join('Vampire survivor', 'images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for file_path, sub_folder, files in walk(join('Vampire survivor', 'images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file in sorted(files, key = lambda name : int(name.split(".")[0])):
                    full_path = join(file_path, file)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)


    ## Uploading objects to the Sprites      
    def setup(self):
        map = load_pygame("vampire survivor/data/maps/world.tmx")
        
        for obj in map.get_layer_by_name("Collisions"):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        
        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        
        for obj in map.get_layer_by_name("Objects"):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))
    
    ## Mouse input for shooting
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.shoot_sound.play()
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
    
    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True
  
    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                for sprite in collision_sprites:
                    self.impact.play(0)
                    self.impact.set_volume(0.6)
                    sprite.destroy()
                    bullet.kill()
    
    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False          
         
    ## Start of the game  
    def run(self):
        while self.running == True:
            dt = self.clock.tick() / 1000
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == self.enemy_event:
                Enemies(choice(self.spawn_positions), choice(list(self.enemy_frames.values())), self.player, (self.all_sprites, self.enemy_sprites), self.collision_sprites)
                
                
            
    def update(self, dt):
        #self.music.play()
        #self.music.set_volume(0.03)
        self.gun_timer()
        self.input()
        self.all_sprites.update(dt)
        self.bullet_collision()
        self.player_collision()
        
      
    ## Display       
    def draw(self):
        self.display_surface.fill("#3a2e3f")
        self.all_sprites.draw(self.player.rect.center)
        pygame.display.update()
        
        

if __name__ == "__main__":

    game = Game()
    game.run()