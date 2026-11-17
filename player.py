
import pygame
from config import *

class Player:
    """The player controlled by the user"""

    def __init__(self, x, y, color=PLAYER_COLOR, speed=PLAYER_SPEED):
        """Initialize the player with a position and size"""
        self.start_x = x  # Reto 5: remember the initial position
        self.start_y = y
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = color
        self.speed = speed
        self.lives = PLAYER_LIVES  # Reto 10
        self.invulnerable_until = 0  # Reto 10: time (ms) when the invulnerability ends

    def reset(self):
        """Reto 5: move the player back to its initial position"""
        self.rect.topleft = (self.start_x, self.start_y)
        self.lives = PLAYER_LIVES  # Reto 10: recover all the lives
        self.invulnerable_until = 0

    def is_alive(self):
        """Reto 10: the player is alive while it has lives left"""
        return self.lives > 0

    def is_invulnerable(self, current_time):
        """Reto 10: True during the seconds after a hit"""
        return current_time < self.invulnerable_until

    def hit(self, current_time):
        """Reto 10: lose a life and become invulnerable for a while"""
        self.lives -= 1
        self.invulnerable_until = current_time + INVULNERABLE_TIME

    def keep_inside_screen(self):
        """Reto 1: prevent the player from leaving the window"""
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def moveArrows(self):
        """Update the player's position based on keyboard input"""
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        self.keep_inside_screen()

    def moveWASD(self):
        """Update the player's position based on WASD keyboard input"""
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        self.keep_inside_screen()

    def change_speed(self, amount):
        """Reto 8: change the speed, keeping it between the min and max"""
        self.speed = max(PLAYER_MIN_SPEED, min(PLAYER_MAX_SPEED, self.speed + amount))

    def draw(self, surface):
        """Draw the player on the given surface"""
        pygame.draw.rect(surface, self.color, self.rect)
