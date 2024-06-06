import pygame
import math
from projectile import Projectile
from mine import Mine


class Player:
    def __init__(self, x, y):
        self.model = pygame.Rect(x, y, 50, 50)
        self.model_aim = pygame.Rect(0, 0, 50, 10)
        self.SPEED = 5
        self.mines = []
        self.projectiles = []
        self.MAX_PROJECTILES = 5
        self.MAX_MINES = 3
        self.score = 0
        self.lives = 5
        self.destroys_with_projectiles = 0
        self.destroys_with_mines = 0

    def handle_movements(self):
        # Move model with WASD keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.model.y -= self.SPEED
        if keys[pygame.K_a]:
            self.model.x -= self.SPEED
        if keys[pygame.K_s]:
            self.model.y += self.SPEED
        if keys[pygame.K_d]:
            self.model.x += self.SPEED

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and len(self.projectiles) < self.MAX_PROJECTILES:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.model.centerx
            dy = mouse_y - self.model.centery
            angle = math.degrees(math.atan2(-dy, dx))
            projectile = Projectile(self.model.centerx + math.cos(math.radians(angle)) * (self.model_aim.width // 2),
                                    self.model.centery - math.sin(math.radians(angle)) * (self.model_aim.width // 2), angle)
            self.projectiles.append(projectile)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and len(self.mines) < 3:
            self.mines.append(
                Mine(self.model.centerx, self.model.centery))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.model)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate angle between model and mouse
        dx = mouse_x - self.model.centerx
        dy = mouse_y - self.model.centery
        angle = math.degrees(math.atan2(-dy, dx))

        # Draw the model aim
        aim_length = 50
        surf = pygame.Surface(
            (aim_length, self.model_aim.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, (0, 255, 0),
                         (0, 0, aim_length, self.model_aim.height))
        surf = pygame.transform.rotate(surf, angle)

        # Calculate new pivot point
        offset_x = math.cos(math.radians(angle)) * (aim_length // 2)
        offset_y = -math.sin(math.radians(angle)) * (aim_length // 2)

        aim_rect = surf.get_rect(
            center=(self.model.centerx + offset_x, self.model.centery + offset_y))
        screen.blit(surf, aim_rect)

    def update(self, screen, enemies):
        self.update_projectiles(screen)
        self.update_mines(screen, enemies)

    def update_projectiles(self, screen):
        # Update and draw projectiles
        for projectile in self.projectiles[:]:
            projectile.update()
            # Remove projectile if it goes off screen
            if not screen.get_rect().colliderect(projectile.rect):
                self.projectiles.remove(projectile)
            else:
                # Draw the projectile
                projectile.draw(screen)

    def update_mines(self, screen, enemies):
        for mine in self.mines[:]:
            mine.update()
            mine.draw(screen)
            if mine.exploded:
                for enemy in enemies[:]:
                    if math.hypot(enemy.rect.centerx - mine.rect.centerx, enemy.rect.centery - mine.rect.centery) < 50:
                        try:
                            # Remove enemy if it is within the blast radius
                            enemies.remove(enemy)
                        except ValueError:  # If enemy is already removed, ignore
                            pass
                        self.score += 1
                        self.destroys_with_mines += 1
                if math.hypot(self.model.centerx - mine.rect.centerx, self.model.centery - mine.rect.centery) < 50:
                    self.lives -= 1
                try:
                    self.mines.remove(mine)
                except ValueError:
                    pass

    def update_enemies(self, screen, enemies):
        # Update and draw/destroy enemies
        for enemy in enemies[:]:
            enemy.update(self.model)
            enemy.draw(screen, self.model)
            for projectile in enemy.projectiles[:]:
                if self.model.colliderect(projectile.rect):
                    self.lives -= 1
                    enemy.projectiles.remove(projectile)
            for player_projectile in self.projectiles[:]:
                if player_projectile.rect.colliderect(enemy.rect):
                    try:
                        # Remove enemy if it is hit by a player projectile
                        enemies.remove(enemy)
                    except ValueError:  # If enemy is already removed, ignore
                        pass
                    try:
                        # Remove player projectile if it hits an enemy
                        self.projectiles.remove(player_projectile)
                    except ValueError:
                        pass
                    self.score += 1
                    self.destroys_with_projectiles += 1
