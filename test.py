import unittest
from game.models import Player, Enemy
import random
from unittest.mock import patch
from game.settings import ALLOWED_ATTACKS
from game.exceptions import EnemyDown, GameOver
from game.game import Game


class TestEnemy(unittest.TestCase): 
    

    def test_enemy_init_normal_difficulty(self):
        
        enemy = Enemy("1")
        self.assertEqual(enemy.lives, 1, "Should be 1")
        self.assertEqual(enemy.lives, 1, "Should be 1")
        
    def test_enemy_init_hard_difficulty(self):

        enemy = Enemy("2")
        self.assertEqual(enemy.level, 1, "Should be 1") 
        self.assertEqual(enemy.lives, 2, "Should be 2")

    def test_enemy_init_wrong_difficulty(self):
        with self.assertRaises(KeyError):
            enemy = Enemy("3")

        with self.assertRaises(KeyError):
            enemy = Enemy("")

        with self.assertRaises(KeyError):
            enemy = Enemy(" ")

    @patch('random.randint')
    def test_select_enemy_attack_paper(self, select_attack):
        select_attack.return_value = 1
        result = random.randint(1, 3)
        self.assertEqual(result, 1)
        enemy_attack = str(result)
        self.assertEqual(ALLOWED_ATTACKS[enemy_attack], "Paper")

    @patch('random.randint')    
    def test_select_enemy_attack_stone(self, select_attack):
        select_attack.return_value = 2
        result = random.randint(1, 3)
        self.assertEqual(result, 2)
        enemy_attack = str(result)
        self.assertEqual(ALLOWED_ATTACKS[enemy_attack], "Stone")

    @patch('random.randint')    
    def test_select_enemy_attack_scissors(self, select_attack):
        select_attack.return_value = 3
        result = random.randint(1, 3)
        self.assertEqual(result, 3)
        enemy_attack = str(result)
        self.assertEqual(ALLOWED_ATTACKS[enemy_attack], "Scissors")

    @patch('random.randint')    
    def test_select_enemy_attack_wrong_number(self, select_attack):
        select_attack.return_value = 4
        result = random.randint(1, 3)
        enemy_attack = str(result)
        with self.assertRaises(KeyError):
            ALLOWED_ATTACKS[enemy_attack]
    
    def test_increase_level_hard_difficulty(self):
        enemy = Enemy("2")
        enemy.increase_level()
        self.assertEqual(enemy.level, 2, "Should be 2")
        
    def test_increase_level_normal_difficulty(self):
        enemy = Enemy("1")
        enemy.increase_level()
        self.assertEqual(enemy.level, 2, "Should be 2")

    def test_restart_lives_normal_difficulty(self):
        enemy_normal = Enemy("1")
        enemy_normal.restart_lives("1")
        self.assertEqual(enemy_normal.lives, 1, "Should be 1")
        
    def test_restart_lives_hard_difficulty(self):
        enemy = Enemy("2")
        enemy.restart_lives("2")
        self.assertEqual(enemy.lives, 2, "Should be 2")

    def test_recreate_enemy_normal_difficulty(self):
        enemy = Enemy("1")
        enemy.recreate_enemy("1")
        self.assertEqual(enemy.lives, 2, "Should be 1")
        self.assertEqual(enemy.level, 2, "Should be 2")
        
    
    def test_recreate_enemy_hard_difficulty(self):
        enemy = Enemy("2")
        enemy.recreate_enemy("2")
        self.assertEqual(enemy.lives, 4, "Should be 2")
        self.assertEqual(enemy.level, 2, "Should be 2")

    def test_decrease_lives_normal_difficulty(self):
        enemy = Enemy("1")    
        with self.assertRaises(EnemyDown):
            enemy.decrease_lives()

    def test_decrease_lives_hard_difficulty(self):
        enemy = Enemy("2")    
        enemy.decrease_lives()
        self.assertEqual(enemy.lives, 1, "Should be 1")
        with self.assertRaises(EnemyDown):
            enemy.decrease_lives()

class TestPlayer(unittest.TestCase):

    @patch('builtins.input', return_value='Alice')
    def test_init_player(self, mock_name):
        player = Player()
        self.assertEqual(player.lives, 2, "Should be 1")
        self.assertEqual(player.score, 0, "Should be 1")
        self.assertEqual(player.name, "Alice")
    
    @patch('builtins.input', side_effect=['', "Alice"])
    def test_init_player_wrong_name(self, mock_input):
        player = Player()
        self.assertEqual(player.lives, 2, "Should be 1")
        self.assertEqual(player.score, 0, "Should be 1")
        self.assertEqual(player.name, 'Alice')
        self.assertEqual(mock_input.call_count, 2)

    @patch('builtins.input', side_effect=['              ', "Alice"])
    def test_init_player_wrong_name(self, mock_input):
        player = Player()
        self.assertEqual(player.lives, 2, "Should be 1")
        self.assertEqual(player.score, 0, "Should be 1")
        self.assertEqual(player.name, 'Alice')
        self.assertEqual(mock_input.call_count, 2)

    @patch('builtins.input', return_value='        b      ')
    def test_init_player_wrong_name(self, mock_input):
        player = Player()
        self.assertEqual(player.lives, 2, "Should be 1")
        self.assertEqual(player.score, 0, "Should be 1")
        self.assertEqual(player.name, 'b')

    @patch('builtins.input', side_effect=['Name', "1"])
    def test_select_attack_paper(self, mock_input):
        player = Player()
        self.assertEqual(player.select_attack(), "Paper")

    @patch('builtins.input', side_effect=['Name', "2"])
    def test_select_attack_stone(self, mock_input):
        player = Player()
        self.assertEqual(player.select_attack(), "Stone")
    
    @patch('builtins.input', side_effect=['Name', "3"])
    def test_select_attack_scissors(self, mock_input):
        player = Player()
        self.assertEqual(player.select_attack(), "Scissors")

    @patch('builtins.input', side_effect=['Name', "4", "3"])
    def test_select_attack_wrong_number(self, mock_input):
        player = Player()
        self.assertEqual(player.select_attack(), "Scissors")
        self.assertEqual(mock_input.call_count, 3)

    @patch('builtins.input', side_effect=['Name', "    ", "3"])
    def test_select_attack_empty_spaces(self, mock_input):
        player = Player()
        self.assertEqual(player.select_attack(), "Scissors")
        self.assertEqual(mock_input.call_count, 3)
    
    @patch('builtins.input', side_effect=['Name', "", "3"])
    def test_select_attack_empty(self, mock_input):
        player = Player()
        self.assertEqual(player.select_attack(), "Scissors")
        self.assertEqual(mock_input.call_count, 3)

    @patch('builtins.input', side_effect=['Name', "       3      "])
    def test_select_attack_with_spaces(self, mock_input):
        player = Player()
        self.assertEqual(player.select_attack(), "Scissors")

    @patch('builtins.input', return_value='Name')
    def test_decrease_lives_player(self, mock_input):
        player = Player()
        player.decrease_lives()
        self.assertEqual(player.lives, 1)

    @patch('builtins.input', return_value='Name')
    def test_raise_GameOver(self, mock_input):
        player = Player()
        player.decrease_lives()
        with self.assertRaises(GameOver):
            player.decrease_lives()
    
    @patch('builtins.input', return_value='Name')
    def test_add_score_for_fight_normal_difficulty(self, mock_input):
        player = Player()
        player.add_score_for_fight("1")
        self.assertEqual(player.score, 1)
    
    @patch('builtins.input', return_value='Name')
    def test_add_score_for_fight_hard_difficulty(self, mock_input):
        player = Player()
        player.add_score_for_fight("2")
        self.assertEqual(player.score, 2)
    
    @patch('builtins.input', return_value='Name')
    def test_add_score_for_killing_hard_difficulty(self, mock_input):
        player = Player()
        player.add_score_for_killing("1")
        self.assertEqual(player.score, 5)
    
    @patch('builtins.input', return_value='Name')
    def test_add_score_for_killing_hard_difficulty(self, mock_input):
        player = Player()
        player.add_score_for_killing("2")
        self.assertEqual(player.score, 10)

class TestGame(unittest.TestCase):

    @patch('builtins.input', side_effect = ["1", "Name"])
    def test_game_init_normal_difficulty(self, mock_input):
        game = Game()
        self.assertEqual(game.difficulty_mode, "1")
        self.assertEqual(game.player.name, "Name")
        self.assertEqual(game.player.lives, 2)
        self.assertEqual(game.player.score, 0)
        self.assertEqual(game.enemy.lives, 1)
        self.assertEqual(game.enemy.level, 1)

    @patch('builtins.input', side_effect = ["2", "Name"])
    def test_game_init_hard_difficulty(self, mock_input):
        game = Game()
        self.assertEqual(game.difficulty_mode, "2")
        self.assertEqual(game.player.name, "Name")
        self.assertEqual(game.player.lives, 2)
        self.assertEqual(game.player.score, 0)
        self.assertEqual(game.enemy.lives, 2)
        self.assertEqual(game.enemy.level, 1)

    @patch('builtins.input', side_effect = ["", "3", "2", "   " , "Name"])
    def test_game_init_wrong_inputs(self, mock_input):
        game = Game()
        self.assertEqual(game.difficulty_mode, "2")
        self.assertEqual(game.player.name, "Name")
        self.assertEqual(game.player.lives, 2)
        self.assertEqual(game.player.score, 0)
        self.assertEqual(game.enemy.lives, 2)
        self.assertEqual(game.enemy.level, 1)
        self.assertEqual(mock_input.call_count, 5)
    
    @patch('builtins.input', side_effect = ["1", "Name"])
    def test_game_create_enemy_normal_difficulty(self, mock_input):
        game = Game()
        game.create_enemy()
        self.assertEqual(game.enemy.level, 2)
        self.assertEqual(game.enemy.lives, 2)
    
    @patch('builtins.input', side_effect = ["2", "Name"])
    def test_game_create_enemy_hard_difficulty(self, mock_input):
        game = Game()
        game.create_enemy()
        self.assertEqual(game.enemy.level, 2)
        self.assertEqual(game.enemy.lives, 4)
    
    @patch('builtins.input', side_effect = ["1", "Name"])
    def test_game_create_enemy_normal_difficulty_twice_times(self, mock_input):
        game = Game()
        game.create_enemy()
        game.create_enemy()
        self.assertEqual(game.enemy.level, 3)
        self.assertEqual(game.enemy.lives, 3)
    
    @patch('builtins.input', side_effect = ["2", "Name"])
    def test_game_create_enemy_hard_difficulty(self, mock_input):
        game = Game()
        game.create_enemy()
        game.create_enemy()
        self.assertEqual(game.enemy.level, 3)
        self.assertEqual(game.enemy.lives, 6)
    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["1", "Name", "1"])
    def test_game_fight_draw_papers(self, mock_input, randint_attack):
        game = Game()
        randint_attack.return_value = 1
        self.assertEqual(game.fight(), 0)

    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["1", "Name", "2"])
    def test_game_fight_draw_stones(self, mock_input, randint_attack):
        game = Game()
        randint_attack.return_value = 2
        self.assertEqual(game.fight(), 0)
    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["1", "Name", "3"])
    def test_game_fight_draw_scissors(self, mock_input, randint_attack):
        game = Game()
        randint_attack.return_value = 3
        self.assertEqual(game.fight(), 0)
    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["1", "Name", "1"])
    def test_game_fight_win_papers(self, mock_input, randint_attack):
        game = Game()
        randint_attack.return_value = 2
        self.assertEqual(game.fight(), 1)

    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["1", "Name", "2"])
    def test_game_fight_win_stones(self, mock_input, randint_attack):
        game = Game()
        randint_attack.return_value = 3
        self.assertEqual(game.fight(), 1)
    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["1", "Name", "3"])
    def test_game_fight_win_scissors(self, mock_input, randint_attack):
        game = Game()
        randint_attack.return_value = 1
        self.assertEqual(game.fight(), 1)
    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["1", "Name", "1"])
    def test_game_fight_lose_papers(self, mock_input, randint_attack):
        game = Game()
        randint_attack.return_value = 3
        self.assertEqual(game.fight(), -1)

    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["1", "Name", "2"])
    def test_game_fight_lose_stones(self, mock_input, randint_attack):
        game = Game()
        randint_attack.return_value = 1
        self.assertEqual(game.fight(), -1)
    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["1", "Name", "3"])
    def test_game_fight_lose_scissors(self, mock_input, randint_attack):
        game = Game()
        randint_attack.return_value = 2
        self.assertEqual(game.fight(), -1)
    
    @patch('builtins.input', side_effect = ["1", "Name"])
    def test_game_handle_fight_result_win_normal_diffiulty(self, mock_input):
        game = Game()
        with self.assertRaises(EnemyDown):
            game.handle_fight_result(1)
     
    @patch('builtins.input', side_effect = ["2", "Name"])
    def test_game_handle_fight_result_win_hard_diffiulty(self, mock_input):
        game = Game()
        game.handle_fight_result(1)
        self.assertEqual(game.enemy.lives, 1)  
        with self.assertRaises(EnemyDown):
            game.handle_fight_result(1)
 
    @patch('builtins.input', side_effect = ["1", "Name"])
    def test_game_handle_fight_result_lose_normal_diffiulty(self, mock_input):
        game = Game()
        game.handle_fight_result(-1)
        self.assertEqual(game.player.lives, 1)
        with self.assertRaises(GameOver):
            game.handle_fight_result(-1)
    
    @patch('builtins.input', side_effect = ["2", "Name"])
    def test_game_handle_fight_result_lose_hard_diffiulty(self, mock_input):
        game = Game()
        game.handle_fight_result(-1)
        self.assertEqual(game.player.lives, 1)
        with self.assertRaises(GameOver):
            game.handle_fight_result(-1)
    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["1", "Name", "3", "3"])
    def test_game_play_method_normal_mode_lose(self, mock_input, randint_attack):
        game = Game()
        randint_attack.side_effect = [2, 2]
        game.play()
        self.assertEqual(game.player.lives, 0)
        self.assertEqual(game.player.score, 0)
        self.assertEqual(game.enemy.lives, 1)
        self.assertEqual(game.enemy.level, 1)

    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["1", "Name", "2", "2", "3", "3"])
    def test_game_play_method_normal_mode_win(self, mock_input, randint_attack):
        game = Game()
        randint_attack.side_effect = [3, 3, 2, 2]
        game.play()
        self.assertEqual(game.player.lives, 0)
        self.assertEqual(game.player.score, 6)
        self.assertEqual(game.enemy.lives, 1)
        self.assertEqual(game.enemy.level, 2)
        
        
        




    

    

        


        


    


        
        
        
    
    



    






        

        
         






