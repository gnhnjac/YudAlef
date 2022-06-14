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
IS_FULLSCREEN = config.getboolean('settings', 'FULLSCREEN')
REFRESH_RATE = min(int(config.get('settings', 'REFRESH_RATE')), 60)
# audio setup
mixer = MusicManager(['resources/music/' + music for music in os.listdir('resources/music')], 0.1)

# pygame setup
pygame.init()
if IS_FULLSCREEN:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

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

ip_input = InputBox(w / 2 - 299, h / 2 + 43, 400, 50, (0, 0, 0), (10, 10, 10), pix_font, "127.0.0.1")  # "IP:")
port_input = InputBox(w / 2 - 100, h / 2 + 43, 400, 50, (0, 0, 0), (10, 10, 10), pix_font, "5555")  # "PORT:")
name_input = InputBox(w / 2 + 99, h / 2 + 43, 400, 50, (0, 0, 0), (10, 10, 10), pix_font, "NAME:")

waiting_for_players = Text(w / 2, h / 2 + 200, "Waiting for players...", pix_font, (0, 0, 0))

# settings assets
settings = Image(0, 0, "resources\\images\\settings.png", True)
volume_slider = Slider(w / 2 - 200 + 15, h / 2 - 400, 400, 100, 0, 1, 1, "Music Volume", pix_font, (255, 255, 255),
                       (8, 96, 168), (45, 115, 178), (8, 96, 168), 2)
quit_settings_button = Button(0, 0, 400, 100, "Quit", (0, 0, 0), pix_font, (45, 115, 178), (8, 96, 168), (0, 0, 0), 0)

# convert_radio_btn = Checkbox(screen, w / 2 - 200 + 15, h / 2 - 300, (230,230,230),"Change convert method (In case of poor performance)",(0,0,0),(0,0,0), pix_font, (8, 96, 168))

# game assets

players = ["Cyborg", "Punk", "Biker"]
choice = random.choice(players)

monologue = Image(0, 0, "resources\\images\\monologue.png", True)
player = Player(f"resources\\sprites\\{choice}_Thin\\{choice}_idle.png",
                f"resources\\sprites\\{choice}_Thin\\{choice}_run.png",
                f"resources\\sprites\\{choice}_Thin\\{choice}_jump.png",
                f"resources\\sprites\\{choice}_Thin\\{choice}_death.png",
                f"resources\\sprites\\{choice}_Thin\\{choice}_dash.png", 32, 32, 48, (w / 2, h - 500), 500)

# gameover assets
gameover_button = Button(0, 0, 400, 100, "Restart", (0, 0, 0), pix_font, (45, 115, 178), (8, 96, 168), (0, 0, 0), 0)
gameover = None

# arena assets
arena = Image(0, 0, "resources\\images\\arena-repeating-bg.png", True, None, None, True, 4000, 1080)

guns = [Weapons.GUN, Weapons.SHOTGUN, Weapons.SYN_UZI, Weapons.FIRE_WALL_FLAMETHROWER, Weapons.MACHINE_GUN,
        Weapons.LASER]
weapon_index = 0

renderer = Renderer(screen, title)
renderer.game_started = False

player_still = False

cl = None


def connect(ip, port, name):
    global cl
    if cl is None:
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


def init_monologue(fade_in=True):
    global renderer
    global player
    player.change_weapon(Weapons.GUN)
    if renderer.world is not None and "level" in renderer.world:
        player.x = 7700
        renderer.orig_background_progressionx = 8000 - WIDTH
        renderer.background_progressionx = 8000 - WIDTH
    else:
        player.x = 150
        renderer.orig_background_progressionx = 0
        renderer.background_progressionx = 0
    renderer.world = "monologue"
    renderer.clear_platforms()
    renderer.clear_children()
    renderer.clear_bullets()
    if fade_in:
        renderer.fadeout_bg(monologue)
        player.y = h - 500
    else:
        player.y = h - 500
        renderer.replace_bg(monologue)
    player.max_y = None
    player.orig_x, player.orig_y = player.x, player.y
    renderer.add_imaginary_platform(JumpCrystal((2522, 648)))
    renderer.add_imaginary_platform(JumpCrystal((2759, 648)))
    renderer.add_imaginary_platform(JumpCrystal((2966, 648)))
    renderer.add_imaginary_platform(JumpCrystal((3438, 658)))
    renderer.add_imaginary_platform(JumpCrystal((4353, 653)))
    renderer.add_imaginary_platform(JumpCrystal((5105, 375)))
    renderer.add_imaginary_platform(JumpCrystal((5961, 621)))
    renderer.add_imaginary_platform(JumpCrystal((4732, 317)))
    renderer.add_platform((0, h - 255), 2285, 255)
    renderer.add_platform((0, h - 170), monologue.get_size()[0], 170)
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
    renderer.add_imaginary_platform(HeightPortal((0, 0), None, None, "arena"))
    renderer.add_imaginary_platform(HeightPortal((monologue.get_size()[0] - 80, 0), None, None, "level_1", True))


def init_arena():
    global renderer
    global player
    player.max_y = None
    renderer.clear_platforms()
    renderer.clear_children()
    renderer.clear_bullets()
    player.x = 4000 - 200
    player.orig_x = player.x
    player.orig_y = player.y
    renderer.orig_background_progressionx = 2094
    renderer.background_progressionx = 2094
    renderer.replace_bg(arena)
    renderer.add_child(framerate_text)
    renderer.add_imaginary_platform(HeightPortal((4000 - 80, 0), None, None, "monologue", True))
    renderer.add_platform((0, h - 255), 4000, 255, (0, 255, 0))
    renderer.add_platform((1000, h / 2 - 100), 700, 50, (0, 255, 0))
    renderer.add_platform((0, h / 2 - 100), 500, 50, (241, 145, 155))
    renderer.add_imaginary_platform(JumpCrystal((700, h / 2 - 150)))
    renderer.add_platform((800, h / 2 - 400), 1000, 50, (0, 255, 0))
    renderer.add_platform((3000, h / 2 - 300), 600, 50, (0, 0, 255))
    renderer.add_platform((2500, h / 2 - 200), 400, 50, (255, 0, 0))
    renderer.add_imaginary_platform(JumpCrystal((2300, h / 2 - 150)))
    renderer.add_child(JumpPad((2000, h - 255 - 40), 115, 40, 1.7))
    renderer.add_imaginary_platform(JumpCrystal((1900, h / 2 - 350)))
    renderer.add_child(JumpPad((500, h - 255 - 40), 115, 40, 1.7))
    renderer.add_imaginary_platform(StaminaCrystal((3000, h - 255 - 100)))
    renderer.add_imaginary_platform(StaminaCrystal((1200, h - 255 - 100)))
    renderer.add_imaginary_platform(StaminaCrystal((1000, 140 - 100)))
    renderer.add_imaginary_platform(HealthCrystal((300, 440 - 100)))
    renderer.add_imaginary_platform(HealthCrystal((3200, 240 - 100)))
    renderer.add_imaginary_platform(HealthCrystal((1200, 440 - 100)))


def init_settings():
    renderer.add_child(volume_slider)
    renderer.add_child(quit_settings_button)


def init_gameover():
    global renderer
    global gameover
    global player
    global choice
    player = Player(f"resources\\sprites\\{choice}_Thin\\{choice}_idle.png",
                    f"resources\\sprites\\{choice}_Thin\\{choice}_run.png",
                    f"resources\\sprites\\{choice}_Thin\\{choice}_jump.png",
                    f"resources\\sprites\\{choice}_Thin\\{choice}_death.png",
                    f"resources\\sprites\\{choice}_Thin\\{choice}_dash.png",
                    32, 32, 48, (w / 2, h - 500), 500)
    gameover = Image(0, 0, "resources\\images\\death_screens\\death_screen" + str(random.randint(0, 2)) + ".png")
    renderer.__init__(screen, gameover)
    renderer.add_child(gameover_button)
    renderer.background_progressionx = 0
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

            if renderer.game_started and event.button == 4 and renderer.world != "monologue":
                weapon_index = (weapon_index + 1) % len(guns)
                player.change_weapon(guns[weapon_index])
            if renderer.game_started and event.button == 5 and renderer.world != "monologue":
                weapon_index = (weapon_index - 1) % len(guns)
                player.change_weapon(guns[weapon_index])

            if renderer.background == title and not renderer.background.is_fading_out and not renderer.has_child(
                    waiting_for_players):
                if quit_btn.is_clicked(pygame.mouse.get_pos()):
                    running = False
                elif connect_btn.is_clicked(pygame.mouse.get_pos()):
                    renderer.remove_child(connect_btn)
                    renderer.remove_child(settings_btn)
                    renderer.remove_child(quit_btn)
                    renderer.remove_child(ip_input)
                    renderer.remove_child(port_input)
                    renderer.remove_child(name_input)
                    connect(ip_input.text, int(port_input.text),
                            random_name() if name_input.text == "NAME:" or name_input.text == "" else name_input.text)
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
                if player.weapon == Weapons.MACHINE_GUN:
                    player.shoot_cooldown = player.machine_gun_start_cooldown
        if renderer.game_started:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.dash(renderer.dt)
                    if not player.is_temp_dead:
                        cl.send_dash()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.move("stay")
                if event.key == pygame.K_d:
                    player.move("stay")
            if event.type == pygame.MOUSEBUTTONUP and not player.is_temp_dead and event.button == 1 and player.shoot_timer == -1:
                m_pos = pygame.mouse.get_pos()
                x_pos = (player.x - (renderer.background.get_size()[0] - WIDTH)) if player.x > \
                                                                                    renderer.background.get_size()[
                                                                                        0] - WIDTH / 2 else (
                    player.x if player.x < WIDTH / 2 else WIDTH / 2)
                y_pos = player.y if player.y < HEIGHT / 2 - player.image.get_height() / 2 else HEIGHT / 2 - player.image.get_height() / 2
                if player.y > renderer.background.get_size()[1] - HEIGHT / 2 - player.image.get_height() / 2:
                    y_pos = player.y - (renderer.background.get_size()[1] - HEIGHT)
                if player.weapon == Weapons.GUN:
                    renderer.add_bullet(cl, player.x + player.image.get_width() / 2,
                                        player.y + player.image.get_height() / 2, x_pos + player.image.get_width() / 2,
                                        y_pos + player.image.get_height() / 2, m_pos[0],
                                        m_pos[1], 10, 700)
                    player.shoot_timer = 0
                elif player.weapon == Weapons.SHOTGUN:
                    for i in range(-1, 2):
                        renderer.add_bullet(cl, player.x + player.image.get_width() / 2,
                                            player.y + player.image.get_height() / 2,
                                            x_pos + player.image.get_width() / 2,
                                            y_pos + player.image.get_height() / 2, m_pos[0],
                                            m_pos[1] + i * 30, 10, 700, 500, 4)
                    player.shoot_timer = 0

    if renderer.game_started and renderer.background == title:
        player = renderer.get_player()
        init_monologue()

    if pygame.mouse.get_pressed(3)[0]:
        if renderer.background == settings:
            volume_slider.update(pygame.mouse.get_pos())
            mixer.set_volume(volume_slider.value)
        if renderer.game_started:
            m_pos = pygame.mouse.get_pos()
            x_pos = (player.x - (renderer.background.get_size()[0] - WIDTH)) if player.x > \
                                                                                renderer.background.get_size()[
                                                                                    0] - WIDTH / 2 else (
                player.x if player.x < WIDTH / 2 else WIDTH / 2)
            y_pos = player.y if player.y < HEIGHT / 2 - player.image.get_height() / 2 else HEIGHT / 2 - player.image.get_height() / 2
            if player.y > renderer.background.get_size()[1] - HEIGHT / 2 - player.image.get_height() / 2:
                y_pos = player.y - (renderer.background.get_size()[1] - HEIGHT)
            if player.weapon == Weapons.FIRE_WALL_FLAMETHROWER:
                for i in range(50):
                    randy = random.randint(-10, 10)
                    randx = random.randint(0, 20)
                    rand_color = random.choice([(random.randint(100, 255), 0, 0), (255, 128, 0), (242, 186, 73)])
                    renderer.add_bullet(cl, player.x + player.image.get_width() / 2 + randx,
                                        player.y + player.image.get_height() / 2 + randy,
                                        x_pos + player.image.get_width() / 2, y_pos + player.image.get_height() / 1,
                                        m_pos[0], m_pos[1] + randy, 2, 100, 120, 0.01, rand_color)
            elif player.weapon == Weapons.SYN_UZI and player.shoot_timer == -1:
                renderer.add_bullet(cl, player.x + player.image.get_width() / 2,
                                    player.y + player.image.get_height() / 2, x_pos + player.image.get_width() / 2,
                                    y_pos + player.image.get_height() / 2, m_pos[0], m_pos[1], 5, 1000, 600, 1.45)
                player.shoot_timer = 0
            elif player.weapon == Weapons.MACHINE_GUN and player.shoot_timer == -1:
                for i in range(10):
                    renderer.add_bullet(cl, player.x + player.image.get_width() / 2,
                                        player.y + player.image.get_height() / 2, x_pos + player.image.get_width() / 2,
                                        y_pos + player.image.get_height() / 2, m_pos[0],
                                        m_pos[1] + random.randint(-20, 20), 5, 600, 300, 0.1)
                player.shoot_cooldown -= renderer.dt * player.machine_gun_cooldown_reduction_multiplier
                if player.shoot_cooldown < 0.5:
                    player.shoot_cooldown = 0.5
                player.shoot_timer = 0
            elif player.weapon == Weapons.LASER:
                d = None
                for i in range(100):
                    dx = m_pos[0] - (x_pos + player.image.get_width() / 2)
                    dy = m_pos[1] - (y_pos + player.image.get_height() / 2)

                    direction = pygame.math.Vector2(dx, dy).normalize()
                    d = direction
                    renderer.add_bullet(cl, player.x + player.image.get_width() / 2 + direction[0] * i * 5,
                                        player.y + player.image.get_height() / 2 + direction[1] * i * 5,
                                        x_pos + player.image.get_width() / 2, y_pos + player.image.get_height() / 2,
                                        m_pos[0], m_pos[1], 10, 1000, 10, 0, (255, 0, 0))

                renderer.add_bullet(cl, player.x + player.image.get_width() / 2 + d[0] * 105 * 5,
                                    player.y + player.image.get_height() / 2 + d[1] * 105 * 5,
                                    x_pos + player.image.get_width() / 2, y_pos + player.image.get_height() / 2,
                                    m_pos[0], m_pos[1], 10, 1000, 10, 0.3, (220, 0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        player = Player(f"resources\\sprites\\{choice}_Thin\\{choice}_idle.png",
                        f"resources\\sprites\\{choice}_Thin\\{choice}_run.png",
                        f"resources\\sprites\\{choice}_Thin\\{choice}_jump.png",
                        f"resources\\sprites\\{choice}_Thin\\{choice}_death.png",
                        f"resources\\sprites\\{choice}_Thin\\{choice}_dash.png", 32, 32, 48, (w / 2, h - 500), 500)
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
            player.jump(renderer.dt)
        if keys[pygame.K_s] and player.is_on_ladder:
            player.y += 500 * renderer.dt
        if WIDTH / 2 < player.x < renderer.background.get_size()[0] - WIDTH / 2:
            renderer.background_progressionx = player.x - WIDTH / 2
        if HEIGHT / 2 - player.image.get_height() / 2 < player.y < renderer.background.get_size()[
            1] - HEIGHT / 2 - player.image.get_height() / 2:
            renderer.background_progressiony = -(player.y - HEIGHT / 2 + player.image.get_height() / 2)
        elif HEIGHT / 2 - player.image.get_height() / 2 > player.y:
            renderer.background_progressiony = 0
        elif renderer.background.get_size()[1] - HEIGHT / 2 - player.image.get_height() / 2 < player.y:
            renderer.background_progressiony = -(renderer.background.get_size()[1] - HEIGHT)
        if (
                ((player.y + player.image.get_height() >= h - 170 and player.world == "monologue") or player.hp <= 0) and not player.is_temp_dead):
            player.is_temp_dead = True
            cl.send_dead()
        player.check_mouse_over_gun_slot(pygame.mouse.get_pos())

    if player.revived:
        player.revived = False
        renderer.background_progressionx = renderer.orig_background_progressionx
        cl.send_revived()

    if renderer.game_over is True:
        renderer.game_over = False
        renderer.game_started = False
        init_gameover()
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, w, h))
    prev_x = player.x
    prev_y = player.y
    renderer.update_all()
    renderer.render_all(pygame.mouse.get_pos())
    if renderer.game_started:
        player.draw_stats(screen, pix_font, renderer.background.get_size()[0], renderer.background.get_size()[1])
        if prev_x != player.x or prev_y != player.y:
            cl.send_player_coords(player.x, player.y)
            player_still = False
        elif prev_x == player.x and prev_y == player.y and not player_still:
            cl.send_player_coords(player.x, player.y)
            player_still = True
        if player.world != renderer.world:
            cl.send_world(player.world)
            if player.world == "arena":
                init_arena()
            if player.world == "monologue":
                init_monologue(False)
            if "level" in player.world:
                cl.send_level(player.world.split("_")[1])
            renderer.world = player.world

    if renderer.level_name is not None:
        renderer.render_level_name(screen)

    pygame.display.flip()
    framerate_text.set_text("FPS: " + str(int(clock.get_fps())))
    clock.tick(REFRESH_RATE)
    renderer.update_dt()

pygame.quit()
if cl is not None:
    cl.send_quit()
    cl.close()

# tile reflection, crystalize, dents
