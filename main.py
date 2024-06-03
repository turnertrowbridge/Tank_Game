import pygame
from game import Game


def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    WIDTH, HEIGHT = 1600, 1200
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Create a Game instance
    game = Game(screen)

    # Game loop
    running = True
    while running:
        running = game.handle_events()
        game.draw()

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
