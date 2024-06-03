import pygame
import math
from projectile import Projectile


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.SPEED = 3
        self.player = pygame.Rect(100, 100, 50, 50)
        self.player_aim = pygame.Rect(0, 0, 50, 10)
        self.projectiles = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - self.player.centerx
                dy = mouse_y - self.player.centery
                angle = math.degrees(math.atan2(-dy, dx))
                projectile = Projectile(self.player.centerx + math.cos(math.radians(angle)) * (self.player_aim.width // 2),
                                        self.player.centery - math.sin(math.radians(angle)) * (self.player_aim.width // 2), angle)
                self.projectiles.append(projectile)

        return True

    def draw(self):
        # Make screen white
        self.screen.fill((255, 255, 255))

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

        for projectile in self.projectiles:
            projectile.update()
            projectile.draw(self.screen)

        pygame.display.flip()

        # Cap the frame rate
        pygame.time.delay(1000 // 60)
