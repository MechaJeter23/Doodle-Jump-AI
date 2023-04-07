#imports the pygame modules
import pygame
import os
import screens
from doodle_jump_sprites import SpriteSheet

WIDTH,HEIGHT = 640,920
FPS = 60
PATH_TO_ASSETS = os.path.join('Assets','doodle_jump_texture')

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Doodle Jump!")
SPRITESHEET = SpriteSheet(os.path.join(PATH_TO_ASSETS,'texture.png'))
pygame.display.set_icon(SPRITESHEET.parse_sprite("Icon@2x.png"))
BACKGROUND = SPRITESHEET.parse_sprite("bck@2x.png")
FONT = pygame.font.Font(os.path.join('Assets','al-seana.ttf'),28)


def main():
    clock = pygame.time.Clock()
    running = True
    Scenes = {
        screens.Scenes.MENU: screens.main_menu(screen,SPRITESHEET,BACKGROUND),
        screens.Scenes.MAIN_GAME: screens.Main_game(screen,SPRITESHEET,BACKGROUND,FONT),
        screens.Scenes.GAME_OVER: screens.Game_over(screen,SPRITESHEET,BACKGROUND,FONT),
        screens.Scenes.PAUSED: screens.Paused(screen,SPRITESHEET.parse_sprite("pause-cover@2x.png"))
    }
    current_screen = screens.Scenes.MENU

    while running:
        dt = clock.tick(FPS) / 100
        result,button_clicked = Scenes.get(current_screen).execute(dt)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            elif event.type == pygame.MOUSEBUTTONDOWN and button_clicked and result == None:
                running = False
                break

            elif event.type == pygame.MOUSEBUTTONDOWN and button_clicked:
                current_screen = result
                break

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and current_screen == screens.Scenes.MAIN_GAME:
                current_screen = screens.Scenes.PAUSED
                break

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and current_screen == screens.Scenes.PAUSED:
                current_screen = screens.Scenes.MAIN_GAME
                break

        else:
            if result == screens.Scenes.GAME_OVER:
                current_screen = result


    pygame.quit()

if __name__ == "__main__":
    main()
