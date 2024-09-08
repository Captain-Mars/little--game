import pygame
from pygame.sprite import Sprite
from random import randint , choice


class Alien(Sprite):
    """表示单个alien"""
    def __init__(self,sw_game):

        super().__init__()
        self.screen = sw_game.screen
        self.settings = sw_game.settings
        self.image = pygame.image.load("images/alien_images/alien.bmp")
        new_image_width = self.image.get_width()/3
        new_image_height = self.image.get_height()/3
        self.image = pygame.transform.scale(self.image,(new_image_width,new_image_height))
        self.image = pygame.transform.rotate(self.image,-90)
        self.rect = self.image.get_rect()
        #设置初始位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height + self.settings.fleet_initial_position
        #储存精确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        direction = [-1,1]
        self.direction = int(choice(direction))     #direction:  1:right ; -1:left
        #速度随机偏值
        self.random_relativedrop_speed = float(randint(-10,10)/20)


    def update(self):
        self.x += self.settings.alien_speed * self.direction
        self.y += (self.settings.fleet_drop_speed + self.random_relativedrop_speed)
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self):
        """如果alien碰到边缘返回Ture"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
    def change_direction(self):
        self.direction *= -1




class SuperAlien(Alien):
    """表示单个alien"""
    def __init__(self,sw_game):

        super().__init__(sw_game)
        self.game = sw_game
        self.game_time = sw_game.game_time
        self.image = pygame.image.load("images/alien_images/beast_alien.bmp")
        new_image_width = self.image.get_width()/3
        new_image_height = self.image.get_height()/3
        self.image = pygame.transform.scale(self.image,(new_image_width,new_image_height))
        self.image = pygame.transform.rotate(self.image,180)
        self.rect = self.image.get_rect() 
        self.fire_active = True
        self.last_fire_time = 0

    def update(self):
        self.game_time = self.game.game_time
        self.x += self.settings.alien_speed * self.direction
        self.y += (self.settings.fleet_drop_speed + self.random_relativedrop_speed)
        self.rect.x = self.x
        self.rect.y = self.y
        if self.y > 0 :
            self.fire()


    def fire(self):
        if self.fire_active and self.last_fire_time < self.game_time - self.settings.alien_fire_frequency:
            self.game._fire_alien_bullet(self)
            self.last_fire_time = self.game_time



