import pygame
from setup import WIDTH, HEIGHT, WHITE_COLOR, RED_COLOR, BLOCK_SIZE, OBSTACLE_SIZE, OBSTACLE_SHAPE
from scripts import Text, Audio
from random import choice, randint

class Player(pygame.sprite.Sprite):
    def __init__(self, group, collision):
        super().__init__(group)
        self.attributes = {"image": pygame.image.load("../graphics/player.png").convert_alpha(),
                           "alive": True,
                           "lives": 3,
                           "speed": 300,
                           "score": 0,
                           "ready": True,
                           "pos_i": (WIDTH // 2, HEIGHT - 5)}

        self.image = self.attributes["image"]
        self.rect = self.image.get_rect(midbottom = self.attributes["pos_i"])
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.move = 0

        self.laser = {"group": pygame.sprite.Group(),
                      "direction": -1,
                      "timer": 0,
                      "reload": 500}

        self.group = {"obstacle": collision[0],
                      "alien": collision[1],
                      "extra": collision[2]}

        self.win = pygame.display.get_surface()

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move = -1
        else:
            self.move = 0

        if keys[pygame.K_SPACE] and self.attributes["ready"]:
            self.shoot()

    def movement(self, dt):
        self.pos.x += self.move * self.attributes["speed"] * dt
        self.rect.x = round(self.pos.x)

    def constraint(self):
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.pos.x = self.rect.x
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x

    def shoot(self):
        Laser(self.rect.center, self.laser["direction"], self.laser["group"])
        self.attributes["ready"] = False
        self.laser["timer"] = pygame.time.get_ticks()

    def reload(self):
        current_time = pygame.time.get_ticks()

        if (current_time - self.laser["timer"]) >= self.laser["reload"]:
            self.attributes["ready"] = True

    def collision(self):
        for laser in self.laser["group"]:
            if pygame.sprite.spritecollide(laser, self.group["obstacle"], True):
                laser.kill()
            alien_hit = pygame.sprite.spritecollide(laser, self.group["alien"], True)
            if alien_hit:
                for alien in alien_hit:
                    Audio("../audio/explosion.wav").play()
                    self.attributes["score"] += alien.value
                    laser.kill()
            if pygame.sprite.spritecollide(laser, self.group["extra"], True):
                self.attributes["score"] += 500
                laser.kill()

    def display_surf(self):
        Text(f"Score: {self.attributes['score']}", (7, -10), "topleft")

        IMG_W = self.attributes["image"].get_width()
        for live in range(self.attributes["lives"] - 1):
            pos_x = (WIDTH - IMG_W) - (live * (IMG_W + 10)) - 10
            self.win.blit(self.attributes["image"], (pos_x, 10))

    def alive(self):
        if self.attributes["lives"] <= 0:
            self.attributes["alive"] = False

    def update(self, dt):
        self.input()
        self.movement(dt)
        self.constraint()
        self.laser["group"].update(dt)
        self.reload()
        self.collision()
        self.alive()

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, direction, group):
        super().__init__(group)
        Audio("../audio/laser.wav").play()
        
        self.image = pygame.Surface((4, 20))
        self.image.fill(WHITE_COLOR)
        self.rect = self.image.get_rect(center = pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.move = direction
        self.speed = 400

    def update(self, dt):
        self.pos.y += self.move * self.speed * dt
        self.rect.y = round(self.pos.y)

        if self.rect.top > WIDTH or self.rect.bottom < 0:
            self.kill()

class Block(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(RED_COLOR)
        self.rect = self.image.get_rect(topleft = pos)

class Obstacle:
    def __init__(self, amount, group):
        self.start_x = (WIDTH // amount - OBSTACLE_SIZE) // 2
        self.start_y = 480

        self.positions = [n * (WIDTH // amount) for n in range(amount)]
        self.obstacle = group

        self.create()

    def create(self):
        for offset_x in self.positions:
            for row_index, row in enumerate(OBSTACLE_SHAPE):
                for col_index, col in enumerate(row):
                    if col == "O":
                        pos_x = self.start_x + col_index * BLOCK_SIZE + offset_x
                        pos_y = self.start_y + row_index * BLOCK_SIZE

                        Block((pos_x, pos_y), self.obstacle)

class Alien(pygame.sprite.Sprite):
    def __init__(self, pos, color, group):
        super().__init__(group)
        self.image = pygame.image.load(f"../graphics/aliens/{color}.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.move = 1
        self.speed_i = 80
        self.speed = self.speed_i

        if color == "red":
            self.value = 300
        elif color == "yellow":
            self.value = 200
        else:
            self.value = 100

    def update(self, dt):
        self.pos.x += self.move * self.speed * dt
        self.rect.x = round(self.pos.x)

class Extra(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        info = choice(((-20, 1), (WIDTH + 20, -1)))

        self.image = pygame.image.load("../graphics/aliens/blue.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (info[0], 80))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.move = info[1]
        self.speed = 200

    def update(self, dt):
        self.pos.x += self.move * self.speed * dt
        self.rect.x = round(self.pos.x)

        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

class AlienSetup:
    def __init__(self, amount, group, collision):
        self.start_x, self.start_y = 70, 100
        self.distance_x, self.distance_y = 60, 48
        self.rows, self.cols = amount[0], amount[1]
        self.increase = 4

        self.group = {"alien": group[0],
                      "extra": group[1],
                      "laser": pygame.sprite.Group(),
                      "obstacle": collision[0],
                      "player": collision[1]}

        self.LASERTIMER = pygame.USEREVENT + 1
        pygame.time.set_timer(self.LASERTIMER, 1000)

        self.EXTRASPAWN = pygame.USEREVENT + 2
        pygame.time.set_timer(self.EXTRASPAWN, randint(6000, 8000))

        self.grid()

    def grid(self):
        for row_index, row in enumerate(range(self.rows)):
            for col_index, col in enumerate(range(self.cols)):
                pos_x = self.start_x + col_index * self.distance_x
                pos_y = self.start_y + row_index * self.distance_y

                if row_index == 0:
                    Alien((pos_x, pos_y), "red", self.group["alien"])
                elif 1 <= row_index <= 2:
                    Alien((pos_x, pos_y), "yellow", self.group["alien"])
                else:
                    Alien((pos_x, pos_y), "green", self.group["alien"])

    def position(self):
        for alien in self.group["alien"]:
            if alien.rect.right > WIDTH:
                self.movement(-1)
            if alien.rect.left < 0:
                self.movement(1)

    def movement(self, direction):
        for alien in self.group["alien"]:
            alien.move = direction
            alien.rect.y += 2
            alien.pos.y = alien.rect.y

    def shoot(self):
        aliens = []
        for alien in self.group["alien"]:
            aliens.append(alien)
            
        if aliens:
            alien = choice(aliens)
            Laser(alien.rect.center, 1, self.group["laser"])

    def increase_speed(self):
        aliens = []
        for alien in self.group["alien"]:
            aliens.append(alien)

        new_speed = ((self.rows * self.cols) - len(aliens)) * self.increase

        for alien in self.group["alien"]:
            alien.speed = alien.speed_i + new_speed

    def collision(self):
        for laser in self.group["laser"]:
            if pygame.sprite.spritecollide(laser, self.group["obstacle"], True):
                laser.kill()
            if pygame.sprite.spritecollide(laser, self.group["player"], False):
                laser.kill()
                self.group["player"].sprite.attributes["lives"] -= 1

        for alien in self.group["alien"]:
            pygame.sprite.spritecollide(alien, self.group["obstacle"], True)
            if pygame.sprite.spritecollide(alien, self.group["player"], False):
                self.group["player"].sprite.attributes["alive"] = False

    def spawn(self):
        Extra(self.group["extra"])

    def update(self, dt):
        self.position()
        self.increase_speed()
        self.collision()
        self.group["laser"].update(dt)
