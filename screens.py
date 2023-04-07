import pygame
from map import Map
import doodle_jump_sprites
from enum import Enum

class Scenes(Enum):
    MAIN_GAME = 0
    MENU = 1
    GAME_OVER = 2
    PAUSED = 3

class Game_over():
    def __init__(self,screen,sprite_sheet,background,font):
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.background = background
        self.game_over_buttons = pygame.sprite.Group()
        self.game_over_buttons.add(doodle_jump_sprites.Button((self.screen.get_width() / 2) - 100, (self.screen.get_height() / 2) - 150, self.sprite_sheet.parse_sprite("play_again_button.png"),doodle_jump_sprites.BUTTON_TYPE.PLAY_AGAIN))
        self.game_over_buttons.add(doodle_jump_sprites.Button((self.screen.get_width() / 2) - 100, (self.screen.get_height() / 2) + 50, self.sprite_sheet.parse_sprite("menu@2x.png"),doodle_jump_sprites.BUTTON_TYPE.MENU))
        self.font = font

    def update(self):
        for button in self.game_over_buttons:
            if button.update() and button.get_button_type() == doodle_jump_sprites.BUTTON_TYPE.PLAY_AGAIN:
                return Scenes.MAIN_GAME,True
                
            elif button.update() and button.get_button_type() == doodle_jump_sprites.BUTTON_TYPE.MENU:
                return Scenes.MENU,True
        return Scenes.GAME_OVER,False

    def draw(self):
        self.screen.blit(self.background, [0, 0])
        self.game_over_buttons.draw(self.screen)

    def execute(self,dt):
        self.draw()
        return self.update()


class Main_game():
    def __init__(self,screen,sprite_sheet,background,font):
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.JUMP_LINE = 350
        self.x,self.y = screen.get_width() / 2, screen.get_height() / 2
        self.background = background
        self.game_map = Map()
        self.players = pygame.sprite.Group()
        self.players.add(doodle_jump_sprites.Player(self.sprite_sheet,self.x,self.y))
        self.players.remove()
        self.game_map.add_tile(doodle_jump_sprites.Green_platfrom(self.sprite_sheet,self.x, self.y + 300,"default_tile.png"))
        self.font = font
        self.score = 0
        self.current_font_distance = 15
        self.current_digit_amount = 1

    def draw(self,players,tiles,enemies,background):
        self.screen.blit(background, [0, 0])
        if len(str(self.score)) > self.current_digit_amount:
            self.current_font_distance += 13
            self.current_digit_amount += 1
        players.draw(self.screen)
        tiles.draw(self.screen)
        enemies.draw(self.screen)
        self.screen.blit(self.font.render(str(self.score),0,(0,0,0)),(self.screen.get_width() - self.current_font_distance,0))

    def update(self,players,tiles,enemies,dt):
        
        if not players:
            self.reset()
            return Scenes.GAME_OVER,False

        for player in players:
            scroll = player.update(tiles,enemies,self.JUMP_LINE)
            enemies.update(scroll,self.screen.get_width(),self.screen.get_height())
            tiles.update(scroll,self.screen.get_width(),self.screen.get_height(),dt)
            self.game_map.generate_tiles(self.sprite_sheet,player.get_score(),self.screen.get_width())
            self.score = player.get_score()
        self.game_map.spawn_enemy(self.sprite_sheet)
        return Scenes.MAIN_GAME,False

    def execute(self,dt):
        self.draw(self.players,self.game_map.get_tiles(),self.game_map.get_enemies(),self.background)
        return self.update(self.players,self.game_map.get_tiles(),self.game_map.get_enemies(),dt)

    def reset(self):
        self.players.empty()
        self.game_map.clear_tiles()
        self.game_map.clear_enemies()
        self.players.add(doodle_jump_sprites.Player(self.sprite_sheet,self.x,self.y))
        self.game_map.add_tile(doodle_jump_sprites.Green_platfrom(self.sprite_sheet,self.x, self.y + 300,"default_tile.png"))
        self.game_map.set_max_platforms(30)
        self.current_font_distance = 15
        self.current_digit_amount = 1


class main_menu():
    def __init__(self,screen,sprite_sheet,background,font):
        self.screen = screen
        self.x = (self.screen.get_width() / 2) - 200
        self.y = (self.screen.get_height() / 2) - 350
        self.background = background
        self.sprite_sheet = sprite_sheet
        self.font = font
        self.tear = self.sprite_sheet.parse_sprite("paper_tear.png")
        self.title = self.sprite_sheet.parse_sprite("doodle-jump@2x.png")
        self.enemies = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.enemies.add(doodle_jump_sprites.Blue_Winged_Monster(sprite_sheet,(self.screen.get_width() / 2) + 100,(self.screen.get_height() / 2) - 50,["monster_13.png","monster_14.png","monster_15.png","monster_16.png","monster_17.png"]))
        self.enemies.add(doodle_jump_sprites.Spider_monster(sprite_sheet,(self.screen.get_width() / 2) - 200,(self.screen.get_height() / 2) + 200,"monster_18.png"))
        self.buttons.add(doodle_jump_sprites.Button(self.x - 50,self.y + 200,self.sprite_sheet.parse_sprite("play@2x.png"),doodle_jump_sprites.BUTTON_TYPE.START))
        self.buttons.add(doodle_jump_sprites.Button(self.x - 20,self.y + 350,self.sprite_sheet.parse_sprite("quit_button.png"),doodle_jump_sprites.BUTTON_TYPE.QUIT))

    def update(self):

        for button in self.buttons:
            if button.update() and button.get_button_type() == doodle_jump_sprites.BUTTON_TYPE.START:
                self.enemies.update(0,self.screen.get_width(),self.screen.get_height())
                return Scenes.MAIN_GAME,True
            
            elif button.update() and button.get_button_type() == doodle_jump_sprites.BUTTON_TYPE.QUIT:
                self.enemies.update(0,self.screen.get_width(),self.screen.get_height())
                return None,True
        else:
            self.enemies.update(0,self.screen.get_width(),self.screen.get_height())
            return Scenes.MENU,False

    def execute(self,dt):
        self.draw()
        return self.update()

    def draw(self):
        self.screen.blit(self.background, [0, 0])
        self.screen.blit(self.title,(self.x - 70,self.y))
        self.buttons.draw(self.screen)
        self.screen.blit(self.tear,(0,self.screen.get_height() - 100))
        self.enemies.draw(self.screen)
        self.screen.blit(self.font.render("By Garrett and Evan",0,(0,0,0)),(self.x + 100,self.y + 100))

class Paused():
    def __init__(self,screen,background):
        self.screen = screen
        self.background = background
    
    def update(self):
        return Scenes.MAIN_GAME,False

    def draw(self):
        self.screen.blit(self.background, [0, 0])

    def execute(self,dt):
        self.draw()
        return self.update()
