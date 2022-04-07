# Space Invaders by @Ludov1kyyy

import pygame
from sys import exit
from time import perf_counter
from setup import WINSIZE
from scripts import CRT
from states import GameState

class Game:
    def __init__(self):
        pygame.init()
        self.pf = perf_counter()
        self.win = pygame.display.set_mode(WINSIZE)
        self.CRT = CRT()
        self.state = GameState()
        pygame.display.set_caption("Space Invaders")

    def run(self):
        while True:
            dt = perf_counter() - self.pf
            self.pf = perf_counter()

            self.state.game_state(self.win, dt)
            self.CRT.draw(self.win)

            pygame.display.update()

game = Game()

if __name__ == "__main__":
    game.run()
