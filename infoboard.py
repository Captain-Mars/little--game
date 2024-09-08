import pygame.font


class Infoboard:
    """显示信息"""
    def __init__(self,sw_game):
        self.screen = sw_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = sw_game.settings
        self.stats = sw_game.stats
        self.ship = sw_game.ship
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont('arial',48)
        self.prep_info()

    def prep_info(self):
        """将信息渲染成图像"""
        #右侧信息
        self.prep_score()
        #左侧信息
        self.font = pygame.font.SysFont('arial',30)

        if self.settings.cheat_mode_active:
            self.cheat_mode_image = self.font.render('cheat_mode_active',True,self.text_color)

        self.ship_left_image = self.font.render(f'ship left: {self.stats.ships_left}',True,self.text_color)
        
        self.round_num_image = self.font.render(f'round {self.stats.fleet_round}',True,self.text_color)

        if self.ship.beast_mode:
            self.beast_mode_image = self.font.render(f'beast mode left time:{round(self.ship.beast_left_time,1)}',True,self.text_color)
            
        elif self.ship.beast_cooling_state:
            self.beast_mode_image = self.font.render(f'beast mode left cooling time:{round(self.ship.beast_left_cooling_time,1)}',True,self.text_color)

        else :
            self.beast_mode_image = self.font.render(f'Beast Mode is ready!',True,self.text_color)
 
    def prep_score(self):
        self.prep_high_score()
        self.font = pygame.font.SysFont('arial',48)
        round_score = round(self.stats.score,-1)
        score_str = f"{round_score:,}"
        self.score_image = self.font.render(score_str,True,self.text_color)
        self.score_rect =self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 50

    def prep_high_score(self):
        self.font = pygame.font.SysFont('arial',30)
        high_score_round = round(self.stats.high_score,-1)
        high_score_str = f"{high_score_round:,}"
        self.high_score_image = self.font.render(f"record:{high_score_str}",True,self.text_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right -20
        self.high_score_rect.top = 20

    def show_info(self):
        """显示信息"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        if self.settings.cheat_mode_active:
            self.screen.blit(self.cheat_mode_image,(30,120))
        self.screen.blit(self.ship_left_image,(30,30))
        self.screen.blit(self.round_num_image,(30,90))
        self.screen.blit(self.beast_mode_image,(30,60))
