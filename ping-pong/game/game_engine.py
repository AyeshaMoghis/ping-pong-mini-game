import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 50)
        self.medium_font = pygame.font.SysFont("Arial", 35)
        
        # Game state
        self.game_over = False
        self.winner = None
        self.winning_score = 5
        self.show_replay_menu = False
        
        # Initialize pygame mixer for sounds
        try:
            pygame.mixer.init()
            self.paddle_sound = pygame.mixer.Sound("sounds/paddle_hit.wav")
            self.score_sound = pygame.mixer.Sound("sounds/score.wav")
            self.game_over_sound = pygame.mixer.Sound("sounds/player_lost.wav")
            print("✅ Sounds loaded successfully!")
        except Exception as e:
            print(f"⚠️ Sound loading failed: {e}")
            self.paddle_sound = None
            self.score_sound = None
            self.game_over_sound = None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-7, self.height)
        if keys[pygame.K_s]:
            self.player.move(7, self.height)

    def update(self):
        if self.game_over:
            return
            
        self.ball.move()
        
        # Store old velocity to detect collision
        old_velocity_x = self.ball.velocity_x
        
        self.ball.check_collision(self.player, self.ai)
        
        # Play paddle sound if ball changed direction (hit paddle)
        if old_velocity_x != self.ball.velocity_x and self.paddle_sound:
            self.paddle_sound.play()

        # Check if ball went off screen (scoring)
        if self.ball.x <= 0:
            self.ai_score += 1
            if self.score_sound:
                self.score_sound.play()
            self.ball.reset()
            self.check_game_over()
        elif self.ball.x >= self.width:
            self.player_score += 1
            if self.score_sound:
                self.score_sound.play()
            self.ball.reset()
            self.check_game_over()

        self.ai.auto_track(self.ball, self.height)

    def check_game_over(self):
        """Check if someone has won the game"""
        if self.player_score >= self.winning_score:
            self.game_over = True
            self.winner = "Player"
        elif self.ai_score >= self.winning_score:
            self.game_over = True
            self.winner = "AI"
            # Play game over sound when PLAYER LOSES
            if self.game_over_sound:
                self.game_over_sound.play()

    def reset_game(self):
        """Reset the game for replay"""
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None
        self.show_replay_menu = False
        self.ball.reset()
        self.player.y = self.height // 2 - 50
        self.ai.y = self.height // 2 - 50

    def handle_replay_input(self, event):
        """Handle keyboard input for replay menu"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                self.winning_score = 2  # Best of 3 = first to 2
                self.reset_game()
                return True
            elif event.key == pygame.K_5:
                self.winning_score = 3  # Best of 5 = first to 3
                self.reset_game()
                return True
            elif event.key == pygame.K_7:
                self.winning_score = 4  # Best of 7 = first to 4
                self.reset_game()
                return True
            elif event.key == pygame.K_ESCAPE:
                return "exit"
        return False

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        
        # Draw center line
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        # Draw game over screen
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # Winner text
            winner_text = self.big_font.render(f"{self.winner} Wins!", True, WHITE)
            winner_rect = winner_text.get_rect(center=(self.width//2, self.height//3))
            screen.blit(winner_text, winner_rect)
            
            # Final score
            score_text = self.medium_font.render(f"Final Score: {self.player_score} - {self.ai_score}", True, WHITE)
            score_rect = score_text.get_rect(center=(self.width//2, self.height//2))
            screen.blit(score_text, score_rect)
            
            # Replay options
            replay_title = self.medium_font.render("Play Again?", True, WHITE)
            replay_rect = replay_title.get_rect(center=(self.width//2, self.height//2 + 60))
            screen.blit(replay_title, replay_rect)
            
            option1 = self.font.render("Press 3 - Best of 3", True, GRAY)
            option2 = self.font.render("Press 5 - Best of 5", True, GRAY)
            option3 = self.font.render("Press 7 - Best of 7", True, GRAY)
            option4 = self.font.render("Press ESC - Exit", True, GRAY)
            
            screen.blit(option1, option1.get_rect(center=(self.width//2, self.height//2 + 110)))
            screen.blit(option2, option2.get_rect(center=(self.width//2, self.height//2 + 150)))
            screen.blit(option3, option3.get_rect(center=(self.width//2, self.height//2 + 190)))
            screen.blit(option4, option4.get_rect(center=(self.width//2, self.height//2 + 230)))
