import pygame
from pygame.locals import *
from utils import *

# pygame setup
pygame.init()
clock = pygame.time.Clock()

pix_font = pygame.font.Font('resources\\fonts\\yoster-island\\yoster.ttf', 25)

# debug assets
framerate_text = Text('FPS: ', pix_font, (255, 0, 0))

# title screen assets
title = Image("resources\\images\\title-screen.png", True)
w, h = title.get_size()
start_btn = Button(400, 100, "Start", (0, 0, 0), pix_font, (45, 115, 178), (8, 96, 168), (0, 0, 0), 0)
quit_btn = Button(400, 100, "Quit", (0, 0, 0), pix_font, (45, 115, 178), (8, 96, 168), (0, 0, 0), 0)

# game assets
started = False
monologue = Image("resources\\images\\monologue.png", True)
player = Player("resources\\sprites\\Cyborg\\Cyborg_idle.png", "resources\\sprites\\Cyborg\\Cyborg_run.png",
                "resources\\sprites\\Cyborg\\Cyborg_jump.png", 48, (w / 2, 0), 8)

screen = pygame.display.set_mode((w, h))
renderer = Renderer(screen, title)
renderer.add_child(start_btn, (w / 2 - 200, h / 2 + 100))
renderer.add_child(quit_btn, (w / 2 - 200, h / 2 + 220))
renderer.add_child(framerate_text, (50, 50))


def init_game():
    global started
    renderer.add_sprite(player)
    renderer.add_platform((0, h - 283), 2273, 283)
    renderer.add_platform((2406, h - 283), 131, 283)
    renderer.add_platform((2755, h - 283), 131, 283)
    renderer.add_platform((3250, h - 283), 131, 283)
    renderer.add_platform((3510, h - 498), 131, 498)
    renderer.add_platform((3916, h - 415), 283, 415)
    renderer.add_platform((4556, h - 282), 130, 282)
    renderer.add_platform((4805, h - 851), 131, 851)
    renderer.add_platform((5292, h - 545), 131, 545)
    renderer.add_platform((5649, h - 545), 131, 546)
    renderer.add_platform((6090, h - 251), 1910, 251)
    started = True


running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0
        if event.type == pygame.MOUSEBUTTONUP:
            if not started:
                if quit_btn.is_clicked(renderer.get_child_pos(quit_btn), pygame.mouse.get_pos()):
                    print("Bye bye")
                    running = False
                elif start_btn.is_clicked(renderer.get_child_pos(start_btn), pygame.mouse.get_pos()):
                    renderer.remove_child(start_btn)
                    renderer.remove_child(quit_btn)
                    renderer.fadeout_bg(monologue)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.move("stay")
            if event.key == pygame.K_d:
                player.move("stay")
    if renderer.background == monologue and not started:
        init_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    if started:
        if keys[pygame.K_a]:
            player.move("left")
        if keys[pygame.K_d]:
            player.move("right")
        if keys[pygame.K_w]:
            player.jump()

        if player.x > 1920 / 2:
            renderer.background_progression = player.x - 1920 / 2

    pygame.draw.rect(screen, (0, 0, 0), (0, 0, w, h))
    renderer.render_all(pygame.mouse.get_pos())
    pygame.display.flip()
    framerate_text.set_text("FPS: " + str(int(clock.get_fps())))
    clock.tick(60)

pygame.quit()
