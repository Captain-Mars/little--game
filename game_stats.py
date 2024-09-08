from pathlib import Path
import json


class GameStats:
    """统计游戏信息"""

    def __init__(self,sw_game):
        self.game = sw_game
        self.settings = sw_game.settings
        self.ship = sw_game.ship
        self.high_score_path = Path('high_score.json')
        if self.high_score_path.exists():
            self.high_score = json.loads(self.high_score_path.read_text())
        else:
            self.high_score = 0
            self.high_score_path.write_text(json.dumps(self.high_score))
        self.reset_stats()

    def reset_stats(self):
        """初始化游戏期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.fleet_round = 1
        #初始化beastmode
        self.ship.reset_beast_mode()

    def check_high_score(self):
        """检查是否诞生最高分"""

        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_path.write_text(json.dumps(self.high_score))
            self.game.warning("New Record!!!")

            
