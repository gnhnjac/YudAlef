import random

import pygame
from enum import Enum

# Notes to self:
# - Add Dori's idea to add an electricity bar which always decreases and is only replenished by killing enemies and gaining orbs
# - Add a way to make the player invincible for a short time after being hit
# - Add armor
# - Add items + server chests
# - Add end level routers
# - Add random level generation
# - Add player death animation and add fading animation when next level is going to be loaded and fade in when level is loaded
# - Add character selection in settings
# - Add weapons + weapon upgrades
# - Add consumable items

class Slider:
    def __init__(self, x, y, w, h, min_value, max_value, value, text, font, text_color, bg_color,fg_color, border_color, border_width):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.border_color = border_color
        self.border_width = border_width

    def render(self, surface):
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, self.border_color, (self.x, self.y, self.w, self.h), self.border_width)
        pygame.draw.rect(surface, self.fg_color, (self.x, self.y, self.w * (self.value - self.min_value) / (self.max_value - self.min_value), self.h))
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = (self.x + self.w/2, self.y + self.h/2)
        surface.blit(text, text_rect)


    def update(self, mouse_pos):

        if self.x < mouse_pos[0] < self.x + self.w and self.y < mouse_pos[1] < self.y + self.h:
            self.value = self.min_value + (self.max_value - self.min_value) * (mouse_pos[0] - self.x) / self.w
            if self.value < self.min_value:
                self.value = self.min_value
            if self.value > self.max_value:
                self.value = self.max_value

class Items(Enum):
    # Powerups

    COPPER_WIRE = 0  # Increase speed but decrease armor
    SILVER_WIRE = 1  # Increase armor but decrease speed
    GOLD_WIRE = 2  # Increase armor drastically but decrease speed drastically
    SYN_ATTACK = 3  # Shoot out seeking syn requests upon taking damage
    ANTI_VIRUS_SYSTEM = 5  # Decreases damage taken from viruses
    FIRE_WALL = 6  # Deploy a fire wall that blocks incoming attacks and damages enemies
    NEW_CPU = 7  # Increases health, armor and stamina by 10%
    MORE_RAM = 8  # Increases jump height
    BETTER_INTERNET = 9  # Increases attack speed
    BETTER_BANDWIDTH = 10  # Increases attack damage
    SHIELDED_ETHERNET_CABLE = 11  # Automatically blocks incoming attacks in a 1 second period
    GPU_CORE = 12  # Increases stamina regeneration speed
    FASTER_MEMORY = 13  # Increases stamina
    BIGGER_POWER_SUPPLY = 14  # Increases electricity bar capacity

    # Upgrade weapons
    PC_PART = 14  # Used to upgrade basic weapons
    HEAT_RESISTANT_PC_PART = 15  # used to upgrae weapons that heat up
    ELITE_PC_PART = 16  # Used to upgrade elite weapons


class Weapons(Enum):
    # Basic weapons
    GUN = 0  # Just a basic gun
    UDP_PACKET_MISSILE = 1  # Shoots out UDP packets that seek out enemies, has a low chance of hitting
    SYN_PACKET_MISSILE = 2  # Shoots out SYN packets that seek out enemies, has a very low chance of hitting but deals devestating damage
    SYN_ACK_CANNON = 3  # Deals low damage and has a short cooldown but has a high chance of hitting
    UZI = 4  # Deals medium damage and has a very low cooldown but has a very low chance of hitting
    SHOTGUN = 5  # Deals high damage and has a medium cooldown but has a medium chance of hitting

    # cooldown weapons (heat up)
    MACHINE_GUN = 6  # Deals high damage and has a long cooldown but has a very low chance of hitting
    FLAMETHROWER = 7  # Deals high damage and has a very long cooldown but has a very high chance of hitting
    LASER = 8  # Deals high damage and has a very long cooldown but has a very high chance of hitting

    # legendary elite super mega cool weapons
    YOSSIZ_THE_DEVASTATOR = 9  # Deals immensely high damage in a spread attack and has a short cooldown, has a good chance of hitting
    THE_LIGHTNING_BOLT = 10  # Deals incredibly high damage and has a medium cooldown, has a good chance of hitting
    SYN_ACK_LASER = 11  # Deals low damage, has a very low cooldown, 100% chance of hitting
    CYBER_CALL_OF_THE_BLACK_KNIGHT = 13  # Deals immense damage, has no cooldown, 100% chance of hitting, calls for help.
    DOOM = 14  # destruction.


class Consumables(Enum):
    JUMP_PAD_POTION = 0  # Restores used jump pads
    HEALTH_POTION = 1  # Restores health
    ARMOR_POTION = 2  # Restores armor
    STAMINA_POTION = 3  # Restores stamina


class Text:

    def __init__(self, x, y, text: str, font, color: tuple):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color

    def render(self, surface,pos=None):
        if pos is None:
            pos = (self.x, self.y)
        text = self.font.render(self.text, True, self.color)
        surface.blit(text, (pos[0] - text.get_width() / 2, pos[1] - text.get_height() / 2))

    def set_text(self, text):
        self.text = text


class Button(Text):

    def __init__(self, x, y,w: int, h: int, text: str, text_color: tuple, font, bg_color: tuple, hover_color: tuple,
                 border_color: tuple, border_size: int):
        super().__init__(x, y, text, font, text_color)
        self.width = w
        self.height = h
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_size = border_size

    def render(self, surface: pygame.Surface, hover=False):
        if hover:
            color = self.hover_color
        else:
            color = self.bg_color
        pygame.draw.rect(surface, color, pygame.Rect(self.x, self.y, self.width, self.height))
        if self.border_size != 0:
            pygame.draw.rect(surface, self.border_color, pygame.Rect(self.x, self.y, self.width, self.height),
                             self.border_size)
        super().render(surface,
                       (self.x + self.border_size + self.width / 2, self.y + self.border_size + self.height / 2))

    def is_clicked(self, click_pos: tuple):
        return self.x <= click_pos[0] <= self.x + self.width and self.y <= click_pos[1] <= self.y + self.height


class Image:

    def __init__(self, x, y,image_path: str, fade_in: bool = False):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.image.set_alpha(255 if not fade_in else 0)
        self.is_fading_in = fade_in
        self.is_fading_out = False
        self.faded_out = False
        self.replace_image = None

    def render(self, surface: pygame.Surface):
        if self.is_fading_in:
            if self.fade_in():
                self.is_fading_in = False
        elif self.is_fading_out:
            if self.fade_out():
                self.is_fading_out = False
                self.faded_out = True

        surface.blit(self.image, (self.x, self.y))

    def get_size(self):
        return self.image.get_size()

    def fade_in(self):
        if self.image.get_alpha() is None:
            return True
        self.image.set_alpha(self.image.get_alpha() + 15)
        return True if self.image.get_alpha() is None else self.image.get_alpha() >= 255

    def fade_out(self):
        if self.image.get_alpha() is None:
            return True
        self.image.set_alpha(self.image.get_alpha() - 15)
        return self.image.get_alpha() <= 0


class Player:

    def __init__(self, idle_image_path: str, move_image_path: str, jump_image_path: str, sprite_width: int,
                 side_padding: int, top_padding: int, pos: tuple,
                 speed: int):
        super().__init__()

        # Mechanics variables
        self.speed = 0
        self.xspeed = speed
        self.is_falling = False
        self.left = False
        self.animation_timer = 0
        self.x, self.y = pos
        self.side_padding = side_padding
        self.top_padding = top_padding

        self.y_velocity = 0
        self.gravity = 0.5
        self.jump_height = -15
        self.jump_multiplier = 1

        # Game variables
        self.max_health = 100
        self.hp = self.max_health
        self.max_stamina = 110
        self.stamina = self.max_stamina
        self.consumables = []
        self.items = []
        self.jump_boost = False

        # Animation files
        self.idle_sheet = pygame.image.load(idle_image_path)
        self.move_sheet = pygame.image.load(move_image_path)
        self.jump_sheet = pygame.image.load(jump_image_path)
        self.current_image = self.idle_sheet
        self.image = pygame.Surface.subsurface(self.current_image, (0, 0, sprite_width, sprite_width))
        self.frame_width = sprite_width

        # Animation variables
        self.animation_framerate = 0.2

    def update(self):
        if self.is_falling:
            self.y_velocity += self.gravity
        self.x += self.speed
        if self.speed != 0 and self.stamina - 0.1 > 0:
            self.stamina -= 0.1
        elif self.speed == 0 and self.stamina < self.max_stamina:
            self.stamina += 0.5
            if self.stamina > self.max_stamina:
                self.stamina = self.max_stamina
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
        if not self.is_falling and self.stamina - 10 > 0:
            self.current_image = self.jump_sheet
            self.y_velocity = self.jump_height * self.jump_multiplier
            self.jump_multiplier = 1
            self.jump_boost = False
            self.is_falling = True
            self.stamina -= 10

    def stop_fall(self, y: int):
        self.is_falling = False
        if self.current_image == self.jump_sheet:
            self.move("stay" if self.speed == 0 else ("left" if self.speed < 0 else "right"))
        self.y_velocity = 0
        self.y = y - self.image.get_height()

    def fall(self):
        self.is_falling = True

    def dash(self):
        if self.stamina - 10 > 0:
            self.stamina -= 10
            self.x += self.speed * 2.5

    def draw(self, surface: pygame.Surface):
        if self.animation_timer >= int(self.current_image.get_width() / self.frame_width):
            self.animation_timer = 0

        self.image = pygame.Surface.subsurface(self.current_image, (
            0 + self.frame_width * int(self.animation_timer),
            0,
            self.frame_width, self.current_image.get_height()))
        self.image = pygame.transform.scale(self.image,
                                            (150, int(150 * self.image.get_height() / self.image.get_width())))
        surface.blit(self.image, (self.x if self.x < 1920 / 2 else 1920 / 2, self.y))

    def draw_stats(self, surface: pygame.Surface, font: pygame.font.Font):
        pygame.draw.rect(surface, (150, 150, 150), (surface.get_width() - 550, 0, 550, 100))
        hp_text = font.render(f"HP:", True, (255, 0, 0))
        stamina_text = font.render(f"Stamina:", True, (0, 0, 255))
        surface.blit(hp_text, (surface.get_width() - hp_text.get_width() - 420, 10))
        surface.blit(stamina_text, (surface.get_width() - stamina_text.get_width() - 420, 40))
        pygame.draw.rect(surface, (255, 0, 0),
                         (surface.get_width() - 410, 10, int(self.hp * 400 / self.max_health), 20))
        pygame.draw.rect(surface, (0, 0, 255),
                         (surface.get_width() - 410, 40, int(self.stamina * 400 / self.max_stamina), 20))

        if self.jump_boost:
            # surface.blit(pygame.image.load('resources/icons/jump_boost.png'), (surface.get_width() - 410, 70)) # below stamina
            surface.blit(pygame.transform.scale(pygame.image.load('resources/icons/jump_boost.png'), (60, 60)),
                         ((self.x if self.x < 1920 / 2 else 1920 / 2) + self.side_padding, self.y))  # above player


class Platform:

    def __init__(self, pos: tuple, width: int, height: int, color: tuple = None):
        self.x, self.y = pos
        self.width = width
        self.height = height
        self.color = color

    def collide(self, player: Player):
        if player.x + player.side_padding <= self.x + self.width and player.x + player.image.get_width() - player.side_padding >= self.x:
            if player.y + player.image.get_height() >= self.y and player.y <= self.y + self.height:
                return True
        return False

    def draw(self, surface: pygame.Surface, background_progression: int):
        if self.color is not None and self.x + self.width - background_progression > 0:
            pygame.draw.rect(surface, self.color, (self.x - background_progression, self.y, self.width, self.height))


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


class JumpPad(Platform):
    def __init__(self, pos: tuple, width: int, height: int, jump_multiplier: float = 1.5, is_finite: bool = False):
        super().__init__(pos, width, height)
        self.jump_multiplier = jump_multiplier
        self.used = False
        self.is_finite = is_finite

    def render(self, surface: pygame.Surface, background_progression: int):
        if self.x + self.width - background_progression > 0 and (
                (self.is_finite and not self.used) or not self.is_finite):
            surface.blit(
                pygame.transform.scale(pygame.image.load("resources/special/jump_pad_crystalized.png" if (
                        not self.used or not self.is_finite) else 'resources/special/used_pad.png'),
                                       (self.width, self.height)),
                (self.x - background_progression, self.y))


class Renderer:

    def __init__(self, screen: pygame.Surface, background_image: Image):
        self.screen = screen
        self.sprites = SpriteGroup(self.screen)
        self.background = background_image
        self.background_progression = 0
        self.children = []
        self.platforms = []

    def render_all(self, mouse_pos: tuple):
        self.background.x = -self.background_progression
        self.background.render(self.screen)
        if self.background.faded_out:
            self.background.faded_out = False
            self.background.is_fading_out = False
            self.background.is_fading_in = True
            self.background = self.background.replace_image
            self.background.replace_image = None
        for platform in self.platforms:
            platform.draw(self.screen, self.background_progression)
        for child in self.children:

            if isinstance(child, Button):
                child.render(self.screen,
                             child.x < mouse_pos[0] < child.x + child.width and child.y < mouse_pos[1] < child.y + child.height)
            elif isinstance(child, JumpPad):
                child.render(self.screen, self.background_progression)
            else:
                child.render(self.screen)
        self.sprites.draw()

    def update_all(self):
        self.sprites.update()

        for sprite in self.sprites.get_sprites():
            found_bot = False
            for platform in self.platforms:
                if platform.collide(sprite) and sprite.is_falling and sprite.y_velocity > 0 and abs(
                        sprite.y + sprite.image.get_height() - platform.y) < 20:
                    sprite.stop_fall(platform.y)
                    found_bot = True
                    if isinstance(platform, JumpPad):
                        sprite.jump_multiplier = platform.jump_multiplier
                        sprite.jump_boost = True
                        platform.used = True
                if platform.collide(
                        sprite) and platform.y < sprite.y + sprite.image.get_height() < platform.y + platform.height and sprite.speed < 0:
                    sprite.x = platform.x + platform.width
                if platform.collide(
                        sprite) and platform.y < sprite.y + sprite.image.get_height() < platform.y + platform.height and sprite.speed > 0:
                    sprite.x = platform.x - sprite.image.get_width()
                if platform.collide(
                        sprite) and platform.y + platform.height > sprite.y + sprite.top_padding and sprite.y_velocity < 0:
                    sprite.y_velocity = 0

            if not found_bot:
                sprite.fall()

    def add_child(self, child):
        if isinstance(child,JumpPad):
            self.platforms.append(child)
        self.children.append(child)

    def remove_child(self, child):
        return self.children.remove(child)

    def fadeout_bg(self, replace_with: Image):
        self.background.is_fading_out = True
        self.background.replace_image = replace_with

    def clear_children(self):
        self.children = []

    def add_sprite(self, sprite):
        self.sprites.add(sprite)

    def remove_sprite(self, sprite):
        self.sprites.remove(sprite)

    def clear_sprites(self):
        self.sprites.empty()

    def add_platform(self, pos: tuple, width: int, height: int, color: tuple = None):
        self.platforms.append(Platform(pos, width, height, color))

    def clear_platforms(self):
        self.platforms.clear()


class MusicManager:

    def __init__(self, music_list: list, music_volume: float = 1.0):
        self.music_list = music_list
        self.music_playing = False
        self.music_index = random.randint(0, len(self.music_list) - 1)
        pygame.mixer.init()
        pygame.mixer.music.set_volume(music_volume)

    def start_music(self):
        pygame.mixer.music.load(self.music_list[self.music_index])
        pygame.mixer.music.play()
        self.music_playing = True

    def start_specific_music(self, music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()
        self.music_playing = True

    def next_music(self):
        self.music_index += 1
        if self.music_index >= len(self.music_list):
            self.music_index = 0
        self.start_music()

    def prev_music(self):
        self.music_index -= 1
        if self.music_index < 0:
            self.music_index = len(self.music_list) - 1
        self.start_music()

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False

    def pause_music(self):
        pygame.mixer.music.pause()
        self.music_playing = False

    def unpause_music(self):
        pygame.mixer.music.unpause()
        self.music_playing = True

    def update(self):
        if not self.music_playing:
            self.next_music()

    def set_volume(self, volume: float):
        pygame.mixer.music.set_volume(volume)