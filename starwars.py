#游戏名称：Star Wars
#开发者：Captain Mars（王博轩）
#版本：1.0
#开发环境：python
#行数：1015行
#字数：约37,000字（含空格）
#修改日期：2024/8/24
#游戏玩法：（见文件"instruction.txt")
#Click Esc to escape the game.
#Use the mouse to guide the ship.
#Click the mouse the fire bullets.
#When 'Beast Mode is ready!' appear,
#click the space key to turn on the  beast mode.
#Beast mode can run for 5 seconds,
#and it needs to cool for 60 seconds.
#You have 3 ship
#If you collide with the alien or alien's bullets,
#you will lose one ship.
#If alien reach the bottom of the screen,
#you will also lose one ship.

import sys
import pygame
from settings import Settings
from ship import Ship
from alien import Alien , SuperAlien
from bullet import Bullet , AlienBullet
from game_stats import GameStats
from button import Button
from infoboard import Infoboard
from time import sleep , time
import traceback
import numpy as np
from random import randint

class StarWars:
    """管理游戏"""
    def __init__(self):
        """初始化"""
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.game_time = time()
        #创建音频
        self.normal_gunshot_sound = pygame.mixer.Sound("sound/normal_gunshot.wav")
        self.beast_gunshot_sound = pygame.mixer.Sound("sound/beast_gunshot.mp3")
        self.background_music = pygame.mixer.Sound("sound/background_music.wav")
        self.alien_crash_sound = pygame.mixer.Sound("sound/alien_crash.wav")
        self.tap_sound = pygame.mixer.Sound("sound/tap.wav")
        self.ship_crash_sound = pygame.mixer.Sound("sound/ship_crash.wav")
        self.game_launch_sound = pygame.mixer.Sound("sound/game_launch.wav")
        self._game_over_sound = pygame.mixer.Sound("sound/game_over.wav")
        #
        self.deep_space_image = pygame.image.load("images/background/deep_space.jpg")
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.screen_rect = self.screen.get_rect()
        self.game_name = "StarWars"
        self.publisher = "Captain_Mars"
        pygame.display.set_caption(self.game_name)
        self.deep_space_image = pygame.transform.scale(self.deep_space_image,(self.settings.screen_width,self.settings.screen_height))
        self.mouse_pos_x = 0
        self.mouse_pos_y = 0
        self.mouse_vector = np.array([0,0])
        self.mouse_vector_norm = 0
        #创建ship
        self.ship = Ship(self)
        #统计游戏数据
        self.stats = GameStats(self)
        self.infoboard = Infoboard(self)
        #创建alien编组
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        #创建bullets编组
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        #开火状态
        self.fire_active = False
        self.last_fire_time = 0
        self.game_active = False
        self.font = pygame.font.Font(None,50)
        self.play_button = Button(self,"PLAY",center = True)
        self.instruction_button = Button(self,"Instruction",800,600)
        self.return_page_button = Button(self,"BACK",40,40)
        self.escape_button = Button(self,"Esc",200,600)
        self.warning_time_start = time()
        self.warning_bool = 0
        self.warning_contents = "Press The Button To Start"
        #instruction page
        self.instruction_page = False



    def run_game(self):
        """开始游戏循环"""
        self.game_launch_time = time()
        #开场动画
        self._game_launch()
        self.background_music.play(-1)
        while True:
            self.event_list = pygame.event.get()
            self._check_event()
            self.game_time = time()
            self._mouse_control()
            self.ship.update(self)
            if self.game_active:
                self._update_aliens()
                self._fire()
                self._update_bullet()
                self._update_alien_bullet()  
            else:
                self._mouse_pos()

            self.infoboard.prep_info()
            self._update_screen()
            self.clock.tick(60)

    def _game_launch(self):
        """开场动画"""
        self.game_launch_sound.play()
        current_time = time()
        while current_time < 8 + self.game_launch_time:
            current_time = time()
            brightness = (current_time - self.game_launch_time)*35
            game_name_size = int((current_time - self.game_launch_time)*50)
            publisher_size = int((current_time - self.game_launch_time)*5)
            self.screen.fill(self.settings.background_color)
            if brightness <= 255:
                self.font = pygame.font.SysFont('arial',game_name_size)
                game_name = self.font.render(self.game_name,True,(brightness,brightness,brightness))
                self.font = pygame.font.SysFont('arial',publisher_size)
                publisher = self.font.render(f"publisher: {self.publisher}",True,(brightness,brightness,brightness))
            publisher_rect = publisher.get_rect()
            game_name_rect = game_name.get_rect()
            game_name_rect.midtop = self.screen_rect.midtop
            publisher_rect.midtop = self.screen_rect.midtop
            game_name_rect.y += 200
            publisher_rect.y += 600
            self.screen.blit(game_name,(game_name_rect.x,game_name_rect.y)) 
            self.screen.blit(publisher,(publisher_rect.x,publisher_rect.y)) 
            pygame.display.flip()




    def _check_event(self):
        for event in self.event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_buttondown()
            elif event.type == pygame.MOUSEBUTTONUP:
                self._check_mouse_buttonup()

    def _check_mouse_buttondown(self):
        """鼠键检查"""
        if self.game_active == False:
            pass
        elif self.game_active == True:
            self.fire_active = True

    def _check_mouse_buttonup(self):
        self.fire_active = False


    def _mouse_control(self):
        """用鼠标控制ship"""
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos_x = mouse_pos[0]
        self.mouse_pos_y = mouse_pos[1]
        vector = [self.mouse_pos_x - self.ship.rect.x,self.mouse_pos_y - self.ship.rect.y]
        self.mouse_vector = np.array(vector)
        self.mouse_vector_norm  = np.linalg.norm(self.mouse_vector)
        if  self.ship.rect.collidepoint(mouse_pos):
            self.ship.moving_right = 0
            self.ship.moving_left = 0
            self.ship.moving_down = 0
            self.ship.moving_up = 0
        else:
            if self.ship.rect.x < self.mouse_pos_x - 20 :
                self.ship.moving_left = 0
                self.ship.moving_right = 1
            elif self.ship.rect.x > self.mouse_pos_x + 20 :
                self.ship.moving_right = 0
                self.ship.moving_left = 1
            else:
                self.ship.moving_left = 0
                self.ship.moving_right = 0
            if self.ship.rect.y < self.mouse_pos_y - 20:
                self.ship.moving_up = 0
                self.ship.moving_down = 1
            elif self.ship.rect.y > self.mouse_pos_y + 20:
                self.ship.moving_up = 1
                self.ship.moving_down = 0
            else:
                self.ship.moving_up = 0
                self.ship.moving_down = 0

    def _mouse_pos(self):
        """追踪鼠标位置"""
        mouse_pos = pygame.mouse.get_pos()
        if self.instruction_page:
            if self.return_page_button.rect.collidepoint(mouse_pos):
                self._check_return_page_button()
        else:
            if self.play_button.rect.collidepoint(mouse_pos):
                self._check_play_button()
            elif self.instruction_button.rect.collidepoint(mouse_pos):
                self._check_instruction_button()
            elif self.escape_button.rect.collidepoint(mouse_pos):
                self._check_escape_button()

    def _check_escape_button(self):
        for event in self.event_list:
            button_clicked = (event.type == pygame.MOUSEBUTTONDOWN)
            if button_clicked and not self.game_active:
                self.tap_sound.play()
                sleep(0.5)
                pygame.quit()
                sys.exit()


    def _check_return_page_button(self):
        for event in self.event_list:
            button_clicked = (event.type == pygame.MOUSEBUTTONDOWN)
            if button_clicked and not self.game_active:
                self.tap_sound.play()
                self.instruction_page = False

            

    def _check_play_button(self):
        for event in self.event_list:
            button_clicked = (event.type == pygame.MOUSEBUTTONDOWN)
            if button_clicked and not self.game_active:
                self.tap_sound.play()
                #重置数据
                self.settings.initialize_dynamic_settings()
                self.stats.reset_stats()
                #清空子弹和alien
                self.bullets.empty()
                self.aliens.empty()
                #重建ship，alien
                self._create_fleet()
                #游戏开始
                self.game_active = True
                break

    def _check_instruction_button(self):
       for event in self.event_list:
            button_clicked = (event.type == pygame.MOUSEBUTTONDOWN)
            if button_clicked and not self.game_active:
                self.tap_sound.play()
                self.instruction_page = True
                break
            

    def _check_keydown_events(self,event):
        """响应按下"""
        if event.key == pygame.K_RIGHT:
            #开始右移飞船
            self.ship.moving_right = 1
        elif event.key == pygame.K_LEFT:
            #开始左移飞船
            self.ship.moving_left = 1
        elif event.key == pygame.K_UP:
            #上升
            self.ship.moving_up = 1
        elif event.key == pygame.K_DOWN:
            #下降
            self.ship.moving_down = 1
        elif event.key == pygame.K_SPACE:
            #野兽模式
            self._beast_mode()
        elif event.key == pygame.K_ESCAPE:
            if self.game_active:
                self._game_over()
            else:
                pygame.quit()
                sys.exit()


    def _check_keyup_events(self,event):
        """响应释放"""
        pass

    def _ship_hit(self):
        """响应ship和alien或alien_bullet的碰撞"""
        if self.stats.ships_left > 0:
            self.ship_crash_sound.play()
            self.stats.ships_left -= 1
            self.bullets.empty()
            self.alien_bullets.empty()
            self.aliens.empty()
            #创建新的fleet
            self._create_fleet()
            self.ship.center_ship()
            self.warning("SHIP CRASH!!!")
            sleep(0.2)
        else:
            self._game_over()

    def _game_over(self):
        self.game_active = False
        self._game_over_sound.play()
        self.warning("GAME OVER!!!")
        #重置数据
        self.ship.center_ship()
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        #清空子弹和alien
        self.bullets.empty()
        self.alien_bullets.empty()
        self.aliens.empty()


    def _check_aliens_bottom(self):
        """检查alien是否到达下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #像ship hit 一样处理
                self._ship_hit()
                break

    def _beast_mode(self):
        """野兽模式下子弹口径变大，子弹不会消失"""
        if self.ship.beast_mode == 0 and self.ship.beast_cooling_state == False:
            self.ship.beast_mode = 1
            self.settings.bullet_width = self.settings.bullet_beast_width
            self.settings.bullet_color = self.settings.bullet_beast_color
            self.settings.bullet_speed = self.settings.bullet_beast_speed
            self.ship.beast_start_time = self.game_time
            self.warning('BEAST MODE ON')
        elif self.ship.beast_mode:
            self.warning("beast mode is active")
        elif self.ship.beast_cooling_state:
            self.warning("beast mode is cooling")

    def _create_fleet(self):
        """创建alien fleet"""
        #创建第一个alien
        alien = Alien(self)
        self.aliens.add(alien)
        alien_width , alien_height = alien.rect.size
        current_x , current_y = alien_width + 2 * alien_width , alien_height + self.settings.fleet_initial_position
        while current_y < 0:
            #创建多行alien
            while current_x < (self.settings.screen_width - 2 * alien_width):
                if randint(-2,self.settings.fleet_density) > 0:
                    self._create_alien(current_x,current_y)
                current_x += 2 * alien_width
            #重置current_x&y
            current_x = alien_width
            current_y += 2 * alien_height
            

    def _create_alien(self,x_position,y_position):
        if randint(-5,self.settings.beast_alien_density) > 0:
            new_alien = SuperAlien(self)
        else:
            new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = new_alien.x
        new_alien.y = y_position
        new_alien.rect.y = new_alien.y
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """更新所有alien位置"""
        self._check_fleet_edges()
        self.aliens.update()
        #检测ship与alien的碰撞
        if pygame.sprite.spritecollideany(self.ship , self.aliens):
            self._ship_hit()
        #检查与屏幕下缘碰撞
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                alien.change_direction()


    def _fire(self):
        """控制开火"""
        if self.fire_active and self.last_fire_time < time() - self.settings.fire_frequency:
            self._fire_bullet()
            self.last_fire_time = time()
        

    def _fire_bullet(self):
        """创建一个子弹,并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            if self.ship.beast_mode:
                self.beast_gunshot_sound.play()
            else:
                self.normal_gunshot_sound.play()
            new_bullet= Bullet(self)
            self.bullets.add(new_bullet)
        else:
            self.warning("Your gun needs to cool down!!!")

    def _fire_alien_bullet(self,superalien):
        """创建一个alien子弹,并将其加入编组bullets"""
        new_bullet= AlienBullet(self,superalien)
        self.alien_bullets.add(new_bullet)

    def _update_bullet(self):
        """更新子弹位置并删除飞离屏幕的子弹,检查中弹情况"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _update_alien_bullet(self):
        self.alien_bullets.update()
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.bullets.remove(bullet)
        self._check_bullet_ship_collisions()

    def _check_bullet_ship_collisions(self):
         #检查中弹
        collisions = pygame.sprite.spritecollideany(self.ship , self.alien_bullets)
            
        if collisions:
            self._ship_hit()

    def _check_bullet_alien_collisions(self):
         #检查中弹并删除对应子弹和alien
        if self.ship.beast_mode:
            #collisions是一个字典
            collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,False,True)
        else:
            collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
            
        if collisions:
            for aliens in collisions.values():
                self.alien_crash_sound.play()
                #记分
                self.stats.score += self.settings.alien_points * len(aliens)
            self.stats.check_high_score()
                

        if (self.game_active) and (not self.aliens):
           self._new_round()

    def _new_round(self):
        #删除现有子弹并创建一个新的fleet
        #开启新的一轮
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()
        self.stats.fleet_round += 1
        self.warning(f"fleet round {self.stats.fleet_round}")


    def warning(self,warning:str): 
        """创建warning内容"""
        self.warning_contents  = warning
        self.warning_bool = bool(1)       #判断是否正在打印warning的bool变量
        self.warning_time_start = time()   #记录warning开始的时间

    def _print_warning(self):
        """在游戏界面打印提示"""
        self.font = pygame.font.SysFont('arial',50)
        self.warning_bool = time() < self.warning_time_start + self.settings.warning_time
        if self.warning_bool:
            text = self.font.render(self.warning_contents,True,(255,255,255))
            text_rect = text.get_rect()
            text_rect.midtop = self.screen_rect.midtop
            self.screen.blit(text,(text_rect.x,text_rect.y)) 

    def _print_instruction(self):
        self.font = pygame.font.SysFont('arial',50)
        with open("instruction.txt","r",encoding='utf-8') as file:
            contents = file.read()
        lines = contents.splitlines()
        line_num = 1
        for line in lines:
            text = self.font.render(line,True,(255,255,255))
            text_rect = text.get_rect()
            text_rect.midtop = self.screen_rect.midtop
            text_rect.y += 40 * line_num
            self.screen.blit(text,(text_rect.x,text_rect.y)) 
            line_num += 1

    def _show_record(self):
        self.font = pygame.font.SysFont('arial',50)
        high_score_round = round(self.stats.high_score,-1)
        high_score_str = f"{high_score_round:,}"
        self.high_score_image = self.font.render(f"record:{high_score_str}",True,(255,255,255))
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.center = self.screen_rect.center
        self.high_score_rect.y -= 100
        self.screen.blit(self.high_score_image,self.high_score_rect)

    def _show_name(self):
        self.font = pygame.font.SysFont('arial',80)
        self.game_name_image = self.font.render(f"{self.game_name}",True,(255,255,255))
        self.game_name_rect = self.game_name_image.get_rect()
        self.game_name_rect.center = self.screen_rect.center
        self.game_name_rect.y -= 200
        self.screen.blit(self.game_name_image,self.game_name_rect)



    def _update_screen(self):
        """重绘屏幕"""
        if self.game_active:
            self.screen.blit(self.deep_space_image,(0,0))
            self.ship.biltme()
            self.aliens.draw(self.screen)
            #绘制子弹
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            for bullet in self.alien_bullets.sprites():
                bullet.draw_bullet()
            #打印信息
            self._print_warning()
            self.infoboard.show_info()
        #打印按钮
        else:
            if self.instruction_page:
                self.screen.blit(self.deep_space_image,(0,0))
                self.return_page_button.draw_button()
                self._print_instruction()

            else:
                self.screen.blit(self.deep_space_image,(0,0))
                self._print_warning()
                self._show_name()
                self._show_record()
                self.escape_button.draw_button()
                self.play_button.draw_button()
                self.instruction_button.draw_button()
                self.ship.biltme()
        #刷新屏幕
        pygame.display.flip()




#主程序
if __name__ == "__main__":
    try:
        game = StarWars()
        game.run_game()

    except Exception as e:
        print(f"Error Type:{type(e).__name__}")
        print(f"Error:{str(e)}")
        print(f"Error Postion:")
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()