import random
import pygame
from enum import Enum
from configparser import ConfigParser

# apply configs
config = ConfigParser()
config.read('conf.ini')
WIDTH = int(config.get('settings','WINDOW_WIDTH'))
HEIGHT = int(config.get('settings','WINDOW_HEIGHT'))
ACTIVE_HITBOXES = config.getboolean('settings','ACTIVE_HITBOXES')

# Assets
# Fonts
PIX_FONT = None # pygame.font.Font('resources\\fonts\\yoster-island\\yoster.ttf', 25)

# Buildings
JUMP_PAD = None # pygame.image.load("resources/special/jump_pad_crystalized.png").convert_alpha()
JUMP_PAD_USED = None # pygame.image.load('resources/special/used_pad.png').convert_alpha()

# Icons
JUMP_BOOST_ICON = None # pygame.image.load('resources/icons/jump_boost.png').convert_alpha()

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
# - Add isHoverPlatform to platform to make it not colldie you in sides and bottom

def random_name():
    with open ('names.txt', 'r') as f:
        names = f.read().splitlines()
    return random.choice(names)


class Checkbox:
    def __init__(self, surface, x, y, color, caption,outline_color,check_color, font, font_color,text_offset=(45, 15)):
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
            print(str(self.caption)+' toggle '+str(self.checked))

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
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def render(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Items(Enum):
    # Powerups
    COPPER_WIRE = 0  # Increase speed but decrease armor
    SILVER_WIRE = 1  # Increase armor but decrease speed
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
    GUN = 0  # Just a basic gun
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

    def __init__(self, x, y, image_path: str, fade_in: bool = False):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
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


class Bullet:

    def __init__(self, x, y, for_vel_x, for_vel_y, radius, color, pos, travel_max, player_shot=False, magnitude=200, bg_prog=None):
        self.x = x
        self.y = y
        self.orig_x, self.orig_y = x, y
        self.radius = radius
        self.color = color
        self.player_shot = player_shot
        self.travel_max = travel_max

        dx = pos[0] - for_vel_x
        dy = pos[1] - for_vel_y

        direction = pygame.math.Vector2(dx, dy).normalize()
        direction.scale_to_length(magnitude)

        self.vel_x = direction[0]
        self.vel_y = direction[1]

        self.bg_prog = bg_prog

    def update(self, dt):
        self.x += self.vel_x*dt
        self.y += self.vel_y*dt

    def render(self, win, progression):
        pygame.draw.circle(win, self.color, (self.x-progression, self.y), self.radius)

        if ACTIVE_HITBOXES:
            pygame.draw.rect(win, (0, 255, 0), (self.x - progression-self.radius, self.y-self.radius, self.radius*2, self.radius*2), 2)
    def collide(self, platforms):
        for p in platforms:
            if p.collide_coords(self.x,self.y):
                return True
        return False


class Player:

    def __init__(self, idle_image_path: str, move_image_path: str, jump_image_path: str, dead_image_path: str, dash_image_path: str, sprite_width: int,
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
        self.orig_x, self.orig_y = pos
        self.side_padding = side_padding
        self.top_padding = top_padding

        self.y_velocity = 0
        self.gravity = 14
        self.jump_height = -12
        self.jump_multiplier = 1
        self.terminal_y_velocity = 30

        # Game variables
        self.max_health = 100
        self.hp = self.max_health
        self.max_stamina = 110
        self.stamina = self.max_stamina
        self.consumables = []
        self.items = []
        self.jump_boost = False

        self.is_dead = False
        self.is_temp_dead = False
        self.revived = False
        self.dead_time = 5
        self.dead_timer = 0

        self.dash_framerate = 10
        self.dash_duration = 1.2
        self.dash_timer = -1

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
            self.animation_timer = 0
            return

        if self.is_temp_dead:
            if self.animation_timer < int(self.current_image.get_width() / self.frame_width)-1:
                self.animation_timer += self.animation_framerate * delta_time
                if self.animation_timer > int(self.current_image.get_width() / self.frame_width)-1:
                    self.animation_timer = int(self.current_image.get_width() / self.frame_width)-1
            else:
                self.dead_timer += delta_time
                if self.dead_timer > self.dead_time:
                    self.revive()
            return

        if self.dash_timer != -1:
            self.dash_timer += self.dash_framerate * delta_time
            if self.dash_timer >= self.dash_duration:
                self.dash_timer = -1

        if self.is_falling:
            self.y_velocity += self.gravity * delta_time
            if self.y_velocity > self.terminal_y_velocity:
                self.y_velocity = self.terminal_y_velocity
        self.x += self.speed * delta_time
        if self.speed != 0 and self.stamina - 1 * delta_time > 0:
            self.stamina -= 2 * delta_time
        elif self.speed == 0 and self.stamina < self.max_stamina:
            self.stamina += 15 * delta_time
            if self.stamina > self.max_stamina:
                self.stamina = self.max_stamina
        self.y += self.y_velocity
        self.animation_timer += self.animation_framerate * delta_time

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

    def animate(self, x, y):

        if self.is_temp_dead:
            return

        if x > self.x:
            if self.left:
                self.move_sheet = pygame.transform.flip(self.move_sheet, True, False)
                self.idle_sheet = pygame.transform.flip(self.idle_sheet, True, False)
                self.jump_sheet = pygame.transform.flip(self.jump_sheet, True, False)
                self.left = False
            self.current_image = self.move_sheet
        elif x < self.x:
            if not self.left:
                self.idle_sheet = pygame.transform.flip(self.idle_sheet, True, False)
                self.move_sheet = pygame.transform.flip(self.move_sheet, True, False)
                self.jump_sheet = pygame.transform.flip(self.jump_sheet, True, False)
            self.current_image = self.move_sheet
            self.left = True
        elif y != self.y:
            self.current_image = self.jump_sheet
        else:
            self.current_image = self.idle_sheet

    def jump(self):
        if self.is_temp_dead:
            return
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

    def dash(self, delta_time: float):
        if self.is_temp_dead:
            return
        if self.stamina - 20 > 0:
            self.stamina -= 20
            self.x += self.speed * 5 * delta_time
            self.dash_timer = 0

    def draw(self, surface: pygame.Surface):
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
        surface.blit(self.image, (self.x if self.x < WIDTH / 2 else WIDTH / 2, self.y))

        # Draw name
        name_surface = PIX_FONT.render(self.name, True, (255, 255, 255))
        #name_surface = pygame.transform.scale(name_surface, (150, int(150 * name_surface.get_height() / name_surface.get_width())))
        surface.blit(name_surface, (self.x if self.x < WIDTH / 2 else WIDTH / 2, self.y + self.top_padding/2))

        if self.is_temp_dead:
            pygame.draw.rect(surface, (255, 0, 0), (self.x if self.x < WIDTH / 2 else WIDTH / 2, self.y, 100,10), 2)
            pygame.draw.rect(surface, (255, 0, 0), (self.x if self.x < WIDTH / 2 else WIDTH / 2, self.y, int(100 * self.dead_timer / self.dead_time), 10))

        if ACTIVE_HITBOXES:
            pygame.draw.rect(surface, (255, 0, 0), (self.x if self.x < WIDTH / 2 else WIDTH / 2 + self.side_padding, self.y + self.top_padding, self.image.get_width() - self.side_padding*2, self.image.get_height() - self.top_padding), 2)

    def draw_relative(self, surface: pygame.Surface, progression: int):
        if self.animation_timer >= int(self.current_image.get_width() / self.frame_width) and not self.is_temp_dead:
            self.animation_timer = 0
        try:
            self.image = pygame.Surface.subsurface(self.current_image, (
                0 + self.frame_width * int(self.animation_timer),
                0,
                self.frame_width, self.current_image.get_height()))
            self.image = pygame.transform.scale(self.image,
                                                (150, int(150 * self.image.get_height() / self.image.get_width())))
            surface.blit(self.image, (self.x - progression, self.y))
        except Exception as e:
            print(e)


        # Draw name
        name_surface = PIX_FONT.render(self.name, True, (255, 255, 255))
        surface.blit(name_surface, (self.x - progression, self.y + self.top_padding / 2))

        if self.is_temp_dead:
            pygame.draw.rect(surface, (255, 0, 0), (self.x - progression, self.y, 100,10), 2)
            pygame.draw.rect(surface, (255, 0, 0), (self.x - progression, self.y, int(100 * self.dead_timer / self.dead_time), 10))

        if ACTIVE_HITBOXES:
            pygame.draw.rect(surface, (255, 0, 0), (self.x + self.side_padding - progression, self.y + self.top_padding, self.image.get_width() - self.side_padding*2, self.image.get_height() - self.top_padding), 2)

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
            surface.blit(
                pygame.transform.scale(JUMP_BOOST_ICON, (60, 60)),
                ((self.x if self.x < WIDTH / 2 else WIDTH / 2) + self.side_padding, self.y))  # above player

    def collide(self, platforms, delta_time):
        found_bot = False
        for platform in platforms:
            if platform.collide(self) and self.is_falling and self.y_velocity > 0 and abs(
                    self.y + self.image.get_height() - platform.y) < 30:
                self.stop_fall(platform.y)
                found_bot = True
                if isinstance(platform, JumpPad):
                    self.jump_multiplier = platform.jump_multiplier
                    self.jump_boost = True
                    platform.used = True
            if platform.collide(self) and platform.y < self.y + self.image.get_height() < platform.y + platform.height and self.speed < 0:
                self.x -= self.speed * delta_time
            if platform.collide(self) and platform.y < self.y + self.image.get_height() < platform.y + platform.height and self.speed > 0:
                self.x -= self.speed * delta_time
            if platform.collide(self) and platform.y + platform.height > self.y + self.top_padding and self.y_velocity < 0:
                self.y_velocity = 0

        if not found_bot:
            self.fall()

    def pickelize(self):
        self.idle_sheet = [self.idle_sheet.get_size(),pygame.image.tostring(self.idle_sheet, "RGBA")]
        self.jump_sheet = [self.jump_sheet.get_size(),pygame.image.tostring(self.jump_sheet, "RGBA")]
        self.move_sheet = [self.move_sheet.get_size(),pygame.image.tostring(self.move_sheet, "RGBA")]
        self.dead_sheet = [self.dead_sheet.get_size(),pygame.image.tostring(self.dead_sheet, "RGBA")]
        self.dash_image = [self.dash_image.get_size(),pygame.image.tostring(self.dash_image, "RGBA")]
        self.image = [self.image.get_size(),pygame.image.tostring(self.image, "RGBA")]
        self.current_image = [self.current_image.get_size(),pygame.image.tostring(self.current_image, "RGBA")]

    def unpickelize(self):
        self.idle_sheet = pygame.image.fromstring(self.idle_sheet[1], self.idle_sheet[0],"RGBA")
        self.jump_sheet = pygame.image.fromstring(self.jump_sheet[1], self.jump_sheet[0],"RGBA")
        self.move_sheet = pygame.image.fromstring(self.move_sheet[1], self.move_sheet[0], "RGBA")
        self.dead_sheet = pygame.image.fromstring(self.dead_sheet[1], self.dead_sheet[0], "RGBA")
        self.dash_image = pygame.image.fromstring(self.dash_image[1], self.dash_image[0], "RGBA")
        self.image = pygame.image.fromstring(self.image[1], self.image[0], "RGBA")
        self.current_image = pygame.image.fromstring(self.current_image[1],self.current_image[0], "RGBA")


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

    def draw(self, surface: pygame.Surface, background_progression: int):
        if self.color is not None and self.x + self.width - background_progression > 0:
            pygame.draw.rect(surface, self.color, (self.x - background_progression, self.y, self.width, self.height))

        if ACTIVE_HITBOXES:
            s = PIX_FONT.render(str(self.x) + " " + str(self.y), True, (255, 255, 255))
            surface.blit(s, (self.x - background_progression + 20, self.y))
            pygame.draw.rect(surface, (255, 0, 0), (
            self.x - background_progression, self.y, self.width, self.height), 2)

class SpriteGroup:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.sprites = []

    def add(self, sprite):
        self.sprites.append(sprite)

    def update(self, dt):
        for sprite in self.sprites:
            sprite.update(dt)

    def draw(self, p_id, background_progression: int):
        for sprite in self.sprites:
            if sprite.id != p_id:
                sprite.draw_relative(self.surface, background_progression)
            else:
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
                pygame.transform.scale((JUMP_PAD if
                        not self.used or not self.is_finite else JUMP_PAD_USED),
                                       (self.width, self.height)),
                (self.x - background_progression, self.y))


class Renderer:

    def __init__(self, screen: pygame.Surface, background_image: Image):
        self.screen = screen
        self.sprites = SpriteGroup(self.screen)
        self.background = background_image
        self.background_progression = 0
        self.dt = 0
        self.prev_time = 0
        self.children = []
        self.platforms = []
        self.bullets = []

        self.player_id = None
        self.game_started = False
        self.game_over = False

        # Init global assets
        self.load_global_assets(True)


    def load_global_assets(self, use_convert_alpha: bool):
        # Init global assets
        global PIX_FONT, JUMP_PAD, JUMP_PAD_USED, JUMP_BOOST_ICON
        PIX_FONT = pygame.font.Font('resources\\fonts\\yoster-island\\yoster.ttf', 25)
        if use_convert_alpha:
            # Buildings
            JUMP_PAD = pygame.image.load("resources/special/jump_pad_crystalized.png").convert_alpha()
            JUMP_PAD_USED = pygame.image.load('resources/special/used_pad.png').convert_alpha()

            # Icons
            JUMP_BOOST_ICON = pygame.image.load('resources/icons/jump_boost.png').convert_alpha()
        else:
            JUMP_PAD = pygame.image.load("resources/special/jump_pad_crystalized.png").convert()
            JUMP_PAD_USED = pygame.image.load('resources/special/used_pad.png').convert()

            # Icons
            JUMP_BOOST_ICON = pygame.image.load('resources/icons/jump_boost.png').convert()

    def render_all(self, mouse_pos: tuple):
        self.background.x = -self.background_progression
        self.background.render(self.screen)
        if self.background.faded_out:
            self.background.faded_out = False
            self.background.is_fading_out = False
            self.background.is_fading_in = True
            self.background = self.background.replace_image
            self.background.replace_image = None
        if self.game_started:
            for platform in self.platforms:
                platform.draw(self.screen, self.background_progression)
        for child in self.children:

            if isinstance(child, Button):
                child.render(self.screen,
                             child.x < mouse_pos[0] < child.x + child.width and child.y < mouse_pos[
                                 1] < child.y + child.height)
            elif isinstance(child, JumpPad):
                child.render(self.screen, self.background_progression)
            else:
                child.render(self.screen)
        if self.game_started:
            self.sprites.draw(self.player_id, self.background_progression)
            for bullet in self.bullets:
                bullet.render(self.screen, self.background_progression)

    def update_all(self):
        if self.game_started:
            self.sprites.update(self.dt)
            for sprite in self.sprites.get_sprites():
                if sprite.id == self.player_id:
                    sprite.collide(self.platforms, self.dt)
                if sprite.y + sprite.image.get_height() > self.background.get_size()[1] - 170 and sprite.id != self.player_id:
                    sprite.is_temp_dead = True
                if sprite.revived and sprite.id != self.player_id:
                    sprite.revived = False
            for bullet in self.bullets:
                bullet.update(self.dt)
            for bullet in self.bullets:
                if bullet.x - bullet.orig_x > bullet.travel_max or bullet.x < 0 or bullet.x > self.background.get_size()[0] or bullet.y < 0 or bullet.y > self.background.get_size()[1] or bullet.collide(self.platforms):
                    self.bullets.remove(bullet)
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

    def add_bullet(self, x, y, vel_x, vel_y, x2, y2, rad, isplayer, vel_mult=200):
        self.bullets.append(Bullet(x, y, vel_x, vel_y, rad, (255, 255, 255), (x2, y2), 2000, isplayer, vel_mult,self.background_progression))

    def add_bullet_from_obj(self, bull):
        self.bullets.append(bull)

    def update_dt(self):
        t = pygame.time.get_ticks()
        self.dt = (t - self.prev_time) / 1000.0
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

    def update_player_coords(self, p_id, x, y):
        for sprite in self.sprites.get_sprites():
            if str(sprite.id) == str(p_id):
                sprite.animate(x, y)
                sprite.x = x
                sprite.y = y
                break

    def has_child(self, c):
        for child in self.children:
            if child == c:
                return True
        return False


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
