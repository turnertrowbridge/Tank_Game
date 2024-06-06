import pygame
import math
import random
from projectile import Projectile


class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.aim = pygame.Rect(0, 0, 50, 10)
        self.projectiles = []
        self.shoot_timer = random.randint(20, 50)
        self.SPEED = 1

    def update(self, player):
        dx = player.centerx - self.rect.centerx
        dy = player.centery - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))

        self.shoot_timer -= 1
        if self.shoot_timer <= 0 and len(self.projectiles) < 3:
            projectile = Projectile(self.rect.centerx + math.cos(math.radians(angle)) * (
                self.aim.width // 2), self.rect.centery - math.sin(math.radians(angle)) * (self.aim.width // 2), angle)
            self.projectiles.append(projectile)
            self.shoot_timer = random.randint(20, 50)

        for projectile in self.projectiles[:]:
            projectile.update()
            if not pygame.display.get_surface().get_rect().colliderect(projectile.rect):
                self.projectiles.remove(projectile)

        # Move towards the player
        angle = math.degrees(math.atan2(dy, dx))
        if dx != 0:
            self.rect.x += dx / abs(dx) * self.SPEED
        if dy != 0:
            self.rect.y += dy / abs(dy) * self.SPEED

    def draw(self, screen, player):
        dx = player.centerx - self.rect.centerx
        dy = player.centery - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))

        pygame.draw.rect(screen, (0, 255, 0), self.rect)

        aim_length = 50
        surf = pygame.Surface((aim_length, self.aim.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0),
                         (0, 0, aim_length, self.aim.height))
        surf = pygame.transform.rotate(surf, angle)

        # Calculate new pivot point
        offset_x = math.cos(math.radians(angle)) * (aim_length // 2)
        offset_y = -math.sin(math.radians(angle)) * (aim_length // 2)

        aim_rect = surf.get_rect(
            center=(self.rect.centerx + offset_x, self.rect.centery + offset_y))
        screen.blit(surf, aim_rect)

        for projectile in self.projectiles:
            projectile.draw(screen)
