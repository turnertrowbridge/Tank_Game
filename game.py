import pygame
from enemy import Enemy
from player import Player
import random


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.player = Player(100, 100)
        self.enemies = []
        self.start_time = pygame.time.get_ticks()
        self.game_state = "playing"
        self.game_over_time = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            self.player.handle_events(event)
        return True

    def draw(self):
        if self.game_state == "playing":
            self.draw_game()
        elif self.game_state == "game_over":
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

        # Randomly spawn enemies at a 3% chance each frame
        if random.randint(0, 100) < 3:
            self.spawn_enemy()

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
            if self.game_state == "playing":
                self.game_over_time = (
                    pygame.time.get_ticks() - self.start_time) // 1000
                self.game_state = "game_over"

    def spawn_enemy(self):
        # Randomly choose a side of the screen to spawn the enemy from
        side = random.choice(['top', 'bottom', 'left', 'right'])
        offscreen_offset = 80

        # Generate a random position and velocity for the enemy
        if side == 'top':
            x = random.randint(0, self.screen.get_width())
            y = -1 * offscreen_offset
        elif side == 'bottom':
            x = random.randint(0, self.screen.get_width())
            y = self.screen.get_height() + offscreen_offset
        elif side == 'left':
            x = -1 * offscreen_offset
            y = random.randint(0, self.screen.get_height())
        elif side == 'right':
            x = self.screen.get_width() + offscreen_offset
            y = random.randint(0, self.screen.get_height())

        # Create a new enemy and add it to the list of enemies
        enemy = Enemy(x, y)
        self.enemies.append(enemy)

    def show_game_over_screen(self):
        game_over_surf = pygame.Surface((580, 480))
        game_over_surf.fill((255, 255, 255))
        game_over_surf.set_alpha(200)

        background_surf = pygame.Surface(
            (game_over_surf.get_width() + 20, game_over_surf.get_height() + 20))
        background_surf.fill((0, 0, 0))

        title_font = pygame.font.Font(None, 64)
        title_surf = title_font.render('Game Over', True, (0, 0, 0))
        game_over_surf.blit(title_surf, (150, 20))

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
            'Enemies Destroyed by Mines: ' + str(self.player.destroys_with_mines), True, (0, 0, 0))
        game_over_surf.blit(mines_surf, (100, 240))

        # Calculate the center of the screen
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        # Calculate the top-left position of the game over surface
        game_over_x = 10
        game_over_y = 10

        background_surf.blit(game_over_surf, (game_over_x, game_over_y))

        # Create a play again button
        play_again_font = pygame.font.Font(None, 48)
        play_again_surf = play_again_font.render(
            'Play Again', True, (255, 255, 0))
        play_again_x = background_surf.get_width() // 2 - play_again_surf.get_width() // 2
        play_again_y = background_surf.get_height() - play_again_surf.get_height() - 20
        background_surf.blit(play_again_surf, (play_again_x, play_again_y))

        # Calculate the top-left position of the background surface
        background_x = center_x - background_surf.get_width() // 2
        background_y = center_y - background_surf.get_height() // 2
        self.screen.blit(background_surf, (background_x, background_y))

        play_again_button = pygame.Rect(background_x + play_again_x, background_y +
                                        play_again_y, play_again_surf.get_width(), play_again_surf.get_height())

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_again_button.collidepoint(mouse_pos):
                        waiting = False
                        # Temporarily reset the game solution
                        self.__init__(self.screen)
