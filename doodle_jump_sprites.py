import pygame
from enum import Enum
import json
from abc import ABC,abstractclassmethod
import random

class BUTTON_TYPE(Enum):
    PLAY_AGAIN = 0
    MENU = 1
    RESUME = 2
    START = 3
    QUIT = 4

class POSITIONS(Enum):
    LEFT = 0
    RIGHT = 1
    SHOOTING = 2

class SpriteSheet:
    def __init__(self,filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename)
        self.meta_data = self.filename.replace('png','json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self,x,y,width,height):
        sprite = pygame.Surface((width,height),flags=pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet,(0,0),(x,y,width,height))
        return sprite

    def parse_sprite(self,name):
        sprite = self.data['frames'][name]['frame']
        x,y,width,height = sprite['x'],sprite['y'],sprite['w'],sprite['h']
        return self.get_sprite(x,y,width,height)
    
class Player(pygame.sprite.Sprite):
    def __init__(self,sprite_sheet,pos_x,pos_y) -> None:
        super(Player,self).__init__()
        self.sprite_sheet = sprite_sheet
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.score = 0
        self.sprites = {
            POSITIONS.LEFT: self.sprite_sheet.parse_sprite("lik-left@2x.png"),
            POSITIONS.RIGHT: self.sprite_sheet.parse_sprite('lik-right@2x.png'),
            POSITIONS.SHOOTING: [self.sprite_sheet.parse_sprite('lik-puca@2x.png'),self.sprite_sheet.parse_sprite('lik-njuska@2x.png')],
        }
        self.image = self.sprites.get(POSITIONS.LEFT)
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos_x,self.pos_y)
        self.vel_y = 0
        self.game_width,self.game_height = pygame.display.get_surface().get_size()
        self.dead = False

    def get_score(self):
        return self.score

    def update(self,tiles,enemies,jump_line):

        gravity = 0.5
        scroll = 0
        dy = 0
        dx = 0

        self.vel_y += gravity
        dy += self.vel_y
        
        if self.rect.y >= self.game_height:
            self.kill()

        elif not self.dead:
            keys = pygame.key.get_pressed()

            if self.rect.x <= -30:
                self.rect.x = self.game_width
        
            elif self.rect.x >= self.game_width + 20:
                self.rect.x = -5

            if keys[pygame.K_a]:
                dx = -8
                self.image = self.sprites.get(POSITIONS.LEFT)

            elif keys[pygame.K_d]:
                dx = 8
                self.image = self.sprites.get(POSITIONS.RIGHT)


            enemies_collided = pygame.sprite.spritecollide(self, enemies, False)
            for collided in enemies_collided:
                if self.rect.bottom <= collided.rect.top + 20 and self.vel_y > 0:
                    self.rect.bottom = collided.rect.top
                    dy = 0
                    self.vel_y = -18
                    collided.kill()
                elif self.rect.top <= collided.rect.bottom and (self.rect.x + 10 >= collided.rect.x or self.rect.x - 10 <= collided.rect.x):
                    self.vel_y = 5
                    self.dead = True
                    self.rect.x += dx
                    self.rect.y += dy + scroll
                    return scroll

            ground_hit_list = pygame.sprite.spritecollide(self, tiles, False)   
            for platform in ground_hit_list:
                if self.rect.bottom < platform.rect.centery + 15 and self.vel_y > 0 and platform.is_tile_jumpable():
                    self.rect.bottom = platform.rect.top
                    dy = 0
                    self.vel_y = -18
        
            if self.rect.top <= jump_line and self.vel_y < 0:
                self.score += 3
                scroll = -dy

        self.rect.x += dx
        self.rect.y += dy + scroll
        return scroll

class Platform(ABC,pygame.sprite.Sprite):
    def __init__(self,sprite_sheet,pos_x,pos_y,filename) -> None:
        super(Platform,self).__init__()
        self.sprite_sheet = sprite_sheet
        self.jumpable = True
        if type(filename) == list:
            self.current_frame = 0
            self.frames = []
            for file in filename:
                self.frames.append(self.sprite_sheet.parse_sprite(file))
            self.image = self.frames[0]
            self.rect = self.image.get_rect()
            self.rect.center = (pos_x,pos_y)
        
        else:
            self.image = self.sprite_sheet.parse_sprite(filename)
            self.rect = self.image.get_rect()
            self.rect.center = (pos_x,pos_y)
    
    @abstractclassmethod
    def is_tile_jumpable(self):
        pass

    def update(self,scroll,width,height,dt):
        self.rect.y += scroll
        if self.rect.y >= height:
            self.kill()


class Green_platfrom(Platform):
    def is_tile_jumpable(self):
        return self.jumpable
    
    def update(self,scroll,width,height,dt):
        return super().update(scroll,width,height,dt)
             

class Blue_platform(Platform):

    def __init__(self, sprite_sheet, pos_x, pos_y, filename) -> None:
        super().__init__(sprite_sheet, pos_x, pos_y, filename)
        self.rate = 2

    def is_tile_jumpable(self):
        return self.jumpable
    
    def set_rate(self,value):
        self.rate = value
    
    def update(self,scroll,width,height,dt):
        if self.rect.x >= width - 120:
            self.rate = -abs(self.rate)
        elif self.rect.x <= 0:
            self.rate = abs(self.rate)
        self.rect.x += self.rate
        return super().update(scroll,width,height,dt)
        

class Wooden_platform(Platform):
    def __init__(self, sprite_sheet, pos_x, pos_y, filename) -> None:
        super().__init__(sprite_sheet, pos_x, pos_y, filename)
        self.jumpable = False
        self.broken = False

    def is_tile_jumpable(self):
        if not self.broken:
            self.set_to_broken()
        return self.jumpable

    def is_broken(self):
        return self.broken

    def set_to_broken(self):
        self.broken = True

    def update(self,scroll,width,height,dt):
        if self.is_broken():
            if self.current_frame + 1 < len(self.frames):
                self.current_frame += 1
                self.image = self.frames[self.current_frame]
            self.rect.y += 10
        return super().update(scroll,width,height,dt)
    


class Gray_platform(Platform):

    def __init__(self, sprite_sheet, pos_x, pos_y, filename) -> None:
        super().__init__(sprite_sheet, pos_x, pos_y, filename)
        self.rate = 2
        self.max_height = 150
        self.minimum_height = 350

    def is_tile_jumpable(self):
        return self.jumpable
    
    def update(self,scroll,width,height,dt):

        if scroll > 0:
            self.max_height -= 350
            self.minimum_height += 100

        if self.rect.y >= self.minimum_height:
            self.rate = -abs(self.rate)
        elif self.rect.y <= self.max_height:
            self.rate = abs(self.rate)
        self.rect.y += self.rate
        return super().update(scroll,width,height,dt)
    
class White_platform(Platform):
    def __init__(self, sprite_sheet, pos_x, pos_y, filename) -> None:
        super().__init__(sprite_sheet, pos_x, pos_y, filename)
        self.jumpable = True
        self.broken = False

    def is_tile_jumpable(self):
        
        if not self.is_broken():
            self.set_to_broken()
            previous_state = self.jumpable
            self.jumpable = False
            return previous_state
        
        return self.jumpable

    def is_broken(self):
        return self.broken

    def set_to_broken(self):
        self.broken = True

    def update(self,scroll,width,height,dt):
        if self.is_broken():
            self.kill()
        return super().update(scroll,width,height,dt)
    
class Magma_platform(Platform):
    def __init__(self, sprite_sheet, pos_x, pos_y, filename) -> None:
        super().__init__(sprite_sheet, pos_x, pos_y, filename)
        self.jumpable = True
        self.broken = False
        self.timer = random.randint(8,16)

    def is_tile_jumpable(self):
        
        if not self.is_broken():
            self.set_to_broken()
            previous_state = self.jumpable
            self.jumpable = False
            return previous_state
        
        return self.jumpable

    def is_broken(self):
        return self.broken

    def set_to_broken(self):
        self.broken = True

    def update(self,scroll,width,height,dt):
        if self.is_broken() and self.current_frame + 1 < len(self.frames):
            self.current_frame += 1
            self.image = self.frames[self.current_frame]
            return super().update(scroll,width,height,dt)
        
        elif self.current_frame + 1 >= len(self.frames):
            self.kill()
        
        elif self.timer <= 0:
            self.set_to_broken()
            self.jumpable = False
            return super().update(scroll,width,height,dt)
        
        else:
            self.timer -= dt
            return super().update(scroll,width,height,dt)
        
class Button(pygame.sprite.Sprite):
    def __init__(self,x,y,image,button_type) -> None:
        super(Button,self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.button_type = button_type

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False

    def get_button_type(self):
        return self.button_type
    

class Enemy(pygame.sprite.Sprite,ABC):
    def __init__(self,sprite_sheet,pos_x,pos_y,filename) -> None:
        super(Enemy,self).__init__()
        self.sprite_sheet = sprite_sheet
        self.pos_x = pos_x
        self.pos_y = pos_y
        if type(filename) == list:
            self.current_frame = 0
            self.frames = []
            for file in filename:
                self.frames.append(self.sprite_sheet.parse_sprite(file))
            self.image = self.frames[0]
            self.rect = self.image.get_rect()
            self.rect.center = (self.pos_x,pos_y)
        
        else:
            self.image = self.sprite_sheet.parse_sprite(filename)
            self.rect = self.image.get_rect()
            self.rect.center = (self.pos_x,pos_y)

    def update(self,scroll,width,height):
        self.rect.y += scroll
        if self.rect.y >= height:
            self.kill()


class Blue_Winged_Monster(Enemy):
    def __init__(self, sprite_sheet, pos_x, pos_y, filename) -> None:
        super().__init__(sprite_sheet, pos_x, pos_y, filename)
        self.current_frame = 0
        self.max = self.pos_x + 20
        self.min =  self.pos_x - 20
        self.rate = 2
        self.reversed = False


    def update(self, scroll, width, height):
        if self.current_frame + 1 < len(self.frames) and not self.reversed:
            self.current_frame += 1
            self.image = self.frames[self.current_frame]
        
        elif self.current_frame >= 0 and self.reversed:
            self.current_frame -= 1
            self.image = self.frames[self.current_frame]

        else:
            self.reversed = not self.reversed

        if self.rect.x <= self.min:
            self.rate = abs(self.rate)
        elif self.rect.x >= self.max:
            self.rate = -abs(self.rate)
        self.rect.x += self.rate
        return super().update(scroll, width, height)  

class Cyclopse(Enemy):
    def __init__(self, sprite_sheet, pos_x, pos_y, filename) -> None:
        super().__init__(sprite_sheet, pos_x, pos_y, filename)
        self.rate = 2

    def update(self, scroll, width, height):
        if self.rect.x <= 0:
            self.current_frame = 0
            self.image = self.frames[self.current_frame]
            self.rate = abs(self.rate)
        elif self.rect.x >= width:
            self.current_frame = 1
            self.image = self.frames[self.current_frame]
            self.rate = -abs(self.rate)
        self.rect.x += self.rate
        return super().update(scroll, width, height)
    

class Three_eyed_winged(Enemy):
    def __init__(self, sprite_sheet, pos_x, pos_y, filename) -> None:
        super().__init__(sprite_sheet, pos_x, pos_y, filename)
        self.current_frame = 0
        self.rate = 2
        self.reversed = False


    def update(self, scroll, width, height):
        if self.current_frame + 1 < len(self.frames) and not self.reversed:
            self.current_frame += 1
            self.image = self.frames[self.current_frame]
        
        elif self.current_frame >= 0 and self.reversed:
            self.current_frame -= 1
            self.image = self.frames[self.current_frame]

        else:
            self.reversed = not self.reversed
        self.rect.y += self.rate
        return super().update(scroll, width, height) 
    

class Spider_monster(Enemy):
    def __init__(self, sprite_sheet, pos_x, pos_y, filename) -> None:
        super().__init__(sprite_sheet, pos_x, pos_y, filename)
        self.max = self.pos_x + 20
        self.min =  self.pos_x - 20
        self.rate = 2

    def update(self, scroll, width, height):
        if self.rect.x <= self.min:
            self.rate = abs(self.rate)
        elif self.rect.x >= self.max:
            self.rate = -abs(self.rate)
        self.rect.x += self.rate
        return super().update(scroll, width, height)