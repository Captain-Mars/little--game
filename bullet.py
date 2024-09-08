import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """管理子弹"""
    def __init__(self,sw_game):

        super().__init__()
        self.screen = sw_game.screen
        self.settings = sw_game.settings
        self.color = self.settings.bullet_color
        self.width = self.settings.bullet_width
        self.height = self.settings.bullet_height
        self.speed = self.settings.bullet_speed

        #在（0，0）设置一个子弹，再设置正确位置
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.midtop = sw_game.ship.rect.midtop
        #储存用浮点数表示的子弹坐标
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        #刷新子弹位置
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """绘制子弹"""
        pygame.draw.rect(self.screen,self.color,self.rect)



class AlienBullet(Bullet):
    """管理子弹"""
    def __init__(self,sw_game,superalien):

        super().__init__(sw_game)
        self.color = self.settings.alien_bullet_color
        self.width = self.settings.alien_bullet_width
        self.height = self.settings.alien_bullet_height
        self.speed = self.settings.alien_bullet_speed
        #在（0，0）设置一个子弹，再设置正确位置
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.midbottom = superalien.rect.midbottom
        #储存用浮点数表示的子弹坐标
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        #刷新子弹位置
        self.y += self.speed
        self.rect.y = self.y