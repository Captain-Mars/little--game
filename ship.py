import pygame
from math import sin
from game_stats import GameStats
import numpy as np

class Ship:
    """管理飞船"""
    def __init__(self,sw_game):

        self.screen = sw_game.screen
        self.settings = sw_game.settings
        self.screen_rect = sw_game.screen.get_rect()
        self.moving_right = 0
        self.moving_left = 0
        self.moving_up = 0
        self.moving_down = 0
        self.game = sw_game
        self.center_ship()
        self.font = pygame.font.SysFont('arial',30)
        self.game_time = sw_game.game_time
        self.reset_beast_mode()

    def center_ship(self):
        """load image and center the ship"""
        self.image = pygame.image.load("images/spaceship_images/smallfighter0006.bmp")
        self.new_image_width = self.image.get_width()/2
        self.new_image_height = self.image.get_height()/2
        self._shrink_image()
        self.rect.midbottom = self.screen_rect.midbottom
        self.y = float(self.rect.y - 10)
        self.rect.y = self.y
        self.x = float(self.rect.x)


    def reset_beast_mode(self):
        #beast mode settings
        self.beast_time = self.settings.beast_time
        self.beast_cooling_time = self.settings.beast_cooling_time
        self.beast_left_time = 0
        self.beast_left_cooling_time = self.beast_cooling_time
        self.beast_start_time = -1*self.beast_time
        self.beast_cooling_start_time = 0
        self.beast_cooling_state = True
        self.beast_mode = False


    def update(self,sw_game):
            self.game_time = sw_game.game_time
            if self.moving_right or self.moving_left:
                if self.moving_right and self.rect.right < self.screen_rect.right :
                    self.image = pygame.image.load("images/spaceship_images/smallfighter0011.bmp")
                    self._shrink_image()
                    self.x += self.settings.ship_speed * (self.game.mouse_vector[0]/self.game.mouse_vector_norm)
                    
                if self.moving_left and self.rect.left > self.screen_rect.left :
                    self.image = pygame.image.load("images/spaceship_images/smallfighter0001.bmp")
                    self._shrink_image()
                    self.x += self.settings.ship_speed * (self.game.mouse_vector[0]/self.game.mouse_vector_norm)

            else:
                self.image = pygame.image.load("images/spaceship_images/smallfighter0006.bmp")
                self._shrink_image()

            if self.moving_up or self.moving_down:
                if self.moving_up and self.y > 0 :
                    self.y += self.settings.ship_speed * (self.game.mouse_vector[1]/self.game.mouse_vector_norm)
                    
                if self.moving_down and (self.y + self.new_image_height) < self.settings.screen_height :
                    self.y += self.settings.ship_speed * (self.game.mouse_vector[1]/self.game.mouse_vector_norm)

            self.rect.x = self.x
            self.rect.y = self.y + 5*sin(8*self.game_time)
            #控制beast mode
            self.control_beast_mode(sw_game)

    def control_beast_mode(self,sw_game):
        #控制beast mode
        if self.beast_mode:
            self.beast_left_time = self.beast_time - (self.game_time - self.beast_start_time)
            if self.beast_left_time < 0:
                self.beast_cooling_state = 1
                self.beast_mode = 0
                self.settings.bullet_width = self.settings.bullet_normal_width
                self.settings.bullet_color = self.settings.bullet_normal_color
                self.settings.bullet_speed = self.settings.bullet_normal_speed
                self.beast_cooling_start_time = self.game_time
                sw_game.warning("BEAST MODE OFF")
        elif self.beast_cooling_state:
            self.beast_left_cooling_time = self.beast_cooling_time - (self.game_time - self.beast_cooling_start_time)
            if self.beast_left_cooling_time < 0:
                self.beast_cooling_state = 0

    def _shrink_image(self):
        """修改图片大小并get rect"""
        self.image = pygame.transform.scale(self.image,(self.new_image_width,self.new_image_height))
        self.rect = self.image.get_rect()

    def biltme(self):
        self.screen.blit(self.image,self.rect)