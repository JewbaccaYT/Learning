import pygame
import random
import math
import copy
import angles
pygame.font.init()
pygame.mixer.init()


def get_arial(size):
    return pygame.font.SysFont("Arial", size)


def DistanceCalc(a, b):
    distance = math.sqrt(((a[0] - b[0])**2) + (a[1] - b[1])**2)
    return distance


# Scales a set of coordinates to the current screen size based on a divisor factor
def cscale(*coordinate, divisor=900):
    if len(coordinate) > 1:
        return tuple([int(coordinate[x] / divisor * SCREEN_SIZE[x % 2]) for x in range(len(coordinate))])
    else:
        return int(coordinate[0] / divisor * SCREEN_SIZE[0])


# Scales a set of coordinates to the current screen size based on a divisor factor. Doesn't return integers
def posscale(*coordinate, divisor=900):
    if len(coordinate) > 1:
        return tuple([coordinate[x] / divisor * SCREEN_SIZE[x] for x in range(len(coordinate))])
    else:
        return coordinate[0] / divisor * SCREEN_SIZE[0]


class GameManager:
    def __init__(self):
        self.SPRITES = []

        # queue lists for new and removed sprites
        self.sprite_add_queue = []
        self.sprite_remove_queue = []

        self.game_over = False
        self.win = False

        self.generate_level()

    def generate_level(self):
        enemyNum = random.randint(1, 15)

        self.add_sprite(Player(None, 3, {}, SHIP_IMAGE, [400, 400], [0, 0], health=enemyNum * 3))

        [self.add_sprite(Enemy(None, 2, {}, TURRET_IMAGE,
                               [random.randint(1, SCREEN_SIZE[0]) for _ in range(2)],
                               random.randint(-1000, 1000) / 100,
                               random.randint(1, 200),
                               health=random.randint(3, 15))) for _ in range(enemyNum)]

    # Run on every loop iteration
    def play(self, screen, update_lock):
        enemies = []
        player = None
        pbullets = []
        ebullets = []

        # Runs the inherited method of each sprite
        for sprite in self.SPRITES:
            self.update_sprite(sprite)
            sprite.run_sprite(screen, update_lock, self)

            if "enemy" in sprite.tags:
                enemies.append(sprite)
            elif "PBullet" in sprite.tags:
                pbullets.append(sprite)
            elif "EBullet" in sprite.tags:
                ebullets.append(sprite)
            elif "player" in sprite.tags:
                player = sprite

        # Runs collision shit
        if player is not None:
            [player.collideBullet(b, self) for b in ebullets]
            [player.collideEnemy(e, self) for e in enemies]

            self.game_over = False
        else:
            screen.blit(GAMEOVER, GAMEOVER.get_rect(center=(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)))
            self.game_over = True

        [[e.collide(b, self) for b in pbullets] for e in enemies]

        if not len(enemies):
            self.win = True
            screen.blit(YOUWIN, YOUWIN.get_rect(center=(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)))
        else:
            self.win = False

        self.update_sprites_list()

    # Removes dead sprites, sorts, adds new sprites
    def update_sprites_list(self):
        # Removes sprites queued for removal
        for remove_sprite in self.sprite_remove_queue:
            if remove_sprite in self.SPRITES:
                self.SPRITES.remove(remove_sprite)

        if len(self.sprite_add_queue):
            # Adds new sprites
            for add_sprite in self.sprite_add_queue:
                self.SPRITES.append(add_sprite)

            # Resorts sprites based on their z_order
            self.SPRITES = sorted(self.SPRITES, key=lambda spr: spr.z_order)

        self.sprite_remove_queue = []
        self.sprite_add_queue = []

    def update_sprite(self, sprite):
        # Updates lifetime
        if sprite.lifetime is not None:
            sprite.lifetime -= 1

        # Queues dead sprites for removal
        if sprite.kill or (sprite.lifetime is not None and sprite.lifetime <= 0):
            self.sprite_remove_queue.append(sprite)

    # Add new sprite to queue
    def add_sprite(self, sprite):
        self.sprite_add_queue.append(sprite)

    def remove_sprite(self, sprite):
        self.sprite_remove_queue.append(sprite)


class Object:
    def __init__(self, lifetime, z_order, tags):
        self.lifetime = lifetime
        self.kill = False

        # Draw order
        self.z_order = z_order

        # Set of string tags that can identify an object
        self.tags = set(tags)

    @staticmethod
    def rotate(image, rect, angle):
        """Rotate the image while keeping its center."""
        # Rotate the original image without modifying it.
        new_image = pygame.transform.rotate(image, angle)
        # Get a new rect with the center of the old rect.
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect

    # screen = surface of choice, update_lock = pause game
    def run_sprite(self, screen, update_lock, game_manager):
        pass


class Explosion(Object):
    def __init__(self, lifetime, z_order, tags, sheet_dimensions, animation_speed, sheet, center, frame_count):
        # If none is entered for lifetime, the lifetime is set to -1 iteration of the animation
        if lifetime == -1:
            life = frame_count * animation_speed - 1
        else:
            life = lifetime
        super().__init__(life, z_order, tags)

        # The dimensions of the sprite sheet by frame count (width, height)
        self.sheet_dimensions = sheet_dimensions
        # The amount of game ticks that should pass between each frame
        self.animation_speed = animation_speed

        self.sheet_frames_w = sheet_dimensions[0]
        self.sheet_frames_h = sheet_dimensions[1]

        # The sprite sheet image
        self.sheet = sheet
        # Dimensions of an individual frame
        self.frame_width = self.sheet.get_width() / self.sheet_frames_w
        self.frame_height = self.sheet.get_height() / self.sheet_frames_h

        # Center position of the animation
        self.pos = center

        # Counts the ticks. Used for reference in the animation calculations
        self.tick = 0
        # Gives the current frame number
        self.frame = 1
        # Gets the vertical and horizontal frame coordinates to point to the current frame
        self.frame_pos = [0, 0]
        # Total # of frames in sheet
        self.frame_count = frame_count

        # Surface onto which the animation will be drawn
        self.surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA, 32)
        # Calls update once to blit the first frame and resets the tick
        self.surface.blit(self.sheet, (0, 0))

    def run_sprite(self, screen, update_lock, game_manager):
        if not update_lock:
            self.update()
        self.draw_sprite(screen)

    def update(self):
        # Updates
        if self.tick % self.animation_speed == 0:
            # Calculates the sheet position of frame
            horizontal_pos = self.frame % self.sheet_frames_w  # 8 // 8 = 1
            self.frame_pos = ((horizontal_pos if not horizontal_pos == 0 else self.frame_count) - 1,
                              ((self.frame - 1) // self.sheet_frames_w))

            # Clears surface
            self.surface.fill((255, 255, 255, 0))

            # Resets frame when it finishes cycling the sheet
            self.frame += 1
            if self.frame > self.frame_count:
                self.frame = 1

            # Shifts the sheet accordingly and blits the frame onto the surface
            self.surface.blit(self.sheet,
                              (-self.frame_pos[0] * self.frame_width, -self.frame_pos[1] * self.frame_height))

        self.tick += 1

    def draw_sprite(self, screen):
        # Blits surface onto screen
        screen.blit(self.surface, (self.pos[0] - self.frame_width / 2, self.pos[1] - self.frame_height / 2))


class Player(Object):
    def __init__(self, lifetime, z_order, tags, image, pos, velocity, health=10):
        super().__init__(lifetime, z_order, tags)

        self.tags.add("player")

        self.health = health

        self.original_image = image

        self.image = copy.copy(self.original_image)
        self.rect = self.image.get_rect()

        self.pos = pos
        self.velocity = velocity

        self.angle = 0
        self.angle_vel = []

        self.accel = False
        self.deccel = False

        self.shooting = False
        self.rate_of_fire = 5
        self.shoot_tick = 0

        self.damageCooldown = 0

    def run_sprite(self, screen, update_lock, game_manager):
        if not update_lock:
            self.update(game_manager)
        self.draw(screen)

    def update(self, game_manager):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.accel = True

                if event.key == pygame.K_DOWN:
                    self.deccel = True

                if event.key == pygame.K_RIGHT:
                    self.angle_vel.append(-3)

                if event.key == pygame.K_LEFT:
                    self.angle_vel.append(3)

                if event.key == pygame.K_SPACE:
                    self.shoot_tick = 0
                    self.shooting = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.accel = False

                if event.key == pygame.K_RIGHT:
                    self.angle_vel.remove(-3)

                if event.key == pygame.K_LEFT:
                    self.angle_vel.remove(3)

                if event.key == pygame.K_DOWN:
                    self.deccel = False

                if event.key == pygame.K_SPACE:
                    self.shooting = False

        if self.shooting:
            if self.shoot_tick % self.rate_of_fire == 0:
                self.ShootyShoot(game_manager)

            self.shoot_tick += 1

        if self.health <= 0:
            game_manager.remove_sprite(self)

        # Updates angle based on velocity and rotates image
        if len(self.angle_vel):
            self.angle += self.angle_vel[-1]
            self.image, self.rect = self.rotate(self.original_image, self.rect, self.angle)

        # Updates speed if accelerating
        if self.accel:
            self.velocity[0] += math.cos(math.radians(self.angle)) * 0.2
            self.velocity[1] += -math.sin(math.radians(self.angle)) * 0.2
        if self.deccel:
            self.velocity = [i*.9 for i in self.velocity]
        # Updates position
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.pos[0] %= SCREEN_SIZE[0]
        self.pos[1] %= SCREEN_SIZE[1]

        if self.damageCooldown > 0:
            self.damageCooldown -= 1

    def draw(self, screen):
        self.rect.center = self.pos
        screen.blit(self.image, self.rect)

        for i in range(self.health):
            screen.blit(HEART_IMAGE, (i * HEART_IMAGE.get_width() * 1.2 + 10, 10))

    def ShootyShoot(self, game_manager):
        spread = random.randint(-8000, 8000) / 1000

        game_manager.add_sprite(Bullet(1, {"PBullet"}, BULLET_IMAGE, copy.copy(self.pos),
                                    [self.velocity[0] + math.cos(math.radians(self.angle + spread)) * 13,
                                     self.velocity[1] + -math.sin(math.radians(self.angle + spread)) * 13]))

    def takeDamage(self, game_manager):
        if self.damageCooldown == 0:
            self.health -= 1
            game_manager.add_sprite(Explosion(-1, 5, {}, (8, 1), 5, EXPLODE_IMAGE, copy.copy(self.pos), 8))
            sound = pygame.mixer.Sound("sounds/Explode1.wav")
            sound.set_volume(.05)
            sound.play()

    def collideEnemy(self, sprite, game_manager):
        d_check = DistanceCalc(self.pos, sprite.pos)
        if d_check <= self.rect.width / 2.1 + sprite.rect.width / 2.1:
            sprite.takeDamage(game_manager)
            self.takeDamage(game_manager)
            if self.damageCooldown == 0:
                self.damageCooldown = 40
            if sprite.damageCooldown == 0:
                sprite.damageCooldown = 40
            sprite.show_health = 100

    def collideBullet(self, sprite, game_manager):
        d_check = DistanceCalc(self.pos, sprite.pos)
        if d_check <= self.rect.width / 2.1 + sprite.rect.width / 2.1:
            self.takeDamage(game_manager)
            game_manager.remove_sprite(sprite)


class Enemy(Object):
    def __init__(self, lifetime, z_order, tags, image, pos, angle_vel, rof, health=50):
        super().__init__(lifetime, z_order, tags)

        self.health = health

        self.tags.add("enemy")

        self.original_image = image

        self.image = copy.copy(self.original_image)
        self.rect = self.image.get_rect()

        self.pos = pos

        self.angle = 0
        self.angle_vel = angle_vel

        self.TURRET_OFFSET = 0.17 * self.original_image.get_width()

        self.tick = 0
        self.shoot_every_tick = rof

        self.damageCooldown = 0

        self.show_health = 0

    def run_sprite(self, screen, update_lock, game_manager):
        if not update_lock:
            self.update(game_manager)
        self.draw(screen)

    def update(self, game_manager):
        if not self.angle_vel == 0:
            self.angle += self.angle_vel
            self.image, self.rect = self.rotate(self.original_image, self.rect, self.angle)

        if self.tick % self.shoot_every_tick == 0:
            self.ShootyShoot(game_manager)

        if self.damageCooldown > 0:
            self.damageCooldown -= 1

        if self.show_health > 0:
            self.show_health -= 1

        if self.health <= 0:
            game_manager.remove_sprite(self)

        self.tick += 1

    def draw(self, screen):
        self.rect.center = self.pos
        screen.blit(self.image, self.rect)

        if self.show_health > 0:
            offset = self.pos[0] - (HEART_TRANS_IMAGE.get_width() * 0.4 * self.health) / 2

            for i in range(self.health):
                screen.blit(HEART_TRANS_IMAGE, (offset + (i * 0.4 * HEART_TRANS_IMAGE.get_width()), self.pos[1] + self.rect.height / 2))

    def ShootyShoot(self, game_manager):
        game_manager.add_sprite(Bullet(1, {"EBullet"}, BULLET_IMAGE,
                                       [self.pos[0] + self.TURRET_OFFSET * math.cos(math.radians(self.angle + 90)),
                                        self.pos[1] - self.TURRET_OFFSET * math.sin(math.radians(self.angle + 90))],
                                       [math.cos(math.radians(self.angle)) * 10,
                                        -math.sin(math.radians(self.angle)) * 10]))

        game_manager.add_sprite(Bullet(1, {"EBullet"}, BULLET_IMAGE,
                                       [self.pos[0] + self.TURRET_OFFSET * math.cos(math.radians(self.angle - 90)),
                                        self.pos[1] - self.TURRET_OFFSET * math.sin(math.radians(self.angle - 90))],
                                       [math.cos(math.radians(self.angle)) * 10,
                                        -math.sin(math.radians(self.angle)) * 10]))

    def takeDamage(self, game_manager):
        if self.damageCooldown == 0:
            self.health -= 1
            game_manager.add_sprite(Explosion(-1, 5, {}, (8, 1), 5, EXPLODE_IMAGE, copy.copy(self.pos), 8))
            sound = pygame.mixer.Sound("sounds/Explode1.wav")
            sound.set_volume(.05)
            sound.play()

    def collide(self, sprite, game_manager):
        d_check = DistanceCalc(self.pos, sprite.pos)
        if d_check <= self.rect.width / 2.1 + sprite.rect.width / 2.1:
            self.takeDamage(game_manager)
            self.show_health = 100
            game_manager.remove_sprite(sprite)


class Bullet(Object):
    def __init__(self, z_order, tags, image, pos, velocity):
        super().__init__(100, z_order, tags)

        self.tags.add("bullet")

        self.pos = pos
        self.velocity = velocity

        self.image = image
        self.rect = self.image.get_rect()

        # Updates the image and rect to make the bullet angled in the direction its moving
        if self.velocity[0] == 0:
            angle = 90 * (-1 if not self.velocity[1] < 0 else 1)
        else:
            angle = math.degrees(math.atan2(-self.velocity[1], self.velocity[0]))
        self.image, self.rect = self.rotate(self.image, self.rect, angle)

    def run_sprite(self, screen, update_lock, game_manager):
        if not update_lock:
            self.update()
        self.draw(screen)

    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.pos[0] %= SCREEN_SIZE[0]
        self.pos[1] %= SCREEN_SIZE[1]

    def draw(self, screen):
        # Draws image
        self.rect.center = self.pos
        screen.blit(self.image, self.rect)


# Variables
SCREEN_SIZE = (900, 900)
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
clock = pygame.time.Clock()
running = True

events = ()

EXPLODE_IMAGE = pygame.transform.smoothscale(pygame.image.load("images/explosivo.png"), cscale(800, 100)).convert_alpha()
BULLET_IMAGE = pygame.transform.flip(pygame.transform.smoothscale(pygame.image.load("images/bullet.png"), cscale(30, 5)), True, False).convert_alpha()
SHIP_IMAGE = pygame.transform.smoothscale(pygame.image.load("images/ship.png"), cscale(100, 80)).convert_alpha()
TURRET_IMAGE = pygame.transform.rotate(pygame.transform.smoothscale(pygame.image.load("images/alienturret.png"), cscale(80, 70)), -90).convert_alpha()
HEART_IMAGE = pygame.transform.smoothscale(pygame.image.load("images/heart.png"), cscale(20, 20)).convert_alpha()
HEART_TRANS_IMAGE = copy.copy(pygame.transform.scale(HEART_IMAGE, cscale(10, 10)))
HEART_TRANS_IMAGE.fill((255, 255, 255, 50), None, pygame.BLEND_RGBA_MULT)

GAMEOVER = get_arial(cscale(32)).render("GAME OVER (R to restart)", True, (255, 50, 50))
YOUWIN = get_arial(cscale(32)).render("YOUR IS WINER (R to restart)", True, (50, 255, 50))

GAME = GameManager()

# Game Loop
while running:
    screen.fill((0, 0, 0))

    events = pygame.event.get()

    GAME.play(screen, False)

    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if GAME.game_over or GAME.win:
                    GAME = GameManager()

    pygame.display.update()

    clock.tick(60)
    pygame.display.set_caption(str(clock.get_fps()))
