import pygame
from setup import WIDTH, HEIGHT, BLACK_COLOR
from scripts import Text, Audio
from sprites import Player, Obstacle, AlienSetup

pygame.init()

class GameState:
    def __init__(self):
        self.state = "open"
        self.press = False

        Audio("../audio/music.wav").play(-1, 0.2)

        self.player = pygame.sprite.GroupSingle()
        self.obstacle = pygame.sprite.Group()
        self.alien = pygame.sprite.Group()
        self.extra = pygame.sprite.GroupSingle()

        self.spr_player = Player(self.player, [self.obstacle, self.alien, self.extra])
        self.spr_obstacle = Obstacle(4, self.obstacle)

        self.alien_setup = AlienSetup((6, 8), [self.alien, self.extra], [self.obstacle, self.player])

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            if self.state == "main":
                if event.type == self.alien_setup.LASERTIMER:
                    self.alien_setup.shoot()
                if not self.alien_setup.group["extra"]:
                    if event.type == self.alien_setup.EXTRASPAWN:
                        self.alien_setup.spawn()

    def display_over_surf(self):
        if not self.spr_player.attributes["alive"]:
            Text("Game Over", (WIDTH // 2, HEIGHT // 2 - 40))
            Text(f"Score: {self.spr_player.attributes['score']}", (WIDTH // 2, HEIGHT // 2))
            Text("Press ENTER to play again", (WIDTH // 2, HEIGHT // 2 + 40))
        if not self.alien:
            Text("You Win", (WIDTH // 2, HEIGHT // 2 - 40))
            Text(f"Score: {self.spr_player.attributes['score']}", (WIDTH // 2, HEIGHT // 2))
            Text("Press ENTER to play again", (WIDTH // 2, HEIGHT // 2 + 40))

    def reset_key(self):
        keys = pygame.key.get_pressed()

        if self.state == "open":
            if keys[pygame.K_RETURN] and self.state == "open":
                self.reset()

        if self.state == "over":
            if keys[pygame.K_RETURN] and not self.press:
                self.reset()

    def reset(self):
        self.spr_player.laser["group"].empty()
        
        self.obstacle.empty()
        
        self.alien.empty()
        self.extra.empty()
        self.alien_setup.group["laser"].empty()

        self.spr_obstacle.create()
        self.alien_setup.grid()
        
        self.spr_player.rect.midbottom = self.spr_player.attributes["pos_i"]
        self.spr_player.pos.x = self.spr_player.rect.x
        
        self.spr_player.attributes["score"] = 0
        self.spr_player.attributes["lives"] = 3
        self.spr_player.attributes["alive"] = True
        
        self.state = "main"
        self.press = True

    def open(self, win):
        win.fill(BLACK_COLOR)

        self.spr_player.laser["group"].empty()
        
        self.obstacle.empty()
        
        self.alien.empty()
        self.extra.empty()
        self.alien_setup.group["laser"].empty()

        Text("Press ENTER to play", (WIDTH // 2, HEIGHT // 2))

        self.reset_key()

    def main(self, win, dt):
        self.press = False
        
        self.player.update(dt)
        self.alien.update(dt)
        self.extra.update(dt)
        self.alien_setup.update(dt)

        win.fill(BLACK_COLOR)

        self.player.sprite.laser["group"].draw(win)
        self.player.draw(win)
        self.player.sprite.display_surf()

        self.obstacle.draw(win)

        self.alien_setup.group["laser"].draw(win)
        self.alien.draw(win)
        self.extra.draw(win)

        if not self.spr_player.attributes["alive"] or not self.alien:
            self.state = "over"

    def over(self, win, dt):
        win.fill(BLACK_COLOR)
        
        self.player.sprite.laser["group"].draw(win)
        self.player.draw(win)

        self.obstacle.draw(win)
        self.extra.draw(win)

        self.display_over_surf()

        self.reset_key()

    def game_state(self, win, dt):
        self.events()

        if self.state == "open":
            self.open(win)
        if self.state == "main":
            self.main(win, dt)
        if self.state == "over":
            self.over(win, dt)
