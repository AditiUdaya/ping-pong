import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
    
    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Bounce off top and bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            # Clamp position to prevent getting stuck
            if self.y <= 0:
                self.y = 0
            if self.y + self.height >= self.screen_height:
                self.y = self.screen_height - self.height
    
    def check_collision(self, player, ai):
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()
        
        # Check collision with player (left paddle)
        if ball_rect.colliderect(player_rect):
            if self.velocity_x < 0:  # Only if ball is moving toward this paddle
                # Clamp ball position to prevent tunneling
                self.x = player_rect.right
                # Reverse direction
                self.velocity_x = abs(self.velocity_x)
        
        # Check collision with AI (right paddle)
        elif ball_rect.colliderect(ai_rect):
            if self.velocity_x > 0:  # Only if ball is moving toward this paddle
                # Clamp ball position to prevent tunneling
                self.x = ai_rect.left - self.width
                # Reverse direction
                self.velocity_x = -abs(self.velocity_x)
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
    
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect())
