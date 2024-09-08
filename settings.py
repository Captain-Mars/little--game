class Settings:
    """储存游戏设定"""
    def __init__(self):
        """初始化游戏设定"""
        #管理员作弊模式
        self.cheat_mode_active = 0
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.background_color = (0,0,0)
        #飞船设置
        self.ship_limit = 2
        #子弹设置
        self.fire_frequency = 0.2
        self.alien_fire_frequency = 3
        self.bullet_normal_speed = 3.0
        self.bullet_beast_speed = 6.0
        self.bullet_beast_width = 50
        self.bullet_normal_width = 3
        self.bullet_height = 15
        self.bullet_width = self.bullet_normal_width
        self.bullet_color = (100,100,100)
        self.alien_bullet_height = 15
        self.alien_bullet_width = 3
        self.alien_bullet_color = (100,225,225)
        self.bullet_normal_color = (100,100,100)
        self.bullet_beast_color = (250,100,100)
        self.bullets_allowed = 20
        #beast mode
        self.beast_time = 5
        self.beast_cooling_time = 60
        #warning设置
        self.warning_time = 1
        #alien设置
        self.fleet_drop_speed = 1
        self.fleet_initial_position = -1200     #负数
        #游戏节奏
        self.speedup_scale = 1.1
        #alien分数提高速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.alien_points = 50   #单个alien得分
        self.ship_speed  = 8
        self.bullet_speed = self.bullet_normal_speed
        self.alien_bullet_speed = 2.0
        self.alien_speed = 1.0
        self.fleet_density = 1  #fleet密度
        self.fleet_density_float = float(self.fleet_density)
        self.beast_alien_density = 0    #beastalien 密度
        self.beast_alien_density_float = float(self.beast_alien_density)
        if self.cheat_mode_active:
            self.cheat_mode()
         
    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed *= 1
        if self.fleet_drop_speed < 1.5:
            self.fleet_drop_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points*self.score_scale)
        self.fleet_density_float += 0.5
        self.beast_alien_density_float += 0.5
        self.fleet_density = int(self.fleet_density_float)
        self.beast_alien_density = int(self.beast_alien_density_float)

    def cheat_mode(self):
        """管理员作弊模式"""
        self.beast_time = 100
        self.beast_cooling_time = 0
        self.bullets_allowed = 100
        self.bullet_beast_width = 200
        self.bullet_normal_width = 200
        self.bullet_width = self.bullet_normal_width
        self.ship_limit = 1
