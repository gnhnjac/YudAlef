import pickle
import random
import pygame
from enum import Enum
from configparser import ConfigParser

# apply configs
config = ConfigParser()
config.read('conf.ini')
WIDTH = int(config.get('settings', 'WINDOW_WIDTH'))
HEIGHT = int(config.get('settings', 'WINDOW_HEIGHT'))
MAX_STAMINA = int(config.get('settings', 'MAX_STAMINA'))
MAX_HEALTH = int(config.get('settings', "MAX_HEALTH"))
ACTIVE_HITBOXES = config.getboolean('settings', 'ACTIVE_HITBOXES')
INFINITE_JUMP_DASH = config.getboolean('settings', 'INFINITE_JUMP_DASH')
# Global Assets
# Fonts
PIX_FONT = None  # pygame.font.Font('resources\\fonts\\yoster-island\\yoster.ttf', 25)
PIX_FONT = None  # pygame.font.Font('resources\\fonts\\yoster-island\\yoster.ttf', 25)
SMALL_ARIEL = None

# Buildings
JUMP_PAD = None  # pygame.image.load("resources/special/jump_pad_crystalized.png").convert_alpha()
JUMP_PAD_USED = None  # pygame.image.load('resources/special/used_pad.png').convert_alpha()

# Icons
JUMP_BOOST_ICON = None  # pygame.image.load('resources/icons/jump_boost.png').convert_alpha()

# Backgrounds
PARALLAX = None
OVERGROWN = None
MIRAGE = None


# Notes to self:
# - Add ladder support
# - Add a way to make the player invincible for a short time after being hit
# - Add armor
# - Add items + server chests
# - Add weapons + weapon upgrades
# - Add consumable items
# - Add isHoverPlatform to platform to make it not colldie you in sides and bottom
# - Map types: forest, desert, inferno, ice, network, space, cave, castle, city, etc.

def random_name():
    with open('names.txt', 'r') as f:
        names = f.read().splitlines()
    return random.choice(names)


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class HealthCoord(Coordinate):
    def __init__(self, x, y):
        super().__init__(x, y)


class StaminaCoord(Coordinate):
    def __init__(self, x, y):
        super().__init__(x, y)


class JumpCoord(Coordinate):
    def __init__(self, x, y):
        super().__init__(x, y)


class JumpPadCoord(Coordinate):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.jump_strength = 2.5
        self.width = 115
        self.height = 40


class Checkbox:
    def __init__(self, surface, x, y, color, caption, outline_color, check_color, font, font_color,
                 text_offset=(45, 15)):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fc = font_color
        self.to = text_offset
        self.font = font

        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 40, 40)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = False

    def _draw_button_text(self):
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + 12 / 2 - h / 2 +
                         self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render(self, surface):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 20, self.y + 20), 16)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    def update_checkbox(self):
        self.click = True
        self._update()


class Slider:
    def __init__(self, x, y, w, h, min_value, max_value, value, text, font, text_color, bg_color, fg_color,
                 border_color, border_width):
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
        pygame.draw.rect(surface, self.fg_color, (
            self.x, self.y, self.w * (self.value - self.min_value) / (self.max_value - self.min_value), self.h))
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = (self.x + self.w / 2, self.y + self.h / 2)
        surface.blit(text, text_rect)

    def update(self, mouse_pos):

        if self.x < mouse_pos[0] < self.x + self.w and self.y < mouse_pos[1] < self.y + self.h:
            self.value = self.min_value + (self.max_value - self.min_value) * (mouse_pos[0] - self.x) / self.w
            if self.value < self.min_value:
                self.value = self.min_value
            if self.value > self.max_value:
                self.value = self.max_value


class InputBox:
    def __init__(self, x, y, w, h, inactive, active, font, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = inactive
        self.inactive = inactive
        self.active = active
        self.text = text
        self.font = font
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.active if self.active else self.inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def render(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Items(Enum):
    # Powerups
    COPPER_WIRE = 0  # Increase speed but decrease health
    SILVER_WIRE = 1  # Increase health but decrease speed
    GOLD_WIRE = 2  # Increase armor drastically but decrease speed drastically
    ANTI_VIRUS_SYSTEM = 5  # Decreases damage taken from viruses
    NEW_CPU = 7  # Increases health, armor and stamina by 10%
    MORE_RAM = 8  # Increases jump height
    BETTER_INTERNET = 9  # Increases attack speed
    BETTER_BANDWIDTH = 10  # Increases attack damage
    SHIELDED_ETHERNET_CABLE = 11  # Automatically blocks incoming attacks in a 1 second period
    GPU_CORE = 12  # Increases stamina regeneration speed
    FASTER_MEMORY = 13  # Increases stamina
    BIGGER_POWER_SUPPLY = 14  # Increases electricity bar capacity

    # Legendary powerups
    INFINITE_MEMORY = 15  # Infinite stamina
    FIRE_WALL = 6  # Deploy a fire wall that blocks incoming attacks and damages enemies
    SYN_ATTACK = 3  # Shoot out seeking syn requests upon taking damage
    JETPACK = 16  # obvious. press shift space to activate.

    # Upgrade weapons
    PC_PART = 14  # Used to upgrade basic weapons
    HEAT_RESISTANT_PC_PART = 15  # used to upgrae weapons that heat up
    ELITE_PC_PART = 16  # Used to upgrade elite weapons


class Weapons(Enum):
    # Basic weapons
    GUN = "Basic gun"  # Just a basic gun
    UDP_PACKET_MISSILE = 1  # Shoots out UDP packets that seek out enemies, has a low chance of hitting
    SYN_ACK_CANNON = 3  # Deals low damage and has a short cooldown but has a high chance of hitting
    SYN_UZI = 4  # Deals medium damage and has a very low cooldown but has a very low chance of hitting
    SHOTGUN = 5  # Deals high damage and has a medium cooldown but has a medium chance of hitting

    # cooldown weapons (heat up)
    MACHINE_GUN = 6  # Deals high damage and has a long cooldown but has a very low chance of hitting
    FIRE_WALL_FLAMETHROWER = 7  # Deals high damage and has a very long cooldown but has a very high chance of hitting
    LASER = 8  # Deals high damage and has a very long cooldown but has a very high chance of hitting

    # legendary elite super mega cool weapons
    YOSSIZ_THE_DEVASTATOR = 9  # Deals immensely high damage in a spread attack and has a short cooldown, has a good chance of hitting
    THE_LIGHTNING_BOLT = 10  # Deals incredibly high damage and has a medium cooldown, has a good chance of hitting
    SYN_ACK_LASER = 11  # Deals low damage, has a very low cooldown, 100% chance of hitting
    CYBER_CALL_OF_THE_BLACK_KNIGHT = 13  # Deals immense damage, has no cooldown, 100% chance of hitting, calls for help.
    DOOM = 14  # destruction.


def get_weapon_name(weapon):
    weapon_name_dict = {Weapons.GUN: "Basic gun", Weapons.UDP_PACKET_MISSILE: "UDP packet missile",
                        Weapons.SYN_ACK_CANNON: "SYN/ACK cannon",
                        Weapons.SYN_UZI: "SYN/UZI", Weapons.SHOTGUN: "Shotgun", Weapons.MACHINE_GUN: "Machine gun",
                        Weapons.FIRE_WALL_FLAMETHROWER: "Fire wall", Weapons.LASER: "Laser",
                        Weapons.YOSSIZ_THE_DEVASTATOR: "Yossiz the devastator",
                        Weapons.THE_LIGHTNING_BOLT: "The lightning bolt", Weapons.SYN_ACK_LASER: "SYN/ACK laser",
                        Weapons.CYBER_CALL_OF_THE_BLACK_KNIGHT: "Cyber call of the black knight", Weapons.DOOM: "Doom"}
    return weapon_name_dict[weapon]


def get_weapon_description(weapon):
    weapon_description_dict = {Weapons.GUN: "Low speed. Low damage. Medium cooldown. 100% hit chance.",
                               Weapons.UDP_PACKET_MISSILE: "Shoots out UDP packets that seek out enemies, has a low chance of hitting",
                               Weapons.SYN_ACK_CANNON: "Deals low damage and has a short cooldown but has a high chance of hitting",
                               Weapons.SYN_UZI: "Deals medium damage and has a very low cooldown but has a very low chance of hitting",
                               Weapons.SHOTGUN: "Deals high damage and has a medium cooldown but has a medium chance of hitting",
                               Weapons.MACHINE_GUN: "Deals high damage and has a long cooldown but has a very low chance of hitting",
                               Weapons.FIRE_WALL_FLAMETHROWER: "Deals high damage and has a very long cooldown but has a very high chance of hitting",
                               Weapons.LASER: "Deals high damage and has a very long cooldown but has a very high chance of hitting",
                               Weapons.YOSSIZ_THE_DEVASTATOR: "Deals immensely high damage in a spread attack and has a short cooldown, has a good chance of hitting",
                               Weapons.THE_LIGHTNING_BOLT: "Deals incredibly high damage and has a medium cooldown, has a good chance of hitting",
                               Weapons.SYN_ACK_LASER: "Deals low damage, has a very low cooldown, 100% chance of hitting",
                               Weapons.CYBER_CALL_OF_THE_BLACK_KNIGHT: "Deals immense damage, has no cooldown, 100% chance of hitting, calls for help.",
                               Weapons.DOOM: "Unknown."}
    return weapon_description_dict[weapon]


def get_weapon_pun(weapon):
    weapon_pun_dict = {Weapons.GUN: "It's a gun.",
                       Weapons.UDP_PACKET_MISSILE: "If you've ever wanted to shoot a UDP packet, now is your chance.",
                       Weapons.SYN_ACK_CANNON: "So you'll never miss a shot.",
                       Weapons.SYN_UZI: "Ever wanted to ddos someone? Well now you can.",
                       Weapons.SHOTGUN: "It's a shotgun.",
                       Weapons.MACHINE_GUN: "It's a machine gun.",
                       Weapons.FIRE_WALL_FLAMETHROWER: "It's a fire wall, but it's also a flamethrower.",
                       Weapons.LASER: "It's a laser.",
                       Weapons.YOSSIZ_THE_DEVASTATOR: "Yossi will be proud.",
                       Weapons.THE_LIGHTNING_BOLT: "You can say it's, electric.",
                       Weapons.SYN_ACK_LASER: "Remember the syn uzi? and the lazer? well, when you combine both you get this. a massive ddos attack.",
                       Weapons.CYBER_CALL_OF_THE_BLACK_KNIGHT: "You can call for help.",
                       Weapons.DOOM: "You can't kill me. Destruction."}
    return weapon_pun_dict[weapon]


class Text:

    def __init__(self, x, y, text: str, font, color: tuple):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color

    def render(self, surface, pos=None):
        if pos is None:
            pos = (self.x, self.y)
        text = self.font.render(self.text, True, self.color)
        surface.blit(text, (pos[0] - text.get_width() / 2, pos[1] - text.get_height() / 2))

    def set_text(self, text):
        self.text = text


class Button(Text):

    def __init__(self, x, y, w: int, h: int, text: str, text_color: tuple, font, bg_color: tuple, hover_color: tuple,
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

    def __init__(self, x, y, image_path: str, fade_in: bool = False, width: int = None, height: int = None,
                 repeating=False, repeating_width=None, repeating_height=None):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image.set_alpha(255 if not fade_in else 0)
        self.is_fading_in = fade_in
        self.is_fading_out = False
        self.faded_out = False
        self.replace_image = None

        self.repeating = repeating
        self.repeating_width = repeating_width
        self.repeating_height = repeating_height
        if width is not None:
            self.image = pygame.Surface.subsurface(self.image, (0, 0, width, self.image.get_height()))
        if height is not None:
            self.image = pygame.Surface.subsurface(self.image, (0, 0, self.image.get_width(), height))

    def render(self, surface: pygame.Surface):
        if self.is_fading_in:
            if self.fade_in():
                self.is_fading_in = False
        elif self.is_fading_out:
            if self.fade_out():
                self.is_fading_out = False
                self.faded_out = True
        if self.repeating:
            for i in range(int(self.x), int(surface.get_width()), self.image.get_width()):
                for j in range(int(self.y), int(surface.get_height()), self.image.get_height()):
                    surface.blit(self.image, (i, j))
        else:
            surface.blit(self.image, (self.x, self.y))

    def get_size(self):
        if self.repeating:
            return (self.repeating_width, self.repeating_height)
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


class Bullet:

    def __init__(self, x, y, for_vel_x, for_vel_y, radius, color, pos, travel_max, shooter_id, magnitude=200,
                 world=None, damage=10):
        self.x = x
        self.y = y
        self.orig_x, self.orig_y = x, y
        self.radius = radius
        self.color = color
        self.travel_max = travel_max
        self.damage = damage

        dx = pos[0] - for_vel_x
        dy = pos[1] - for_vel_y

        direction = pygame.math.Vector2(dx, dy).normalize()
        direction.scale_to_length(magnitude)

        self.vel_x = direction[0]
        self.vel_y = direction[1]

        self.world = world

        self.shooter_id = shooter_id

    def update(self, dt):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

    def render(self, win, progressionx, progressiony):
        pygame.draw.circle(win, self.color, (int(self.x - progressionx), int(self.y + progressiony)), self.radius)

        if ACTIVE_HITBOXES:
            pygame.draw.rect(win, (0, 255, 0), (
                self.x - progressionx - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2), 2)

    def collide(self, platforms):
        for p in platforms:
            if isinstance(p, Image) or isinstance(p, Ladder):
                continue
            if p.collide_coords(self.x, self.y):
                return True
        return False

    def collide_with(self, player):
        if self.x < player.x + player.image.get_width() and self.x > player.x and self.y < player.y + player.image.get_height() and self.y > player.y:
            return True
        return False


class Player:

    def __init__(self, idle_image_path: str, move_image_path: str, jump_image_path: str, dead_image_path: str,
                 dash_image_path: str, sprite_width: int,
                 side_padding: int, top_padding: int, pos: tuple,
                 speed: int):
        super().__init__()

        # Mechanics variables
        self.is_on_ladder = False
        self.speed = 0
        self.xspeed = speed
        self.is_falling = False
        self.left = False
        self.animation_timer = 0
        self.x, self.y = pos
        self.orig_x, self.orig_y = pos
        self.side_padding = side_padding
        self.top_padding = top_padding

        self.y_velocity = 0
        self.gravity = 14
        self.jump_height = -12

        self.gravity = self.gravity * 1000 / 250
        self.jump_height = self.jump_height * 1000 / 10

        self.jump_multiplier = 1
        self.terminal_y_velocity = 30

        self.max_y = None

        # Game mechanics variables
        self.max_health = MAX_HEALTH
        self.hp = self.max_health
        self.max_stamina = MAX_STAMINA
        self.stamina = self.max_stamina
        self.consumables = []
        self.items = []
        self.jump_boost = False
        self.double_jump = False

        self.is_dead = False
        self.is_temp_dead = False
        self.revived = False
        self.dead_time = 5
        self.dead_timer = 0

        self.dash_framerate = 10
        self.dash_duration = 1.2
        self.dash_timer = -1

        self.dash_mult = 5

        self.shoot_timer = -1
        self.shoot_framerate = 10
        self.shoot_cooldown = 2

        self.world = "monologue"

        # Item variables
        self.weapon = Weapons.GUN
        self.show_gun_description = False
        self.machine_gun_cooldown_reduction_multiplier = 50
        self.machine_gun_start_cooldown = 7

        # Animation files
        self.idle_sheet = pygame.image.load(idle_image_path)
        self.move_sheet = pygame.image.load(move_image_path)
        self.jump_sheet = pygame.image.load(jump_image_path)
        self.dead_sheet = pygame.image.load(dead_image_path)
        self.dash_image = pygame.image.load(dash_image_path)
        self.current_image = self.idle_sheet
        self.image = pygame.Surface.subsurface(self.current_image, (0, 0, sprite_width, sprite_width))
        self.frame_width = sprite_width

        # Animation variables
        self.animation_framerate = 7.5

        # Networking variables
        self.id = None
        self.name = None
        self.is_host = False

    def revive(self):
        self.is_temp_dead = False
        self.dead_timer = 0
        self.revived = True
        self.move("stay")
        self.hp = self.max_health
        self.stamina = self.max_stamina
        self.x = self.orig_x
        self.y = self.orig_y

    def update(self, delta_time: float):

        if self.is_temp_dead and not self.current_image == self.dead_sheet:
            self.current_image = self.dead_sheet
            self.speed = 0
            self.animation_timer = 0

        if self.is_temp_dead:
            self.dead_timer += delta_time
            if self.dead_timer > self.dead_time:
                self.revive()

        if self.dash_timer != -1:
            self.dash_timer += self.dash_framerate * delta_time
            if self.dash_timer >= self.dash_duration:
                self.dash_timer = -1

        if self.shoot_timer != -1:
            self.shoot_timer += self.shoot_framerate * delta_time
            if self.shoot_timer >= self.shoot_cooldown:
                self.shoot_timer = -1

        if self.hp < self.max_health:
            self.hp += 4 * delta_time
            if self.hp > self.max_health:
                self.hp = self.max_health

        if self.is_falling and not self.is_on_ladder:
            self.y_velocity += self.gravity * delta_time
            if self.y_velocity > self.terminal_y_velocity:
                self.y_velocity = self.terminal_y_velocity
            if self.y_velocity < -self.terminal_y_velocity:
                self.y_velocity = -self.terminal_y_velocity
        self.x += self.speed * delta_time
        if self.speed == 0 and self.stamina < self.max_stamina:
            self.stamina += 15 * delta_time
            if self.stamina > self.max_stamina:
                self.stamina = self.max_stamina
        self.y += self.y_velocity
        self.animation_timer += self.animation_framerate * delta_time
        if self.animation_timer > int(self.current_image.get_width() / self.frame_width) - 1 and self.is_temp_dead:
            self.animation_timer = int(self.current_image.get_width() / self.frame_width) - 1

        if self.max_y is not None and self.y + self.image.get_height() > self.max_y:
            self.y = self.max_y - self.image.get_height()

    def move(self, direction: str):

        if self.is_temp_dead:
            return

        if direction == "left":
            if not self.left:
                self.idle_sheet = pygame.transform.flip(self.idle_sheet, True, False)
                self.move_sheet = pygame.transform.flip(self.move_sheet, True, False)
                self.jump_sheet = pygame.transform.flip(self.jump_sheet, True, False)
                self.dash_image = pygame.transform.flip(self.dash_image, True, False)
            self.current_image = self.move_sheet
            self.speed = -self.xspeed
            self.left = True
        elif direction == "right":
            if self.left:
                self.move_sheet = pygame.transform.flip(self.move_sheet, True, False)
                self.idle_sheet = pygame.transform.flip(self.idle_sheet, True, False)
                self.jump_sheet = pygame.transform.flip(self.jump_sheet, True, False)
                self.dash_image = pygame.transform.flip(self.dash_image, True, False)
                self.left = False
            self.current_image = self.move_sheet
            self.speed = self.xspeed
        else:
            self.current_image = self.idle_sheet
            self.speed = 0

    def animate(self, x, y, dt):

        if self.is_temp_dead:
            return

        if self.dash_timer != -1:
            return

        if x > self.x:
            if self.left:
                self.move_sheet = pygame.transform.flip(self.move_sheet, True, False)
                self.idle_sheet = pygame.transform.flip(self.idle_sheet, True, False)
                self.jump_sheet = pygame.transform.flip(self.jump_sheet, True, False)
                self.dash_image = pygame.transform.flip(self.dash_image, True, False)
                self.left = False
            self.current_image = self.move_sheet
        elif x < self.x:
            if not self.left:
                self.idle_sheet = pygame.transform.flip(self.idle_sheet, True, False)
                self.move_sheet = pygame.transform.flip(self.move_sheet, True, False)
                self.jump_sheet = pygame.transform.flip(self.jump_sheet, True, False)
                self.dash_image = pygame.transform.flip(self.dash_image, True, False)
            self.current_image = self.move_sheet
            self.left = True
        elif y != self.y:
            self.current_image = self.jump_sheet
        else:
            self.current_image = self.idle_sheet

    def jump(self, delta_time):
        if self.is_temp_dead:
            return
        if self.is_on_ladder:
            self.y -= 500 * delta_time
        if not self.is_falling or self.double_jump or INFINITE_JUMP_DASH:
            self.current_image = self.jump_sheet
            self.y_velocity = self.jump_height * self.jump_multiplier * delta_time
            if self.double_jump:
                self.y_velocity *= 2
            self.jump_multiplier = 1
            self.jump_boost = False
            self.double_jump = False
            self.is_falling = True

    def stop_fall(self, y: int):
        self.is_falling = False
        if self.current_image == self.jump_sheet:
            self.move("stay" if self.speed == 0 else ("left" if self.speed < 0 else "right"))
        self.y_velocity = 0
        self.y = y - self.image.get_height()

    def fall(self):
        self.is_falling = True

    def dash(self, delta_time: float):
        if self.is_temp_dead:
            return
        if self.stamina - 7 > 0 or INFINITE_JUMP_DASH:
            self.stamina -= 7
            if self.stamina < 0:
                self.stamina = 0
            self.x += self.speed * self.dash_mult * delta_time + 0 if not INFINITE_JUMP_DASH else self.speed
            self.dash_timer = 0

    def draw(self, surface: pygame.Surface, stage_width: int, stage_height: int):
        if self.animation_timer >= int(self.current_image.get_width() / self.frame_width) and not self.is_temp_dead:
            self.animation_timer = 0
        if self.dash_timer != -1:
            self.image = self.dash_image
        else:
            self.image = pygame.Surface.subsurface(self.current_image, (
                0 + self.frame_width * int(self.animation_timer),
                0,
                self.frame_width, self.current_image.get_height()))
        self.image = pygame.transform.scale(self.image,
                                            (150, int(150 * self.image.get_height() / self.image.get_width())))

        x_pos = (self.x - (stage_width - WIDTH)) if self.x > stage_width - WIDTH / 2 else (
            self.x if self.x < WIDTH / 2 else WIDTH / 2)

        y_pos = self.y if self.y < HEIGHT / 2 - self.image.get_height() / 2 else HEIGHT / 2 - self.image.get_height() / 2
        if self.y > stage_height - HEIGHT / 2 - self.image.get_height() / 2:
            y_pos = self.y - (stage_height - HEIGHT)

        surface.blit(self.image, (x_pos, y_pos))

        # Draw name
        name_surface = PIX_FONT.render(self.name, True, (255, 255, 255))
        # name_surface = pygame.transform.scale(name_surface, (150, int(150 * name_surface.get_height() / name_surface.get_width())))
        surface.blit(name_surface, (x_pos, y_pos + self.top_padding / 2))

        if self.is_temp_dead:
            pygame.draw.rect(surface, (255, 0, 0), (x_pos, y_pos, 100, 10), 2)
            pygame.draw.rect(surface, (255, 0, 0), (x_pos, y_pos, int(100 * self.dead_timer / self.dead_time), 10))

        if ACTIVE_HITBOXES:
            pygame.draw.rect(surface, (255, 0, 0), (
                x_pos + self.side_padding, y_pos + self.top_padding, self.image.get_width() - self.side_padding * 2,
                self.image.get_height() - self.top_padding), 2)

    def draw_relative(self, surface: pygame.Surface, progressionx: int, progressiony: int):
        if self.animation_timer >= int(self.current_image.get_width() / self.frame_width) and not self.is_temp_dead:
            self.animation_timer = 0
        try:
            self.image = pygame.Surface.subsurface(self.current_image, (
                0 + self.frame_width * int(self.animation_timer),
                0,
                self.frame_width, self.current_image.get_height()))
            self.image = pygame.transform.scale(self.image,
                                                (150, int(150 * self.image.get_height() / self.image.get_width())))
            surface.blit(self.image, (self.x - progressionx, self.y + progressiony))
        except Exception as e:
            print("Error drawing player:", e)

        # Draw name
        name_surface = PIX_FONT.render(self.name, True, (255, 255, 255))
        surface.blit(name_surface, (self.x - progressionx, self.y + self.top_padding / 2 + progressiony))

        if self.is_temp_dead:
            pygame.draw.rect(surface, (255, 0, 0), (self.x - progressionx, self.y + progressiony, 100, 10), 2)
            pygame.draw.rect(surface, (255, 0, 0),
                             (self.x - progressionx, self.y + progressiony, int(100 * self.dead_timer / self.dead_time),
                              10))

        if ACTIVE_HITBOXES:
            pygame.draw.rect(surface, (255, 0, 0),
                             (self.x + self.side_padding - progressionx, self.y + self.top_padding + progressiony,
                              self.image.get_width() - self.side_padding * 2,
                              self.image.get_height() - self.top_padding), 2)

    def draw_stats(self, surface: pygame.Surface, font: pygame.font.Font, stage_width: int, stage_height: int):
        bg = pygame.Surface((700, 120))
        bg.fill((50, 50, 50))
        bg.set_alpha(200)
        surface.blit(bg, (surface.get_width() - 700, 0))
        hp_text = font.render(f"HP: {int(self.hp)}", True, (255, 0, 0))
        stamina_text = font.render(f"Stamina: {int(self.stamina)}", True, (173, 216, 230))
        surface.blit(hp_text, (surface.get_width() - hp_text.get_width() - 420, 10))
        surface.blit(stamina_text, (surface.get_width() - stamina_text.get_width() - 420, 40))
        pygame.draw.rect(surface, (255, 0, 0),
                         (surface.get_width() - 410, 10, int(self.hp * 400 / self.max_health), 20))
        pygame.draw.rect(surface, (173, 216, 230),
                         (surface.get_width() - 410, 40, int(self.stamina * 400 / self.max_stamina), 20))

        gun_text = font.render(f"Gun: {get_weapon_name(self.weapon)}", True, (255, 255, 255))
        surface.blit(gun_text, (surface.get_width() - gun_text.get_width() - 420, 70))

        if self.jump_boost:
            x_pos = (self.x - (stage_width - WIDTH)) if self.x > stage_width - WIDTH / 2 else (
                self.x if self.x < WIDTH / 2 else WIDTH / 2)

            y_pos = self.y if self.y < HEIGHT / 2 else HEIGHT / 2
            if self.y > stage_height - HEIGHT / 2:
                y_pos = self.y - (stage_height - HEIGHT)

            # surface.blit(pygame.image.load('resources/icons/jump_boost.png'), (surface.get_width() - 410, 70)) # below stamina
            surface.blit(
                pygame.transform.scale(JUMP_BOOST_ICON, (60, 60)),
                (x_pos + self.side_padding, y_pos))  # above player

        if self.show_gun_description:
            pygame.draw.rect(surface, (50, 50, 50), (surface.get_width() - 410, 70, 400, 200))
            description_text = SMALL_ARIEL.render(get_weapon_description(self.weapon), True, (255, 255, 255))
            surface.blit(description_text, (surface.get_width() - 410, 70))
            pun_text = SMALL_ARIEL.render(f"{get_weapon_pun(self.weapon)}", True, (255, 255, 255))
            surface.blit(pun_text, (surface.get_width() - 410, 70 + description_text.get_height()))

    def collide(self, platforms, delta_time):
        found_bot = False
        found_ladder = False
        for platform in platforms:
            if isinstance(platform, HeightPortal) and platform.collide(self):
                self.world = platform.destination
                continue
            elif isinstance(platform, Crystal) and platform.collide(self):
                if platform.cooldown == -1:
                    if isinstance(platform, JumpCrystal):
                        if self.double_jump:
                            continue
                        self.double_jump = True
                    if isinstance(platform, HealthCrystal):
                        if self.hp == self.max_health:
                            continue
                        self.hp += platform.amount
                        if self.hp > self.max_health:
                            self.hp = self.max_health
                    if isinstance(platform, StaminaCrystal):
                        if self.stamina == self.max_stamina:
                            continue
                        self.stamina += platform.amount
                        if self.stamina > self.max_stamina:
                            self.stamina = self.max_stamina
                    platform.cooldown = 0
                continue

            if isinstance(platform, Ladder):
                if platform.collide(self):
                    self.is_on_ladder = True
                    self.y_velocity = 0
                    found_ladder = True
                    continue
                elif not found_ladder:
                    self.is_on_ladder = False

            if platform.collide(self) and self.is_falling and self.y_velocity > 0 and abs(
                    self.y + self.image.get_height() - platform.y) < 30:
                self.stop_fall(platform.y)
                found_bot = True
                if isinstance(platform, JumpPad):
                    self.jump_multiplier = platform.jump_multiplier
                    self.jump_boost = True
                    platform.used = True
            if platform.collide(
                    self) and platform.y < self.y + self.image.get_height() < platform.y + platform.height and self.speed < 0:
                self.x -= self.speed * delta_time
            if platform.collide(
                    self) and platform.y < self.y + self.image.get_height() < platform.y + platform.height and self.speed > 0:
                self.x -= self.speed * delta_time
            if platform.collide(
                    self) and platform.y + platform.height > self.y + self.top_padding and self.y_velocity < 0:
                self.y_velocity = 0

        if not found_bot:
            self.fall()

    def pickelize(self):
        self.idle_sheet = [self.idle_sheet.get_size(), pygame.image.tostring(self.idle_sheet, "RGBA")]
        self.jump_sheet = [self.jump_sheet.get_size(), pygame.image.tostring(self.jump_sheet, "RGBA")]
        self.move_sheet = [self.move_sheet.get_size(), pygame.image.tostring(self.move_sheet, "RGBA")]
        self.dead_sheet = [self.dead_sheet.get_size(), pygame.image.tostring(self.dead_sheet, "RGBA")]
        self.dash_image = [self.dash_image.get_size(), pygame.image.tostring(self.dash_image, "RGBA")]
        self.image = [self.image.get_size(), pygame.image.tostring(self.image, "RGBA")]
        self.current_image = [self.current_image.get_size(), pygame.image.tostring(self.current_image, "RGBA")]

    def unpickelize(self):
        self.idle_sheet = pygame.image.fromstring(self.idle_sheet[1], self.idle_sheet[0], "RGBA")
        self.jump_sheet = pygame.image.fromstring(self.jump_sheet[1], self.jump_sheet[0], "RGBA")
        self.move_sheet = pygame.image.fromstring(self.move_sheet[1], self.move_sheet[0], "RGBA")
        self.dead_sheet = pygame.image.fromstring(self.dead_sheet[1], self.dead_sheet[0], "RGBA")
        self.dash_image = pygame.image.fromstring(self.dash_image[1], self.dash_image[0], "RGBA")
        self.image = pygame.image.fromstring(self.image[1], self.image[0], "RGBA")
        self.current_image = pygame.image.fromstring(self.current_image[1], self.current_image[0], "RGBA")

    def check_mouse_over_gun_slot(self, pos):
        # surface.get_width() - gun_text.get_width() - 420, 70
        if pos[0] >= 1920 - 700 and pos[0] <= 1920 and pos[1] >= 70 and pos[1] <= 140:
            self.show_gun_description = True
        else:
            self.show_gun_description = False

    def change_weapon(self, weapon):
        self.weapon = weapon
        if self.weapon == Weapons.GUN:
            self.shoot_cooldown = 2
        elif self.weapon == Weapons.SHOTGUN:
            self.shoot_cooldown = 4
        elif self.weapon == Weapons.FIRE_WALL_FLAMETHROWER or self.weapon == Weapons.LASER:
            self.shoot_cooldown = 0
        elif self.weapon == Weapons.SYN_UZI:
            self.shoot_cooldown = 1
        elif self.weapon == Weapons.MACHINE_GUN:
            self.shoot_cooldown = self.machine_gun_start_cooldown


class Platform:

    def __init__(self, pos: tuple, width: int, height: int, color: tuple = None, ):
        self.x, self.y = pos
        self.width = width
        self.height = height
        self.color = color

    def collide(self, player: Player):
        if player.x + player.side_padding <= self.x + self.width and player.x + player.image.get_width() - player.side_padding >= self.x:
            if player.y + player.image.get_height() >= self.y and player.y <= self.y + self.height:
                return True
        return False

    def collide_coords(self, x, y):
        return (self.x + self.width >= x >= self.x) and (self.y <= y <= self.y + self.height)

    def render(self, surface: pygame.Surface, background_progressionx: int, background_progressiony: int):
        if self.color is not None and self.x + self.width - background_progressionx > 0 and self.x - background_progressionx < surface.get_width() and self.y + self.height + background_progressiony > 0 and self.y + background_progressiony < surface.get_height():
            pygame.draw.rect(surface, self.color, (
            self.x - background_progressionx, self.y + background_progressiony, self.width, self.height))

        if ACTIVE_HITBOXES:
            s = PIX_FONT.render(str(self.x) + " " + str(self.y), True, (255, 255, 255))
            surface.blit(s, (self.x - background_progressionx + 20, self.y + background_progressiony))
            pygame.draw.rect(surface, (255, 0, 0), (
                self.x - background_progressionx, self.y + background_progressiony, self.width, self.height), 2)


class SpriteGroup:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.sprites = []

    def add(self, sprite):
        self.sprites.append(sprite)

    def update(self, dt):
        for sprite in self.sprites:
            sprite.update(dt)

    def draw(self, p_id, background_progressionx: int, background_progressiony, background: Image, world: str):
        for sprite in self.sprites:
            if sprite.world != world:
                continue
            if sprite.id != p_id:
                sprite.draw_relative(self.surface, background_progressionx, background_progressiony)
            else:
                sprite.draw(self.surface, background.get_size()[0], background.get_size()[1])

    def remove(self, sprite):
        self.sprites.remove(sprite)

    def empty(self):
        self.sprites.clear()

    def get_sprites(self):
        return self.sprites


class Ladder(Platform):

    def __init__(self, pos: tuple, width: int, height: int, color: tuple = None, ):
        super().__init__(pos, width, height, color)


class JumpPad(Platform):
    def __init__(self, pos: tuple, width: int, height: int, jump_multiplier: float = 1.5, is_finite: bool = False):
        super().__init__(pos, width, height)
        self.jump_multiplier = jump_multiplier
        self.used = False
        self.is_finite = is_finite

    def render(self, surface: pygame.Surface, background_progressionx: int, background_progressiony: int):
        if self.x + self.width - background_progressionx > 0 and self.x - background_progressionx < surface.get_width() and (
                (self.is_finite and not self.used) or not self.is_finite):
            surface.blit(
                pygame.transform.scale((JUMP_PAD if
                                        not self.used or not self.is_finite else JUMP_PAD_USED),
                                       (self.width, self.height)),
                (self.x - background_progressionx, self.y + background_progressiony))


class Crystal(Image):
    def __init__(self, pos: tuple, img_path: str, cooldown_max: int):
        super().__init__(pos[0], pos[1], img_path, False)
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * 2), int(self.image.get_height() * 2)))
        self.width = self.image.get_width() / 4
        self.height = self.image.get_height()
        self.cooldown = -1
        self.cooldown_max = cooldown_max
        self.cooldown_mult = 5

        self.move_rate = 3.5
        self.max_downing = 1
        self.downing = random.randint(-self.max_downing, self.max_downing)
        self.is_downing = True

    def render(self, surface: pygame.Surface, background_progressionx: int, background_progressiony: int):

        if self.x + self.image.get_width() - background_progressionx > 0 and self.x - background_progressionx < surface.get_width() and self.y + self.image.get_height() + background_progressiony > 0 and self.y + background_progressiony < surface.get_height():
            if self.cooldown == -1:
                im = pygame.Surface.subsurface(self.image, (0, 0, self.width, self.height))
            else:
                im = pygame.Surface.subsurface(self.image, (
                    self.width + self.width * (int(self.cooldown * 3) % 3), 0, self.width, self.height))
                pygame.draw.rect(surface, (255, 255, 255),
                                 (self.x - background_progressionx, self.y - 15 + background_progressiony, self.width,
                                  10), 2)
                pygame.draw.rect(surface, (255, 255, 255), (
                    self.x - background_progressionx, self.y - 15 + background_progressiony,
                    self.cooldown * self.width / self.cooldown_max, 10))
            surface.blit(im, (self.x - background_progressionx, self.y + background_progressiony))

    def update(self, dt):
        if self.cooldown != -1:
            self.cooldown += dt * self.cooldown_mult
            if self.cooldown >= self.cooldown_max:
                self.cooldown = -1

        if isinstance(self, JumpCrystal):
            if self.is_downing:
                self.downing += dt * self.move_rate
                if abs(self.downing) >= self.max_downing:
                    self.downing = self.max_downing
                    self.is_downing = False
                else:
                    self.y += self.downing
            else:
                self.downing -= dt * self.move_rate
                if abs(self.downing) >= self.max_downing:
                    self.downing = -self.max_downing
                    self.is_downing = True
                else:
                    self.y += self.downing

    def collide(self, player: Player):
        if player.x + player.side_padding <= self.x + self.width and player.x + player.image.get_width() - player.side_padding >= self.x:
            if player.y + player.image.get_height() >= self.y and player.y + player.top_padding <= self.y + self.height:
                return True
        return False


class JumpCrystal(Crystal):
    def __init__(self, pos: tuple):
        super().__init__(pos, "resources\\special\\jump-crystal.png", 5)


class StaminaCrystal(Crystal):
    def __init__(self, pos: tuple):
        super().__init__(pos, "resources\\special\\stamina-crystal.png", 60)
        self.amount = 60


class HealthCrystal(Crystal):
    def __init__(self, pos: tuple):
        super().__init__(pos, "resources\\special\\health-crystal.png", 120)
        self.amount = 60


class HeightPortal(Image):
    def __init__(self, pos: tuple, width: int, height: int, destination: str, inverted: bool = False):
        super().__init__(pos[0], pos[1], "resources\\special\\arena_entrance.png", True, width, height)
        self.width = width if width is not None else self.image.get_width()
        self.height = height if height is not None else self.image.get_height()
        self.destination = destination

        self.inverted = inverted
        if self.inverted:
            self.image = pygame.transform.flip(self.image, True, False)

    def render(self, surface: pygame.Surface, background_progressionx: int, background_progressiony: int):
        if self.is_fading_in:
            if self.fade_in():
                self.is_fading_in = False
        elif self.is_fading_out:
            if self.fade_out():
                self.is_fading_out = False
                self.faded_out = True
        text = PIX_FONT.render(self.destination, True, (255, 255, 255))
        text = pygame.transform.rotate(text, -90 if not self.inverted else 90)
        text_rect = text.get_rect()
        if not self.inverted:
            text_rect.center = (
            self.x + self.width - background_progressionx, self.y + self.height / 2 + background_progressiony)
        else:
            text_rect.center = (self.x - background_progressionx, self.y + self.height / 2 + background_progressiony)
        surface.blit(text, text_rect)
        if self.x + self.image.get_width() - background_progressionx > 0 and self.x - background_progressionx < WIDTH and self.y + self.image.get_height() + background_progressiony > 0 and self.y + background_progressiony < HEIGHT:
            surface.blit(self.image, (self.x - background_progressionx, self.y + background_progressiony))

    def collide(self, player: Player):
        if player.x + player.side_padding <= self.x + self.width and player.x + player.image.get_width() - player.side_padding >= self.x:
            if player.y + player.image.get_height() >= self.y and player.y <= self.y + self.height:
                return True
        return False


class Chest:
    def __init__(self):
        self.x = 0


class Renderer:

    def __init__(self, screen: pygame.Surface, background_image: Image):
        self.screen = screen
        self.sprites = SpriteGroup(self.screen)
        self.background = background_image
        self.background_progressionx = 0
        self.orig_background_progressionx = 0
        self.background_progressiony = 0
        self.orig_background_progressiony = 0
        self.dt = 0
        self.prev_time = 0
        self.children = []
        self.platforms = []
        self.bullets = []

        self.player_id = None
        self.game_started = False
        self.game_over = False

        self.world = None
        self.level_name = None
        self.level_name_alpha = 0

        # Init global assets
        self.load_global_assets()

    def load_global_assets(self):
        # Init global assets
        global PIX_FONT, JUMP_PAD, JUMP_PAD_USED, JUMP_BOOST_ICON, SMALL_ARIEL, PARALLAX, OVERGROWN, MIRAGE
        PIX_FONT = pygame.font.Font('resources\\fonts\\yoster-island\\yoster.ttf', 25)
        SMALL_ARIEL = pygame.font.SysFont('Arial', 15)
        # Buildings
        JUMP_PAD = pygame.image.load("resources/special/jump_pad_crystalized.png").convert_alpha()
        JUMP_PAD_USED = pygame.image.load('resources/special/used_pad.png').convert_alpha()

        # Icons
        JUMP_BOOST_ICON = pygame.image.load('resources/icons/jump_boost.png').convert_alpha()
        PARALLAX = Image(0, 0, "resources\\images\\arena-repeating-bg.png", True, None, None, True, 7000, 1080)
        OVERGROWN = Image(0, 0, "resources\\images\\overgrown.png", True, 4000, 2000)
        MIRAGE = Image(0, 0, "resources\\images\\mirage.png", True, 4000, 2000)

    def render_all(self, mouse_pos: tuple):
        self.background.x = -self.background_progressionx
        self.background.y = self.background_progressiony
        self.background.render(self.screen)
        if self.background.faded_out:
            self.background.faded_out = False
            self.background.is_fading_out = False
            self.background.is_fading_in = True
            self.background = self.background.replace_image
            self.background.replace_image = None
        if self.game_started:
            for platform in self.platforms:
                platform.render(self.screen, self.background_progressionx, self.background_progressiony)
        for child in self.children:
            if isinstance(child, Button):
                child.render(self.screen,
                             child.x < mouse_pos[0] < child.x + child.width and child.y < mouse_pos[
                                 1] < child.y + child.height)
            elif isinstance(child, JumpPad):
                child.render(self.screen, self.background_progressionx, self.background_progressiony)
            else:
                child.render(self.screen)
        if self.game_started:
            self.sprites.draw(self.player_id, self.background_progressionx, self.background_progressiony,
                              self.background, self.world)
            for bullet in self.bullets:
                bullet.render(self.screen, self.background_progressionx, self.background_progressiony)

    def update_all(self):
        if self.game_started:
            self.sprites.update(self.dt)
            for sprite in self.sprites.get_sprites():
                if sprite.id == self.player_id:
                    sprite.collide(self.platforms, self.dt)
                if sprite.revived and sprite.id != self.player_id:
                    sprite.revived = False
            for bullet in self.bullets:
                bullet.update(self.dt)
            for bullet in self.bullets:
                removed = False
                if bullet.world is not "monologue":
                    for sprite in self.sprites.get_sprites():
                        if bullet.world != sprite.world:
                            continue
                        if bullet.collide_with(
                                sprite) and bullet.shooter_id != sprite.id and not sprite.is_temp_dead and sprite.dash_timer == -1:
                            if sprite.id == self.player_id:
                                sprite.hp -= bullet.damage
                                if sprite.hp <= 0:
                                    sprite.hp = 0
                            self.bullets.remove(bullet)
                            removed = True
                if abs(bullet.x - bullet.orig_x) > bullet.travel_max or abs(
                        bullet.y - bullet.orig_y) > bullet.travel_max or bullet.x < 0 or bullet.x > \
                        self.background.get_size()[0] or bullet.y < 0 or bullet.y > self.background.get_size()[
                    1] or bullet.collide(self.platforms) and not removed:
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
            for platform in self.platforms:
                if isinstance(platform, Crystal):
                    platform.update(self.dt)
        for child in self.children:
            if isinstance(child, InputBox):
                child.update()

    def add_child(self, child):
        if isinstance(child, JumpPad):
            self.platforms.append(child)
        self.children.append(child)

    def remove_child(self, child):
        return self.children.remove(child)

    def fadeout_bg(self, replace_with: Image):
        self.background.is_fading_out = True
        self.background.replace_image = replace_with

    def replace_bg(self, replace_with: Image):
        self.background = replace_with
        self.background.replace_image = None

    def clear_children(self):
        self.children.clear()

    def add_sprite(self, sprite):
        self.sprites.add(sprite)

    def remove_sprite(self, sprite):
        self.sprites.remove(sprite)

    def clear_sprites(self):
        self.sprites.empty()

    def add_platform(self, pos: tuple, width: int, height: int, color: tuple = None):
        self.platforms.append(Platform(pos, width, height, color))

    def add_imaginary_platform(self, plat):
        self.platforms.append(plat)

    def clear_platforms(self):
        self.platforms.clear()

    def add_bullet(self, client, x, y, vel_x, vel_y, x2, y2, rad, vel_mult=200, max_travel=2000, damage=10,
                   color=(255, 255, 255)):
        bull = Bullet(x, y, vel_x, vel_y, rad, color, (x2, y2), max_travel, self.player_id, vel_mult, self.world,
                      damage)
        self.bullets.append(bull)
        client.send_bullet(bull)

    def clear_bullets(self):
        self.bullets.clear()

    def add_bullet_from_obj(self, bull):
        if bull.world == self.world:
            self.bullets.append(bull)

    def update_dt(self):
        t = pygame.time.get_ticks()
        self.dt = min((t - self.prev_time) / 1000.0, 1 / 60)
        self.prev_time = t

    def load_lobby(self, lobby):
        self.clear_sprites()
        for payload in lobby:
            pl = payload.player
            pl.unpickelize()
            self.add_sprite(pl)

    def get_player(self):
        for sprite in self.sprites.get_sprites():
            if sprite.id == self.player_id:
                return sprite

    def get_player_by_id(self, id):
        for sprite in self.sprites.get_sprites():
            if str(sprite.id) == id:
                return sprite

    def update_player_coords(self, p_id, x, y):
        for sprite in self.sprites.get_sprites():
            if str(sprite.id) == str(p_id):
                sprite.animate(x, y, self.dt)
                sprite.x = x
                sprite.y = y
                break

    def has_child(self, c):
        for child in self.children:
            if child == c:
                return True
        return False

    def load_level(self, msg):
        player = self.get_player()
        self.clear_children()
        self.clear_platforms()
        self.clear_bullets()
        firstPlat = True
        while len(msg) > 0:
            obj_len = int.from_bytes(msg[:8], byteorder='big')
            msg = msg[9:]
            plat = pickle.loads(msg[:obj_len])
            if firstPlat:
                if plat.y == 1878:
                    self.replace_bg(OVERGROWN)
                    self.orig_background_progressionx = 0
                    self.background_progressionx = 0
                    self.orig_background_progressiony = -1000  # -987
                    self.background_progressiony = self.orig_background_progressiony
                    player.x = 300
                    player.y = 1874 - player.image.get_height()
                    player.max_y = 1878
                    player.orig_x = player.x
                    player.orig_y = player.y
                    self.level_name = "Overgrown"
                    self.level_name_alpha = 255
                else:
                    self.replace_bg(MIRAGE)
                    self.orig_background_progressionx = 0
                    self.background_progressionx = 0
                    self.orig_background_progressiony = -1000
                    self.background_progressiony = self.orig_background_progressiony
                    player.x = 300
                    player.y = 1553
                    player.max_y = None
                    player.orig_x = player.x
                    player.orig_y = player.y
                    self.level_name = "Mirage"
                    self.level_name_alpha = 255
                firstPlat = False

            if isinstance(plat, JumpPad):
                self.add_child(plat)
            else:
                if isinstance(plat, JumpCoord):
                    plat = JumpCrystal((plat.x, plat.y))
                elif isinstance(plat, StaminaCoord):
                    plat = StaminaCrystal((plat.x, plat.y))
                elif isinstance(plat, HealthCoord):
                    plat = HealthCrystal((plat.x, plat.y))
                elif isinstance(plat, JumpPadCoord):
                    plat = JumpPad((plat.x, plat.y), plat.width, plat.height, plat.jump_strength)

                self.add_imaginary_platform(plat)

            msg = msg[obj_len:]

        self.add_imaginary_platform(
            HeightPortal((4000 - 80, 0), None, None, f"level_{str(int(self.world[-1]) + 1)}", True))
        self.add_imaginary_platform(
            HeightPortal((4000 - 80, 1080), None, None, f"level_{str(int(self.world[-1]) + 1)}", True))
        self.add_imaginary_platform(HeightPortal((0, 0), None, None,
                                                 f"monologue" if self.world == "level_1" else f"level_{str(int(self.world[-1]) - 1)}",
                                                 False))
        self.add_imaginary_platform(HeightPortal((0, 1080), None, None,
                                                 f"monologue" if self.world == "level_1" else f"level_{str(int(self.world[-1]) - 1)}",
                                                 False))

    def render_level_name(self, screen):
        font = pygame.font.SysFont("Edwardian Script ITC", 220)
        text = font.render(self.level_name, True, (0, 0, 255))
        text_rect = text.get_rect()
        # center of screen
        text_rect.center = (WIDTH // 2, 400)
        text.set_alpha(self.level_name_alpha)
        if self.level_name_alpha > 0:
            self.level_name_alpha -= 2
        screen.blit(text, text_rect)


class MusicManager:

    def __init__(self, music_list: list, music_volume: float = 1.0):
        self.music_list = music_list
        self.music_index = random.randint(0, len(self.music_list) - 1)
        pygame.mixer.init()
        pygame.mixer.music.set_volume(music_volume)
        # fucking mute this piece fo shit
        pygame.mixer.music.set_volume(0)

    def start_music(self):
        pygame.mixer.music.load(self.music_list[self.music_index])
        pygame.mixer.music.play()

    def start_specific_music(self, music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()

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

    def pause_music(self):
        pygame.mixer.music.pause()

    def unpause_music(self):
        pygame.mixer.music.unpause()

    def update(self):
        if not pygame.mixer.music.get_busy():
            self.next_music()

    def set_volume(self, volume: float):
        pygame.mixer.music.set_volume(volume)