import pygame
import math
from projectile import Projectile
from enemy import Enemy
from mine import Mine


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.SPEED = 3
        self.player = pygame.Rect(100, 100, 50, 50)
        self.player_aim = pygame.Rect(0, 0, 50, 10)
        self.projectiles = []
        self.MAX_PROJECTILES = 5
        self.font = pygame.font.Font(None, 36)
        self.enemies = [Enemy(300, 300), Enemy(500, 500)]
        self.score = 0
        self.mines = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and len(self.projectiles) < self.MAX_PROJECTILES:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - self.player.centerx
                dy = mouse_y - self.player.centery
                angle = math.degrees(math.atan2(-dy, dx))
                projectile = Projectile(self.player.centerx + math.cos(math.radians(angle)) * (self.player_aim.width // 2),
                                        self.player.centery - math.sin(math.radians(angle)) * (self.player_aim.width // 2), angle)
                self.projectiles.append(projectile)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and len(self.mines) < 3:
                self.mines.append(Mine(self.player.centerx, self.player.centery))

        return True

    def draw(self):
        # Make screen white
        self.screen.fill((255, 255, 255))

        # Handle player movement
        self.handle_movements()

        # Update game state
        self.update()

        # Draw player
        self.draw_player()

        # Draw enemies
        self.draw_projectile_counter()

        # Draw core
        self.draw_score()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.delay(1000 // 60)

    def draw_score(self):
        score_surf = self.font.render(
            str(self.score) + " enemies destroyed", True, (0, 0, 0))
        self.screen.blit(score_surf, (10, 10))

    def draw_projectile_counter(self):
        # Draw projectile counter
        counter_surf = self.font.render(
            str(self.MAX_PROJECTILES - len(self.projectiles)), True, (0, 0, 0))
        self.screen.blit(counter_surf, (self.screen.get_width() - 30, 10))

    def handle_movements(self):
        # Move player with WASD keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.y -= self.SPEED
        if keys[pygame.K_a]:
            self.player.x -= self.SPEED
        if keys[pygame.K_s]:
            self.player.y += self.SPEED
        if keys[pygame.K_d]:
            self.player.x += self.SPEED

    def update(self):
        self.update_enemies()
        self.update_projectiles()
        self.update_mines()

    def update_enemies(self):
        # Update and draw/destroy enemies
        for enemy in self.enemies[:]:
            enemy.update(self.player)
            enemy.draw(self.screen, self.player)
            for projectile in enemy.projectiles[:]:
                if self.player.colliderect(projectile.rect):
                    self.__init__(self.screen)
            for player_projectile in self.projectiles[:]:
                if player_projectile.rect.colliderect(enemy.rect):
                    self.enemies.remove(enemy)
                    self.projectiles.remove(player_projectile)
                    self.score += 1  # Update score when enemy is destroyed

    def update_projectiles(self):
        # Update and draw projectiles
        for projectile in self.projectiles[:]:
            projectile.update()
            # Remove projectile if it goes off screen
            if not self.screen.get_rect().colliderect(projectile.rect):
                self.projectiles.remove(projectile)
            else:
                # Draw the projectile
                projectile.draw(self.screen)

    def update_mines(self):
        for mine in self.mines[:]:
            mine.update()
            mine.draw(self.screen)
            if mine.exploded:
                for enemy in self.enemies[:]:
                    if math.hypot(enemy.rect.centerx - mine.rect.centerx, enemy.rect.centery - mine.rect.centery) < 50:
                        try:
                            # Remove enemy if it is within the blast radius
                            self.enemies.remove(enemy)
                        except ValueError:  # If enemy is already removed, ignore
                            pass
                        self.score += 1
                if math.hypot(self.player.centerx - mine.rect.centerx, self.player.centery - mine.rect.centery) < 50:
                    self.__init__(self.screen)
                try:
                    self.mines.remove(mine)
                except ValueError:
                    pass

    def draw_player(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate angle between player and mouse
        dx = mouse_x - self.player.centerx
        dy = mouse_y - self.player.centery
        angle = math.degrees(math.atan2(-dy, dx))

        pygame.draw.rect(self.screen, (255, 0, 0), self.player)

        # Draw the player aim
        aim_length = 50
        surf = pygame.Surface(
            (aim_length, self.player_aim.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, (0, 255, 0),
                         (0, 0, aim_length, self.player_aim.height))
        surf = pygame.transform.rotate(surf, angle)

        # Calculate new pivot point
        offset_x = math.cos(math.radians(angle)) * (aim_length // 2)
        offset_y = -math.sin(math.radians(angle)) * (aim_length // 2)

        aim_rect = surf.get_rect(
            center=(self.player.centerx + offset_x, self.player.centery + offset_y))
        self.screen.blit(surf, aim_rect)
