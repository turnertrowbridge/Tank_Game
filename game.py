import pygame
from enemy import Enemy
from player import Player


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.player = Player(100, 100)
        self.enemies = [Enemy(300, 300), Enemy(500, 500)]
        self.start_time = pygame.time.get_ticks()
        self.game_over = False
        self.game_over_time = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            self.player.handle_events(event)
        return True

    def draw(self):
        if not self.game_over:
            self.draw_game()
        else:
            self.show_game_over_screen()

    def draw_game(self):
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

        # Draw timer
        self.draw_timer()

        # Display lives and game over if player has no lives
        self.update_lives()

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

    def draw_timer(self):
        # Draw timer
        timer = pygame.time.get_ticks() - self.start_time
        timer_surf = self.font.render(
            str(timer // 1000) + " seconds", True, (0, 0, 0))
        self.screen.blit(timer_surf, (self.screen.get_width() // 2, 10))

    def update_lives(self):
        lives_surf = self.font.render(
            "Lives: " + str(self.player.lives), True, (0, 0, 0))
        self.screen.blit(lives_surf, (10, 40))

        if self.player.lives <= 0:
            if not self.game_over:
                self.game_over_time = (
                    pygame.time.get_ticks() - self.start_time) // 1000
                self.game_over = True

    def show_game_over_screen(self):
        game_over_surf = pygame.Surface((400, 300))
        game_over_surf.fill((255, 255, 255))
        game_over_surf.set_alpha(200)

        title_font = pygame.font.Font(None, 64)
        title_surf = title_font.render('Game Over', True, (0, 0, 0))
        game_over_surf.blit(title_surf, (100, 20))

        stats_font = pygame.font.Font(None, 32)
        stats_surf = stats_font.render('Match Stats', True, (0, 0, 0))
        game_over_surf.blit(stats_surf, (100, 80))

        time_surf = stats_font.render(
            'Time Survived: ' + str(self.game_over_time), True, (0, 0, 0))
        game_over_surf.blit(time_surf, (100, 120))

        enemies_destroyed_surf = stats_font.render(
            'Enemies Destroyed: ' + str(self.player.score), True, (0, 0, 0))
        game_over_surf.blit(enemies_destroyed_surf, (100, 160))

        projectiles_surf = stats_font.render('Enemies Destroyed by Projectiles: ' + str(
            self.player.destroys_with_projectiles), True, (0, 0, 0))
        game_over_surf.blit(projectiles_surf, (100, 200))

        mines_surf = stats_font.render(
            'Enemies Destroyed by Mines: ' + str(self.player.destroys_with_projectiles), True, (0, 0, 0))
        game_over_surf.blit(mines_surf, (100, 240))

        self.screen.blit(game_over_surf, (100, 100))

        pygame.display.flip()
