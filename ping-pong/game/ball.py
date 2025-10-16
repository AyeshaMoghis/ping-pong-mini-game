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

        # Wall collision (top and bottom)
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1

    def check_collision(self, player, ai):
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()
        
        # Check collision with player paddle
        if ball_rect.colliderect(player_rect):
            # Make sure ball is moving toward the paddle (going left)
            if self.velocity_x < 0:
                # Position ball at the edge of paddle to prevent overlap
                self.x = player_rect.right
                self.velocity_x *= -1
                # Add some variation based on where ball hits paddle
                hit_pos = (self.y - player.y) / player.height
                self.velocity_y += (hit_pos - 0.5) * 2
        
        # Check collision with AI paddle
        if ball_rect.colliderect(ai_rect):
            # Make sure ball is moving toward the paddle (going right)
            if self.velocity_x > 0:
                # Position ball at the edge of paddle to prevent overlap
                self.x = ai_rect.left - self.width
                self.velocity_x *= -1
                # Add some variation based on where ball hits paddle
                hit_pos = (self.y - ai.y) / ai.height
                self.velocity_y += (hit_pos - 0.5) * 2

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
