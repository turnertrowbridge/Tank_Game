import pygame
from enemy import Enemy
from player import Player


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.player = Player(100, 100)
        self.enemies = [Enemy(300, 300), Enemy(500, 500)]
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            self.player.handle_events(event)
        return True

    def draw(self):
        # Make screen white
        self.screen.fill((255, 255, 255))

        # Handle player movement
        self.player.handle_movements()

        # Remove enemies
        self.player.update_enemies(self.screen, self.enemies)

        # Update player
        self.player.update(self.screen, self.enemies)

        # Draw player
        self.player.draw(self.screen)

        # Draw projectile counter
        self.draw_projectile_counter()

        # Draw score
        self.draw_score()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.delay(1000 // 60)

    def draw_score(self):
        score_surf = self.font.render(
            str(self.player.score) + " enemies destroyed", True, (0, 0, 0))
        self.screen.blit(score_surf, (10, 10))

    def draw_projectile_counter(self):
        # Draw projectile counter
        counter_surf = self.font.render(
            str(self.player.MAX_PROJECTILES - len(self.player.projectiles)), True, (0, 0, 0))
        self.screen.blit(counter_surf, (self.screen.get_width() - 30, 10))

    def update(self):
        self.update_enemies()
