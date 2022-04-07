WINSIZE = WIDTH, HEIGHT = 600, 600

BLACK_COLOR = (24, 24, 24)
WHITE_COLOR = (200, 200, 200)
RED_COLOR = (241, 79, 80)

OBSTACLE_SHAPE = ["  OOOOOOO  ",
                  " OOOOOOOOO ",
                  "OOOOOOOOOOO",
                  "OOOOOOOOOOO",
                  "OOOOOOOOOOO",
                  "OOO     OOO",
                  "OO       OO"]

BLOCK_SIZE = 6

OBSTACLE_SIZE = max([len(row) for row in OBSTACLE_SHAPE]) * BLOCK_SIZE
