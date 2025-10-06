import pygame
from .paddle import Paddle
from .ball import Ball
import time
import os

# Initialize pygame mixer for sound
pygame.mixer.init()

# Game Engine
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

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
        self.winning_score = 5  # Default winning score
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 60)
        self.menu_font = pygame.font.SysFont("Arial", 35)
        self.game_over = False
        self.winner = None
        self.show_replay_menu = False
        
        # Initialize sound attributes to None
        self.paddle_hit_sound = None
        self.wall_bounce_sound = None
        self.score_sound = None
        self.sounds_loaded = False
        
        # Load sound effects
        self.load_sounds()
    
    def load_sounds(self):
        """Load sound effects with error handling"""
        try:
            self.paddle_hit_sound = pygame.mixer.Sound("assets/sounds/paddle_hit.wav")
            self.wall_bounce_sound = pygame.mixer.Sound("assets/sounds/wall_bounce.wav")
            self.score_sound = pygame.mixer.Sound("assets/sounds/score.wav")
            
            # Set volumes (0.0 to 1.0)
            self.paddle_hit_sound.set_volume(0.5)
            self.wall_bounce_sound.set_volume(0.4)
            self.score_sound.set_volume(0.6)
            
            self.sounds_loaded = True
            print("Sound effects loaded successfully!")
        except (pygame.error, FileNotFoundError) as e:
            print(f"Warning: Could not load sound files: {e}")
            print("Game will continue without sound effects.")
            self.sounds_loaded = False
    
    def play_sound(self, sound):
        """Play sound if sounds are loaded and sound is not None"""
        if self.sounds_loaded and sound is not None:
            sound.play()
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)
    
    def check_game_over(self):
        if self.player_score >= self.winning_score:
            self.game_over = True
            self.winner = "Player"
            self.show_replay_menu = True
            return True
        elif self.ai_score >= self.winning_score:
            self.game_over = True
            self.winner = "AI"
            self.show_replay_menu = True
            return True
        return False
    
    def handle_replay_input(self):
        """Handle keyboard input for replay menu"""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_3]:
            self.reset_game(3)
            return "continue"
        elif keys[pygame.K_5]:
            self.reset_game(5)
            return "continue"
        elif keys[pygame.K_7]:
            self.reset_game(7)
            return "continue"
        elif keys[pygame.K_ESCAPE]:
            return "exit"
        
        return None
    
    def reset_game(self, best_of):
        """Reset the game with new winning score"""
        self.winning_score = (best_of + 1) // 2  # Best of 3 = 2 points, Best of 5 = 3 points, etc.
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None
        self.show_replay_menu = False
        
        # Reset ball position
        self.ball.x = self.ball.original_x
        self.ball.y = self.ball.original_y
        self.ball.velocity_x = 5 if self.ball.velocity_x > 0 else -5
        self.ball.velocity_y = 3 if self.ball.velocity_y > 0 else -3
        
        # Reset paddle positions
        self.player.y = self.height // 2 - 50
        self.ai.y = self.height // 2 - 50
    
    def update(self):
        if self.game_over:
            return  # Stop updating if game is over
        
        # Store old velocities to detect changes
        old_velocity_x = self.ball.velocity_x
        old_velocity_y = self.ball.velocity_y
        
        # Move ball
        self.ball.move()
        
        # Check if ball bounced off wall (velocity_y changed)
        if self.ball.velocity_y != old_velocity_y:
            self.play_sound(self.wall_bounce_sound)
        
        # Check paddle collision
        self.ball.check_collision(self.player, self.ai)
        
        # Check if ball hit paddle (velocity_x changed)
        if self.ball.velocity_x != old_velocity_x:
            self.play_sound(self.paddle_hit_sound)
        
        # Check for scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.play_sound(self.score_sound)
            self.ball.reset()
            self.check_game_over()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.play_sound(self.score_sound)
            self.ball.reset()
            self.check_game_over()
        
        self.ai.auto_track(self.ball, self.height)
    
    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))
        
        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
        
        # Draw game over screen with replay menu
        if self.game_over and self.show_replay_menu:
            self.draw_replay_menu(screen)
    
    def draw_replay_menu(self, screen):
        """Draw the replay menu with options"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Draw winner text
        winner_text = self.game_over_font.render(f"{self.winner} Wins!", True, GREEN)
        text_rect = winner_text.get_rect(center=(self.width // 2, self.height // 2 - 120))
        screen.blit(winner_text, text_rect)
        
        # Draw "Play Again?" text
        play_again_text = self.menu_font.render("Play Again?", True, WHITE)
        play_again_rect = play_again_text.get_rect(center=(self.width // 2, self.height // 2 - 40))
        screen.blit(play_again_text, play_again_rect)
        
        # Draw options
        option_y = self.height // 2 + 20
        spacing = 50
        
        best_of_3 = self.font.render("Press 3 - Best of 3", True, YELLOW)
        best_of_3_rect = best_of_3.get_rect(center=(self.width // 2, option_y))
        screen.blit(best_of_3, best_of_3_rect)
        
        best_of_5 = self.font.render("Press 5 - Best of 5", True, YELLOW)
        best_of_5_rect = best_of_5.get_rect(center=(self.width // 2, option_y + spacing))
        screen.blit(best_of_5, best_of_5_rect)
        
        best_of_7 = self.font.render("Press 7 - Best of 7", True, YELLOW)
        best_of_7_rect = best_of_7.get_rect(center=(self.width // 2, option_y + spacing * 2))
        screen.blit(best_of_7, best_of_7_rect)
        
        exit_text = self.font.render("Press ESC - Exit", True, WHITE)
        exit_rect = exit_text.get_rect(center=(self.width // 2, option_y + spacing * 3 + 20))
        screen.blit(exit_text, exit_rect)
    
    def handle_game_over(self):
        """No longer automatically closes - waits for user input"""
        return False  # Never auto-close
