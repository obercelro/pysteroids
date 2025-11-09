import pygame
from constants import *
from logger import log_state
from player import Player

def main():
    print("Starting Asteroids!")
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)

    while pygame.get_init():
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.Surface.fill(screen, color = "black")
        player.update(dt)
        player.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        dt = clock.get_time() / 1000
        
if __name__ == "__main__":
    main()
