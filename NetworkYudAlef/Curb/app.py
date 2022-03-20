import time
import random
import pygame
from pygame.locals import *
from utils import *
from communication import *
import os
from configparser import ConfigParser

# apply configs
config = ConfigParser()
config.read('conf.ini')
WIDTH = int(config.get('settings', 'WINDOW_WIDTH'))
HEIGHT = int(config.get('settings', 'WINDOW_HEIGHT'))
# audio setup
mixer = MusicManager(['resources/music/' + music for music in os.listdir('resources/music')], 0.1)

# pygame setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# assets
pix_font = pygame.font.Font('resources\\fonts\\yoster-island\\yoster.ttf', 25)

# debug assets
framerate_text = Text(50, 50, 'FPS: ', pix_font, (255, 0, 0))

# title screen assets
title = Image(0, 0, "resources\\images\\title-screen.png", True)
w, h = title.get_size()
connect_btn = Button(w / 2 - 200, h / 2 + 100, 400, 100, "Connect", (0, 0, 0), pix_font, (45, 115, 178), (8, 96, 168),
                     (0, 0, 0), 0)
settings_btn = Button(w / 2 - 200, h / 2 + 220, 400, 100, "Settings", (0, 0, 0), pix_font, (45, 115, 178), (8, 96, 168),
                      (0, 0, 0), 0)
quit_btn = Button(w / 2 - 200, h / 2 + 340, 400, 100, "Quit", (0, 0, 0), pix_font, (45, 115, 178), (8, 96, 168),
                  (0, 0, 0), 0)

ip_input = InputBox(w / 2-299, h / 2+43, 400, 50, (0, 0, 0), (10, 10, 10), pix_font, "127.0.0.1")#"IP:")
port_input = InputBox(w / 2-100, h / 2 + 43, 400, 50, (0, 0, 0), (10, 10, 10), pix_font, "5555") #"PORT:")
name_input = InputBox(w / 2+99, h / 2 + 43, 400, 50, (0, 0, 0), (10, 10, 10), pix_font, "NAME:")

waiting_for_players = Text(w / 2, h / 2 + 200, "Waiting for players...", pix_font, (0, 0, 0))

# settings assets
settings = Image(0, 0, "resources\\images\\settings.png", True)
volume_slider = Slider(w / 2 - 200 + 15, h / 2 - 400, 400, 100, 0, 1, 1, "Music Volume", pix_font, (255, 255, 255),
                       (8, 96, 168), (45, 115, 178), (8, 96, 168), 2)
quit_settings_button = Button(0, 0, 400, 100, "Quit", (0, 0, 0), pix_font, (45, 115, 178), (8, 96, 168), (0, 0, 0), 0)

# game assets

players = ["Cyborg","Punk","Biker"]
choice = random.choice(players)

monologue = Image(0, 0, "resources\\images\\monologue.png", True)
player = Player(f"resources\\sprites\\{choice}_Thin\\{choice}_idle.png", f"resources\\sprites\\{choice}_Thin\\{choice}_run.png",
                f"resources\\sprites\\{choice}_Thin\\{choice}_jump.png",f"resources\\sprites\\{choice}_Thin\\{choice}_death.png", 32, 32, 48, (w / 2, h - 500), 500)
# gameover assets
gameover_button = Button(0, 0, 400, 100, "Restart", (0, 0, 0), pix_font, (45, 115, 178), (8, 96, 168), (0, 0, 0), 0)
gameover = None

renderer = Renderer(screen, title)
renderer.game_started = False

cl = None


def connect(ip,port, name):
    global cl
    cl = Client(ip, port, name, renderer)
    cl.send_pp(player=player)


def init_opening_screen():
    global renderer
    renderer.add_child(connect_btn)
    renderer.add_child(settings_btn)
    renderer.add_child(quit_btn)
    renderer.add_child(ip_input)
    renderer.add_child(port_input)
    renderer.add_child(name_input)


init_opening_screen()


def init_game():
    global renderer
    global player
    player = renderer.get_player()
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

def init_settings():
    renderer.add_child(volume_slider)
    renderer.add_child(quit_settings_button)


def init_gameover():
    global renderer
    global gameover
    global player
    global choice
    player = Player(f"resources\\sprites\\{choice}_Thin\\{choice}_idle.png", f"resources\\sprites\\{choice}_Thin\\{choice}_run.png",
                f"resources\\sprites\\{choice}_Thin\\{choice}_jump.png", 32, 32, 48, (w / 2, h - 500), 500)

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
        if renderer.background == title and not renderer.background.is_fading_out:
            ip_input.handle_event(event)
            port_input.handle_event(event)
            name_input.handle_event(event)
        if event.type == pygame.MOUSEBUTTONUP:
            if renderer.background == title and not renderer.background.is_fading_out:
                if quit_btn.is_clicked(pygame.mouse.get_pos()):
                    running = False
                elif connect_btn.is_clicked(pygame.mouse.get_pos()):
                    renderer.remove_child(connect_btn)
                    renderer.remove_child(settings_btn)
                    renderer.remove_child(quit_btn)
                    renderer.remove_child(ip_input)
                    renderer.remove_child(port_input)
                    renderer.remove_child(name_input)
                    connect(ip_input.text, int(port_input.text), random_name() if name_input.text == "NAME:" or name_input.text == "" else name_input.text)
                    renderer.add_child(waiting_for_players)
                elif settings_btn.is_clicked(pygame.mouse.get_pos()):
                    renderer.remove_child(connect_btn)
                    renderer.remove_child(settings_btn)
                    renderer.remove_child(quit_btn)
                    renderer.remove_child(ip_input)
                    renderer.remove_child(port_input)
                    renderer.remove_child(name_input)
                    renderer.fadeout_bg(settings)
                    init_settings()
            elif renderer.background == settings and not renderer.background.is_fading_out:
                if quit_settings_button.is_clicked(pygame.mouse.get_pos()):
                    renderer.remove_child(volume_slider)
                    renderer.remove_child(quit_settings_button)
                    renderer.fadeout_bg(title)
                    init_opening_screen()
            elif renderer.background == gameover and not renderer.background.is_fading_out:
                if gameover_button.is_clicked(pygame.mouse.get_pos()):
                    renderer.remove_child(gameover_button)
                    renderer.fadeout_bg(title)
                    init_opening_screen()
                    mixer.stop_music()
        if renderer.game_started:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.dash(renderer.dt)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.move("stay")
                if event.key == pygame.K_d:
                    player.move("stay")
            if event.type == pygame.MOUSEBUTTONUP:
                renderer.add_bullet((player.x if player.x < WIDTH / 2 else WIDTH / 2) + player.image.get_width() / 2,
                                    player.y + player.image.get_height() / 2, pygame.mouse.get_pos()[0],
                                    pygame.mouse.get_pos()[1], 10, True, 700)

    if renderer.game_started and renderer.background == title:
        renderer.fadeout_bg(monologue)
        renderer.clear_children()
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
        renderer.game_started = False

    if renderer.game_started:
        mixer.update()
        if keys[pygame.K_a]:
            player.move("left")
        if keys[pygame.K_d]:
            player.move("right")
        if keys[pygame.K_w]:
            player.jump()
        if player.x > WIDTH / 2:
            renderer.background_progression = player.x - WIDTH / 2
        if player.y + player.image.get_height() > h - 170:
            player.is_temp_dead = True
            # init_gameover()
            # renderer.game_started = False

    if player.revived:
        player.revived = False
        renderer.background_progression = 0

    pygame.draw.rect(screen, (0, 0, 0), (0, 0, w, h))
    renderer.update_all()
    renderer.render_all(pygame.mouse.get_pos())
    if renderer.game_started:
        player.draw_stats(screen, pix_font)
        cl.send_player_coords(player.x, player.y)
    pygame.display.flip()
    framerate_text.set_text("FPS: " + str(int(clock.get_fps())))
    clock.tick(60)
    renderer.update_dt()

pygame.quit()
if cl is not None:
    cl.send_quit()
    cl.close()

# tile reflection, crystalize, dents
