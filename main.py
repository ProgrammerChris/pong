#! /usr/bin/env python

import pygame
import sys
import random
import time

# TODO: MAKE BALL ROUND (DRAW CIRCLE ON TOP OF RECTANGLE AND FOLLOW IT)

class Game:

    def __init__(self):
        pygame.init() #Start Pygame

        # Games speed / CPU Usage
        self.clock = pygame.time.Clock() 
        self.FPS = 60
    
        # Set game duration by points
        self.WINNINGPOINTS = 5

        # Screen info
        TITLEBAR_WIDTH = 25
        SCREEN_WIDTH = 640
        SCREEN_HEIGHT = 480
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption('Pong')

        # Paddle info
        PADDLE_WIDTH = SCREEN_WIDTH/90 # SCALE SIZE OF PADDLES TO THE SCREEN SIZE
        PADDLE_HEIGTH = SCREEN_HEIGHT/6
        self.PADDLE_COLOR = (255, 255, 255)
        self.paddles = []
        self.paddles.append(Paddle( pygame.K_w, # Left paddle
                                    pygame.K_s, 
                                    0, 
                                    (SCREEN_HEIGHT/2)-TITLEBAR_WIDTH,
                                    PADDLE_WIDTH, 
                                    PADDLE_HEIGTH)) 

        self.paddles.append(Paddle( pygame.K_UP,  # Right paddle
                                    pygame.K_DOWN, 
                                    SCREEN_WIDTH-PADDLE_WIDTH, 
                                    (SCREEN_HEIGHT/2)-TITLEBAR_WIDTH,  
                                    PADDLE_WIDTH, 
                                    PADDLE_HEIGTH))

        # Ball info
        BALL_RADIUS = 10
        BALL_VELOCITY = 5
        self.BALL_COLOR = (255, 255, 255)
        self.ball = Ball(BALL_RADIUS, BALL_VELOCITY, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, BALL_RADIUS, BALL_RADIUS)

    def game_loop(self):

        running = True
        self.points = [0, 0]

        while running:

            # STOP LOOP
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False        
            self.screen.fill([0,0,0])

            # Font for displaying result
            font_points = pygame.font.SysFont('Arial', 67)

            pygame.draw.line(self.screen, (255, 255, 255), [pygame.display.get_surface().get_size()[0]/2, 0], [pygame.display.get_surface().get_size()[0]/2, pygame.display.get_surface().get_size()[0]], 1)

            # Draw Ball

            pygame.draw.rect(self.screen, self.BALL_COLOR, self.ball)

            self.ball.move_ball()
                
            # Keep track of points and re-position ball
            if self.goal():
                self.ball.top = pygame.display.get_surface().get_size()[1]/2
                self.ball.left = pygame.display.get_surface().get_size()[0]/2
                self.ball.ball_velocity = -self.ball.ball_velocity
                self.ball.ball_angle = random.randint(-5, 5)

            # Draw paddles
            for paddle in self.paddles:
                paddle.handle_keys(self.screen_rect)
                pygame.draw.rect(self.screen, self.PADDLE_COLOR, paddle)
            
            # Checks
            self.check_ball_hits_wall()
            self.check_ball_hits_paddle()
            
            # Display result
            self.screen.blit(font_points.render('{}   {}'.format(self.points[0], self.points[1]), True, (240,240,240)), ((pygame.display.get_surface().get_size()[0]/2) - (pygame.display.get_surface().get_size()[0]/10), 0)) # If winner, to center text in rectangle
            
            pygame.display.flip()

            if self.check_game_won():
                self.points = [0, 0]
                self.splash_screen()
                running = False
                pygame.quit()
            
            self.clock.tick(self.FPS)


    def check_ball_hits_paddle(self):
        for paddle in self.paddles:
            if self.ball.colliderect(paddle):
                self.ball.ball_velocity = -self.ball.ball_velocity
                self.ball.ball_angle = random.randint(-5, 5)
                break

    def check_ball_hits_wall(self):
        if self.ball.top > pygame.display.get_surface().get_size()[1] or self.ball.top < 0:
            self.ball.ball_angle = -self.ball.ball_angle
    
    def goal(self):
        if self.ball.left > pygame.display.get_surface().get_size()[0]:
            self.points[0] = self.points[0] + 1
            return True
        elif self.ball.left < 0:
            self.points[1] = self.points[1] + 1
            return True
        return False
    
    def check_game_won(self):
        if self.points[0] == self.WINNINGPOINTS or self.points[1] == self.WINNINGPOINTS:
            
            # TODO: Draw WINNER LEFT/RIGHT ON SCREEN AND PROMPT FOR RESTART OR QUIT. STEAL MENU FROM TIC TAC TOE?
            # self.game_loop()
            return True
        return False

    def splash_screen(self):
        running = True
                    
        font_buttons = pygame.font.SysFont('Areal', 22)

        # Restart button
        replay_rect = pygame.Rect(pygame.display.get_surface().get_size()[0]/2 - 100, pygame.display.get_surface().get_size()[1]/2 - 50, 100, 50)
        pygame.draw.rect(self.screen, (125, 255, 125), replay_rect, 0)
        self.screen.blit(font_buttons.render('Replay', True, (0,0,0)), ((pygame.display.get_surface().get_size()[0]/2 - 75), (pygame.display.get_surface().get_size()[1]/2) - 30))
        
        # Quit button
        quit_rect = pygame.Rect(pygame.display.get_surface().get_size()[0]/2, pygame.display.get_surface().get_size()[1]/2 - 50, 100, 50)
        pygame.draw.rect(self.screen, (255, 125, 125), quit_rect, 0)
        self.screen.blit(font_buttons.render('Quit', True, (0,0,0)), ((pygame.display.get_surface().get_size()[0]/2 + 35), (pygame.display.get_surface().get_size()[1]/2) - 30))

        pygame.display.flip()

        while running:
            for event in pygame.event.get():
                if (event.type == pygame.MOUSEBUTTONDOWN):# Button actions
                    mouse_pos = pygame.mouse.get_pos()
                    if replay_rect.collidepoint(mouse_pos):
                        running = False
                        self.game_loop()

                    elif quit_rect.collidepoint(mouse_pos):
                        running = False
                        pygame.quit()
            self.clock.tick(10)
        

class Ball(pygame.Rect):

    def __init__(self, ball_size, ball_velocity, *args, **kwargs):
        self.w, self.h = pygame.display.get_surface().get_size()
        self.ball_size = ball_size
        self.ball_velocity = ball_velocity
        self.ball_angle = 0
        super().__init__(*args, **kwargs)

    def move_ball(self):
        self.move_ip(self.ball_velocity, self.ball_angle)

    

class Paddle(pygame.Rect):

    def __init__(self, up_key, down_key, *args, **kwargs):
        self.up_key = int(up_key)
        self.down_key = int(down_key)
        super().__init__(*args, **kwargs)


    def handle_keys(self, limit):
        key = pygame.key.get_pressed()
        dist = 10
        if key[self.up_key] and not self.clamp_ip(limit):
           self.move_ip(0, -dist)
        if key[self.down_key] and not self.clamp_ip(limit):
           self.move_ip(0, dist)


if __name__ == '__main__':

    game = Game()
    game.game_loop()

    
