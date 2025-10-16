import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 10

    def move(self, dy, screen_height):
        self.y += dy
        # Keep paddle within screen bounds
        if self.y < 0:
            self.y = 0
        if self.y + self.height > screen_height:
            self.y = screen_height - self.height

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        # AI follows the ball
        if ball.y < self.y:
            self.move(-self.speed, screen_height)
        elif ball.y > self.y + self.height:
            self.move(self.speed, screen_height)
