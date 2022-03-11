import pygame


class Text:

    def __init__(self, text: str, font, color: tuple):
        self.text = text
        self.font = font
        self.color = color

    def render(self, surface, pos):
        text = self.font.render(self.text, True, self.color)
        surface.blit(text, (pos[0] - text.get_width() / 2, pos[1] - text.get_height() / 2))

    def set_text(self, text):
        self.text = text


class Button(Text):

    def __init__(self, w: int, h: int, text: str, text_color: tuple, font, bg_color: tuple, hover_color: tuple,
                 border_color: tuple, border_size: int):
        super().__init__(text, font, text_color)
        self.width = w
        self.height = h
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_size = border_size

    def render(self, surface: pygame.Surface, pos: tuple, hover=False):
        if hover:
            color = self.hover_color
        else:
            color = self.bg_color
        pygame.draw.rect(surface, color, pygame.Rect(pos[0], pos[1], self.width, self.height))
        if self.border_size != 0:
            pygame.draw.rect(surface, self.border_color, pygame.Rect(pos[0], pos[1], self.width, self.height),
                             self.border_size)
        super().render(surface,
                       (pos[0] + self.border_size + self.width / 2, pos[1] + self.border_size + self.height / 2))

    def is_clicked(self, pos: tuple, click_pos: tuple):
        return pos[0] <= click_pos[0] <= pos[0] + self.width and pos[1] <= click_pos[1] <= pos[1] + self.height


class Image:

    def __init__(self, image_path: str, fade_in: bool = False):
        self.image = pygame.image.load(image_path)
        self.image.set_alpha(255 if not fade_in else 0)
        self.is_fading_in = fade_in
        self.is_fading_out = False
        self.faded_out = False
        self.replace_image = None

    def render(self, surface: pygame.Surface, pos: tuple):
        if self.is_fading_in:
            if self.fade_in():
                self.is_fading_in = False
        elif self.is_fading_out:
            if self.fade_out():
                self.is_fading_out = False
                self.faded_out = True

        surface.blit(self.image, pos)

    def get_size(self):
        return self.image.get_size()

    def fade_in(self):
        self.image.set_alpha(self.image.get_alpha() + 15)
        return self.image.get_alpha() >= 255

    def fade_out(self):
        self.image.set_alpha(self.image.get_alpha() - 15)
        return self.image.get_alpha() <= 0


class Player:

    def __init__(self, idle_image_path: str, move_image_path: str, jump_image_path: str, sprite_width: int, pos: tuple,
                 speed: int):
        super().__init__()

        # Mechanics variables
        self.speed = 0
        self.xspeed = speed
        self.is_falling = False
        self.left = False
        self.animation_timer = 0
        self.x, self.y = pos

        self.y_velocity = 0
        self.gravity = 0.5
        self.jump_height = -15

        # Animation files
        self.idle_sheet = pygame.image.load(idle_image_path)
        self.move_sheet = pygame.image.load(move_image_path)
        self.jump_sheet = pygame.image.load(jump_image_path)
        self.current_image = self.idle_sheet
        self.image = pygame.Surface.subsurface(self.current_image, (0, 0, 48, 48))
        self.frame_width = sprite_width

        # Animation variables
        self.animation_framerate = 0.2

    def update(self):
        if self.is_falling:
            self.y_velocity += self.gravity
        self.x += self.speed
        self.y += self.y_velocity
        self.animation_timer += self.animation_framerate

    def move(self, direction: str):
        if direction == "left":
            if not self.left:
                self.idle_sheet = pygame.transform.flip(self.idle_sheet, True, False)
                self.move_sheet = pygame.transform.flip(self.move_sheet, True, False)
                self.jump_sheet = pygame.transform.flip(self.jump_sheet, True, False)
            self.current_image = self.move_sheet
            self.speed = -self.xspeed
            self.left = True
        elif direction == "right":
            if self.left:
                self.move_sheet = pygame.transform.flip(self.move_sheet, True, False)
                self.idle_sheet = pygame.transform.flip(self.idle_sheet, True, False)
                self.jump_sheet = pygame.transform.flip(self.jump_sheet, True, False)
                self.left = False
            self.current_image = self.move_sheet
            self.speed = self.xspeed
        else:
            self.current_image = self.idle_sheet
            self.speed = 0

    def jump(self):
        if not self.is_falling:
            self.current_image = self.jump_sheet
            self.y_velocity = self.jump_height
            self.is_falling = True

    def stop_fall(self, y: int):
        self.is_falling = False
        if self.current_image == self.jump_sheet:
            self.move("stay" if self.speed == 0 else ("left" if self.speed < 0 else "right"))
        self.y_velocity = 0
        self.y = y - self.image.get_height()

    def fall(self):
        self.is_falling = True

    def draw(self, surface: pygame.Surface):
        self.image = pygame.Surface.subsurface(self.current_image, (0 + 48 * (int(self.animation_timer) % int(self.current_image.get_width() / self.frame_width)), 0, self.frame_width, self.frame_width))
        self.image = pygame.transform.scale(self.image, (150, 150))
        surface.blit(self.image, (self.x if self.x < 1920/2 else 1920/2, self.y))


class Platform:

    def __init__(self, pos: tuple, width: int, height: int):
        self.x, self.y = pos
        self.width = width
        self.height = height

    def collide(self, player: Player):
        if player.x + player.image.get_width() >= self.x and player.x <= self.x + self.width:
            if player.y + player.image.get_height() >= self.y and player.y <= self.y + self.height:
                return True
        return False


class SpriteGroup:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.sprites = []

    def add(self, sprite):
        self.sprites.append(sprite)

    def update(self):
        for sprite in self.sprites:
            sprite.update()

    def draw(self):
        for sprite in self.sprites:
            sprite.draw(self.surface)

    def remove(self, sprite):
        self.sprites.remove(sprite)

    def empty(self):
        self.sprites.clear()

    def get_sprites(self):
        return self.sprites


class Renderer:

    def __init__(self, screen: pygame.Surface, background_image: Image):
        self.screen = screen
        self.sprites = SpriteGroup(self.screen)
        self.background = background_image
        self.background_progression = 0
        self.children = []
        self.platforms = []

    def render_all(self, mouse_pos: tuple):

        self.background.render(self.screen, (-self.background_progression, 0))
        if self.background.faded_out:
            self.background = self.background.replace_image

        for child, pos in self.children:

            if isinstance(child, Button):
                child.render(self.screen, pos,
                             pos[0] < mouse_pos[0] < pos[0] + child.width and pos[1] < mouse_pos[1] < pos[
                                 1] + child.height)
            else:
                child.render(self.screen, pos)

        for sprite in self.sprites.get_sprites():
            found = False
            for platform in self.platforms:
                if platform.collide(sprite) and sprite.is_falling and sprite.y_velocity > 0 and abs(sprite.y + sprite.image.get_height() - platform.y) < 20:
                    sprite.stop_fall(platform.y)
                    found = True
                    break
            if not found:
                sprite.fall()

        self.sprites.update()
        self.sprites.draw()

    def add_child(self, child, pos: tuple = (0, 0)):
        self.children.append((child, pos))

    def remove_child(self, child):
        for i in range(len(self.children)):
            if self.children[i][0] == child:
                return self.children.pop(i)

    def fadeout_bg(self, replace_with: Image):
        self.background.is_fading_out = True
        self.background.replace_image = replace_with

    def clear_children(self):
        self.children = []

    def get_child_pos(self, child):
        for i in range(len(self.children)):
            if self.children[i][0] == child:
                return self.children[i][1]

    def add_sprite(self, sprite):
        self.sprites.add(sprite)

    def remove_sprite(self, sprite):
        self.sprites.remove(sprite)

    def clear_sprites(self):
        self.sprites.empty()

    def add_platform(self, pos: tuple, width: int, height: int):
        self.platforms.append(Platform(pos, width, height))

    def clear_platforms(self):
        self.platforms.clear()
