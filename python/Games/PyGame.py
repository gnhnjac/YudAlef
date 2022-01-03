import pygame

pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("עבריתון")

width = 100
height = 80

x = 80
y = 500 - height

velocity = 5

jump = False

jumpCount = 10

run = True
while run:

    pygame.time.delay(100)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and not x == 0:
        x -= velocity

    if keys[pygame.K_RIGHT] and not x == 500 - width:
        x += velocity

    if not jump:
        if keys[pygame.K_SPACE]:
            jump = True
    else:
        if jumpCount >= -10:
            negativeJump = 1
            if jumpCount < 0:
                negativeJump = -1

            y -= (jumpCount ** 2) / 2 * negativeJump
            jumpCount -= 1
        else:
            jump = False
            jumpCount = 10

    win.fill([0, 0, 0])
    pygame.draw.rect(win, (255, 255, 255), (x, y, width, height))

    pygame.display.update()

pygame.quit()