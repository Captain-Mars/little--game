import pygame.font

class Button:
    def __init__(self,sw_game,msg, x = 0 , y = 0,center = False):
        """初始化按钮属性
        (game class self,
        message,
        x,
        y,
        Whether center the button?
        )
        """
        self.screen = sw_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width , self.height = 200 , 80
        self.button_color = (100,100,100)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont('arial',48)
        if center:
            self.rect = pygame.Rect(0,0,self.width,self.height)
            self.rect.center = self.screen_rect.center
        else:
            self.rect = pygame.Rect(int(x),int(y),self.width,self.height)
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        """将msg渲染成图案,显示在按钮上"""        
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制按钮并绘制文本"""
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)