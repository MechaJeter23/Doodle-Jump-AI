import random
import pygame
import doodle_jump_sprites

class Map():
    def __init__(self) -> None:
        self.tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.MAX_PLATFORMS = 30
        self.current_tile = None
    
    def get_enemies(self):
        return self.enemies

    def get_tiles(self):
        return self.tiles
    
    def add_tile(self,tile):
        self.tiles.add(tile)
        self.current_tile = tile

    def get_current_tile(self):
        return self.current_tile
    
    def clear_tiles(self):
        self.tiles.empty()

    def clear_enemies(self):
        self.enemies.empty()

    def set_max_platforms(self,value):
        self.MAX_PLATFORMS = value

    def generate_tiles(self,spritesheet,score,width):
        if score >= 0 and score <= 2500 and len(self.get_tiles()) < self.MAX_PLATFORMS:
            x = random.randint(0, width)
            y = self.get_current_tile().rect.y - random.randint(80,120)
            if random.randint(0,100) < 95:
                self.add_tile(doodle_jump_sprites.Green_platfrom(spritesheet,x,y,"default_tile.png"))
            else:
                self.add_tile(doodle_jump_sprites.Wooden_platform(spritesheet,x,y,["wooden_tile_1.png","wooden_tile_2.png","wooden_tile_3.png","wooden_tile_4.png"]))
        elif score >= 2500 and score <= 5500 and len(self.get_tiles()) < self.MAX_PLATFORMS:
            if self.MAX_PLATFORMS != 25:
                self.set_max_platforms(25)
            x = random.randint(0, width)
            y = self.get_current_tile().rect.y - random.randint(80,120)
            if random.randint(0,100) < 85:
                self.add_tile(doodle_jump_sprites.Green_platfrom(spritesheet,x,y,"default_tile.png"))

            elif random.randint(0,100) < 40:
                self.add_tile(doodle_jump_sprites.Blue_platform(spritesheet,x,y,"blue_tile.png"))
            elif random.randint(0,100) < 30:
                self.add_tile(doodle_jump_sprites.Wooden_platform(spritesheet,x,y,["wooden_tile_1.png","wooden_tile_2.png","wooden_tile_3.png","wooden_tile_4.png"]))

        
        elif score >= 5500 and score <= 10000 and len(self.get_tiles()) < self.MAX_PLATFORMS:
            if self.MAX_PLATFORMS != 20:
                self.set_max_platforms(20)
            x = random.randint(0, width)
            y = self.get_current_tile().rect.y - random.randint(80,120)
            if random.randint(0,100) < 50:
                self.add_tile(doodle_jump_sprites.Green_platfrom(spritesheet,x,y,"default_tile.png"))

            elif random.randint(0,100) < 50:
                self.add_tile(doodle_jump_sprites.Blue_platform(spritesheet,x,y,"blue_tile.png"))
            elif random.randint(0,100) < 5:
                self.add_tile(doodle_jump_sprites.Wooden_platform(spritesheet,x,y,["wooden_tile_1.png","wooden_tile_2.png","wooden_tile_3.png","wooden_tile_4.png"]))

        elif score >= 10000 and score <= 15000 and len(self.get_tiles()) < self.MAX_PLATFORMS:
            x = random.randint(0, width)
            y = self.get_current_tile().rect.y - random.randint(100,140)
            if random.randint(0,100) < 20:
                blue_platform = doodle_jump_sprites.Blue_platform(spritesheet,x,y,"blue_tile.png")
                blue_platform.set_rate(5) 
                self.add_tile(blue_platform)
            elif random.randint(0,100) < 5:
                self.add_tile(doodle_jump_sprites.White_platform(spritesheet,x,y,"white_tile.png"))

            elif random.randint(0,100) < 1:
                self.add_tile(doodle_jump_sprites.Wooden_platform(spritesheet,x,y,["wooden_tile_1.png","wooden_tile_2.png","wooden_tile_3.png","wooden_tile_4.png"]))

        elif score >= 15000 and score <= 25000 and len(self.get_tiles()) < self.MAX_PLATFORMS:
            if self.MAX_PLATFORMS != 7:
                self.set_max_platforms(7)
            x = random.randint(0, width)
            y = self.get_current_tile().rect.y - random.randint(120,180)
            if random.randint(0,100) < 30:
                self.add_tile(doodle_jump_sprites.White_platform(spritesheet,x,y,"white_tile.png"))
            elif random.randint(0,100) < 1:
                frames = ["magma_tile_1.png","magma_tile_2.png","magma_tile_3.png","magma_tile_4.png","magma_tile_5.png","magma_tile_6.png","magma_tile_7.png","magma_tile_8.png"]
                self.add_tile(doodle_jump_sprites.Magma_platform(spritesheet,x,y,frames))

        elif score >= 25000 and score <= 50000 and len(self.get_tiles()) < self.MAX_PLATFORMS:
            x = random.randint(0, width)
            y = self.get_current_tile().rect.y - random.randint(120,180)
            if random.randint(0,100) < 30:
                self.add_tile(doodle_jump_sprites.White_platform(spritesheet,x,y,"white_tile.png"))
            elif random.randint(0,100) < 20:
                blue_platform = doodle_jump_sprites.Blue_platform(spritesheet,x,y,"blue_tile.png")
                blue_platform.set_rate(9)


    def spawn_enemy(self,spritesheet):
        tile = self.get_current_tile()
        match random.randint(0,20000):
            case 1250:
                self.enemies.add(doodle_jump_sprites.Blue_Winged_Monster(spritesheet,random.randint(10,tile.rect.left + 20),random.randint(tile.rect.top,tile.rect.top + 50),["monster_13.png","monster_14.png","monster_15.png","monster_16.png","monster_17.png"]))

            case 5751:
                self.enemies.add(doodle_jump_sprites.Blue_Winged_Monster(spritesheet,random.randint(10,tile.rect.left + 20),random.randint(tile.rect.top,tile.rect.top + 50),["monster_13.png","monster_14.png","monster_15.png","monster_16.png","monster_17.png"]))

            case 135:
                self.enemies.add(doodle_jump_sprites.Three_eyed_winged(spritesheet,random.randint(10,tile.rect.left + 20),random.randint(tile.rect.top,tile.rect.top + 50),["monster_8.png","monster_9.png","monster_10.png","monster_11.png","monster_12.png"]))

            case 3761:
                self.enemies.add(doodle_jump_sprites.Spider_monster(spritesheet,random.randint(10,tile.rect.left + 20),random.randint(tile.rect.top - 100,tile.rect.top - 50),"monster_18.png"))

            case 914:
                self.enemies.add(doodle_jump_sprites.Cyclopse(spritesheet,random.randint(10,tile.rect.left + 20),random.randint(tile.rect.top,tile.rect.top + 50),["monster_6.png","monster_7.png"]))