import pygame
from pygame.locals import *
from utils import *
import os

# audio setup
mixer = MusicManager(['resources/music/' + music for music in os.listdir('resources/music')], 0.1)

# pygame setup
pygame.init()
clock = pygame.time.Clock()

pix_font = pygame.font.Font('resources\\fonts\\yoster-island\\yoster.ttf', 25)

# debug assets
framerate_text = Text(50, 50, 'FPS: ', pix_font, (255, 0, 0))

# title screen assets
title = Image(0, 0, "resources\\images\\title-screen.png", True)
w, h = title.get_size()
start_btn = Button(w / 2 - 200, h / 2 + 100, 400, 100, "Start", (0, 0, 0), pix_font, (45, 115, 178), (8, 96, 168),
                   (0, 0, 0), 0)
settings_btn = Button(w / 2 - 200, h / 2 + 220, 400, 100, "Settings", (0, 0, 0), pix_font, (45, 115, 178), (8, 96, 168),
                      (0, 0, 0), 0)
quit_btn = Button(w / 2 - 200, h / 2 + 340, 400, 100, "Quit", (0, 0, 0), pix_font, (45, 115, 178), (8, 96, 168),
                  (0, 0, 0), 0)

# settings assets
settings = Image(0, 0, "resources\\images\\settings.png", True)
volume_slider = Slider(w / 2 - 200 + 15, h / 2 - 400, 400, 100, 0, 1, 1, "Music Volume", pix_font, (255, 255, 255),
                       (8, 96, 168), (45, 115, 178), (8, 96, 168), 2)
quit_settings_button = Button(0, 0, 400, 100, "Quit", (0, 0, 0), pix_font, (45, 115, 178), (8, 96, 168), (0, 0, 0), 0)

# game assets
started = False
started_fadeout = False
monologue = Image(0, 0, "resources\\images\\monologue.png", True)
player = Player("resources\\sprites\\Cyborg_Thin\\Cyborg_idle.png", "resources\\sprites\\Cyborg_Thin\\Cyborg_run.png",
                "resources\\sprites\\Cyborg_Thin\\Cyborg_jump.png", 32, 32, 48, (w / 2, h - 500), 12)

# gameover assets
gameover_button = Button(0, 0, 400, 100, "Restart", (0, 0, 0), pix_font, (45, 115, 178), (8, 96, 168), (0, 0, 0), 0)
gameover = None

screen = pygame.display.set_mode((w, h))
renderer = Renderer(screen, title)


def init_opening_screen():
    renderer.add_child(start_btn)
    renderer.add_child(settings_btn)
    renderer.add_child(quit_btn)


init_opening_screen()


def init_game():
    global started
    renderer.add_sprite(player)
    renderer.add_platform((0, h - 255), 2285, 255)
    renderer.add_platform((3259, h - 255), 148, 255)
    renderer.add_platform((3523, h - 486), 148, 486)
    renderer.add_platform((3919, h - 387), 313, 387)
    renderer.add_platform((4579, h - 225), 115, 225)
    renderer.add_platform((4810, h - 849), 148, 849)
    renderer.add_child(JumpPad((4579, h - 225 - 40), 115, 40, 1.7))
    renderer.add_platform((5305, h - 519), 148, 519)
    renderer.add_platform((5470, 0), 148, 264)
    renderer.add_platform((5668, h - 519), 148, 519)
    renderer.add_platform((6097, h - 222), 1903, 222)
    renderer.add_platform((6328, 0), 280, 462)
    renderer.add_child(framerate_text)
    started = True


def init_settings():
    renderer.add_child(volume_slider)
    renderer.add_child(quit_settings_button)

def init_gameover():
    global gameover
    global player
    player.__init__("resources\\sprites\\Cyborg_Thin\\Cyborg_idle.png", "resources\\sprites\\Cyborg_Thin\\Cyborg_run.png",
                "resources\\sprites\\Cyborg_Thin\\Cyborg_jump.png", 32, 32, 48, (w / 2, h - 500), 12)
    gameover = Image(0, 0, "resources\\images\\death_screens\\death_screen" + str(random.randint(0, 2)) + ".png")
    renderer.__init__(screen, gameover)
    renderer.add_child(gameover_button)
    renderer.background_progression = 0
    mixer.start_specific_music('resources/gameover.mp3')

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0
        if event.type == pygame.MOUSEBUTTONUP:
            if not started and not started_fadeout and not renderer.background.is_fading_out:
                if quit_btn.is_clicked(pygame.mouse.get_pos()):
                    running = False
                elif start_btn.is_clicked(pygame.mouse.get_pos()):
                    renderer.remove_child(start_btn)
                    renderer.remove_child(settings_btn)
                    renderer.remove_child(quit_btn)
                    renderer.fadeout_bg(monologue)
                    started_fadeout = True
                elif settings_btn.is_clicked(pygame.mouse.get_pos()):
                    renderer.remove_child(start_btn)
                    renderer.remove_child(settings_btn)
                    renderer.remove_child(quit_btn)
                    renderer.fadeout_bg(settings)
                    init_settings()

            if renderer.background == settings and not renderer.background.is_fading_out:
                if quit_settings_button.is_clicked(pygame.mouse.get_pos()):
                    renderer.remove_child(volume_slider)
                    renderer.remove_child(quit_settings_button)
                    renderer.fadeout_bg(title)
                    init_opening_screen()
            elif renderer.background == gameover:
                if gameover_button.is_clicked(pygame.mouse.get_pos()):
                    renderer.remove_child(gameover_button)
                    renderer.fadeout_bg(title)
                    init_opening_screen()
                    mixer.stop_music()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.dash()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.move("stay")
            if event.key == pygame.K_d:
                player.move("stay")
    if renderer.background == monologue and not started:
        init_game()

    if pygame.mouse.get_pressed(3)[0]:
        if renderer.background == settings:
            volume_slider.update(pygame.mouse.get_pos())
            mixer.set_volume(volume_slider.value)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        player.__init__("resources\\sprites\\Cyborg_Thin\\Cyborg_idle.png",
                        "resources\\sprites\\Cyborg_Thin\\Cyborg_run.png",
                        "resources\\sprites\\Cyborg_Thin\\Cyborg_jump.png", 32, 32, 48, (w / 2, h - 500), 12)
        renderer.__init__(screen, title)
        mixer.stop_music()
        init_opening_screen()
        started = False
        started_fadeout = False

    if started:
        mixer.update()
        if keys[pygame.K_a]:
            player.move("left")
        if keys[pygame.K_d]:
            player.move("right")
        if keys[pygame.K_w]:
            player.jump()
        if player.x > 1920 / 2:
            renderer.background_progression = player.x - 1920 / 2
        if player.y + player.image.get_height() > h-170:
            init_gameover()
            started = False
            started_fadeout = False

    pygame.draw.rect(screen, (0, 0, 0), (0, 0, w, h))
    renderer.update_all()
    renderer.render_all(pygame.mouse.get_pos())
    if started:
        player.draw_stats(screen, pix_font)
    pygame.display.flip()
    framerate_text.set_text("FPS: " + str(int(clock.get_fps())))
    clock.tick(60)

pygame.quit()

# tile reflection, crystalize, dents
