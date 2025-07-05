import unittest
from game.models import Player, Enemy
import random
from unittest.mock import mock_open, patch, call
from game.settings import ALLOWED_ATTACKS
from game.exceptions import EnemyDown, GameOver
from game.game import Game
from game.score import PlayerRecord, GameSave, ReadScoreFile, SaveRecord
from main import show_scores, main

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
    
#     @patch('random.randint') 
#     @patch('builtins.input', side_effect = ["1", "Name", "2", "2", "2", "2", "3", "3"])
#     def test_game_play_method_10_score(self, mock_input, randint_attack):
#         with patch("builtins.open", open_mock):
#             open_mock = mock_open(read_data="Name|2|10\nBob|2|8\n")
#             with patch("builtins.print") as mock_print:
#                 game = Game()
#                 randint_attack.side_effect = [3, 3, 3, 3, 2, 2]
#                 game.play()
#                 self.assertEqual(game.player.lives, 0)
#                 self.assertEqual(game.player.score, 6)
#                 self.assertEqual(game.enemy.lives, 2)
#                 self.assertEqual(game.enemy.level, 3)
#                 mock_print.assert_has_calls([
#     call('Game, over')

# ])


    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["1", "Name", "2", "3", "3"])
    @patch('builtins.open', new_callable=mock_open)
    def test_game_play_method_contoling_info(self, mock_open, mock_input, mock_randint):
        with patch("builtins.print") as mock_print:
            game = Game()
            mock_randint.side_effect = [3, 2, 2]
            game.play()
            self.assertEqual(game.player.lives, 0)
            self.assertEqual(game.player.score, 5)
            self.assertEqual(game.enemy.lives, 2)
            self.assertEqual(game.enemy.level, 2)
                

    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["1", "Name", "2", "3", "3"])
    @patch('builtins.open', new_callable=mock_open)
    def test_game_play_method_contoling_prints(self, mock_open, mock_input, mock_randint):
        with patch("builtins.print") as mock_print:
            game = Game()
            mock_randint.side_effect = [3, 2, 2]
            game.play()
            mock_print.assert_has_calls([
                                         call('You won enemy, now you have 5 points'),
                                         call('You lost fight, you have 1 hp'),
                                         call('Game Over'),
                                         call('You got 5 points')
                                        ])
    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["1", "Name", "2", "3", "3"])
    @patch('builtins.open', new_callable=mock_open)
    def test_game_play_method_contoling_adding_to_empty_file(self, mock_open, mock_input, mock_randint):
        with patch("builtins.print") as mock_print:
            game = Game()
            mock_randint.side_effect = [3, 2, 2]
            game.play()
            mock_file = mock_open()
            mock_file.write.assert_called_once_with("Name|1|5\n")
    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["2", "Name", "2", "3", "3"])
    @patch('builtins.open', new_callable=mock_open)
    def test_game_play_method_contoling_info_hard_mode(self, mock_open, mock_input, mock_randint):
        with patch("builtins.print") as mock_print:
            game = Game()
            mock_randint.side_effect = [3, 2, 2]
            game.play()
            self.assertEqual(game.player.lives, 0)
            self.assertEqual(game.player.score, 2)
            self.assertEqual(game.enemy.lives, 1)
            self.assertEqual(game.enemy.level, 1)
    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["2", "Name", "2", "3", "3"])
    @patch('builtins.open', new_callable=mock_open, read_data="Alice|2|10\nBob|1|7\n")
    def test_game_play_method_contoling_adding_to__not_empty_file(self, mock_open, mock_input, mock_randint):
        with patch("builtins.print") as mock_print:
            game = Game()
            mock_randint.side_effect = [3, 2, 2]
            game.play()
            mock_file = mock_open()
            mock_file.write.assert_has_calls([
            call("Alice|2|10\n"),
            call("Bob|1|7\n"),
            call("Name|2|2\n")
        ])
    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["2", "Name", "2", "3", "3"])
    @patch('builtins.open', new_callable=mock_open, read_data="Alice|2|10\nBob|1|1\n")
    def test_game_play_method_contoling_adding_to__not_empty_file_sorting(self, mock_open, mock_input, mock_randint):
        with patch("builtins.print") as mock_print:
            game = Game()
            mock_randint.side_effect = [3, 2, 2]
            game.play()
            mock_file = mock_open()
            mock_file.write.assert_has_calls([
            call("Alice|2|10\n"),
            call("Name|2|2\n"),
            call("Bob|1|1\n")
        ])
    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["2", "Name", "2", "3", "3"])
    @patch('builtins.open', new_callable=mock_open, read_data="Name|2|10\nBob|1|7\n")
    def test_game_play_method_contoling_adding_to__not_empty_file_same_name(self, mock_open, mock_input, mock_randint):
        with patch("builtins.print") as mock_print:
            game = Game()
            mock_randint.side_effect = [3, 2, 2]
            game.play()
            mock_file = mock_open()
            mock_file.write.assert_has_calls([
            call("Name|2|10\n"),
            call("Bob|1|7\n"),
        ])

    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["2", "Name", "2", "2", "3", "3"])
    @patch('builtins.open', new_callable=mock_open)
    def test_game_play_method_contoling_info_hard_mode_beating_enemy(self, mock_open, mock_input, mock_randint):
        with patch("builtins.print") as mock_print:
            game = Game()
            mock_randint.side_effect = [3, 3, 2, 2]
            game.play()
            self.assertEqual(game.player.lives, 0)
            self.assertEqual(game.player.score, 12)
            self.assertEqual(game.enemy.lives, 4)
            self.assertEqual(game.enemy.level, 2)
    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["2", "Name", "2", "2", "3", "3"])
    @patch('builtins.open', new_callable=mock_open)
    def test_game_play_method_contoling_prints(self, mock_open, mock_input, mock_randint):
        with patch("builtins.print") as mock_print:
            game = Game()
            mock_randint.side_effect = [3, 3, 2, 2]
            game.play()
            mock_print.assert_has_calls([call('You won fight, you have 2 points'),
 call('You won enemy, now you have 12 points'),
 call('You lost fight, you have 1 hp'),
 call('Game Over'),
 call('You got 12 points')])
    
    @patch('random.randint') 
    @patch('builtins.input', side_effect = ["2", "Name", "2", "2", "3", "3"])
    @patch('builtins.open', new_callable=mock_open)
    def test_game_play_method_contoling_adding_to_empty_file_hard_mode(self, mock_open, mock_input, mock_randint):
        with patch("builtins.print") as mock_print:
            game = Game()
            mock_randint.side_effect = [3, 3, 2, 2]
            game.play()
            mock_file = mock_open()
            mock_file.write.assert_called_once_with("Name|2|12\n")
    
    
            
    


class TestPlayerRecord(unittest.TestCase):

    def test_player_record_init(self):
        player_record = PlayerRecord("Name", "2", "2")
        self.assertEqual(player_record.name, "Name")
        self.assertEqual(player_record.difficulty_mode, "2")
        self.assertEqual(player_record.score, "2")

    def test_player_record_str(self):
        player_record = PlayerRecord("Name", "2", "2")
        self.assertEqual(str(player_record), "Name, Hard mode, 2 score")
    
    def test_player_record_gt_False(self):
        player_record = PlayerRecord("Name", "2", "2")
        player_record_other = PlayerRecord("Name", "2", "4")
        self.assertEqual(player_record > player_record_other, False)
    
    def test_player_record_gt_True(self):
        player_record = PlayerRecord("Name", "2", "4")
        player_record_other = PlayerRecord("Name", "2", "2")
        self.assertEqual(player_record > player_record_other, True)

class TestGameSave(unittest.TestCase):

    def test_game_save_init(self):
        game_save = GameSave()
        self.assertEqual(game_save.records, [])
     
    def test_game_save_file_rewrite_one_player_record(self):
        mock = mock_open()
        with patch("builtins.open", mock):
            player1 = PlayerRecord("Name", "1", "10")
            game_save = GameSave()
            game_save.records.append(player1)
            game_save.file_rewrite()
            mock().write.assert_called_once_with("Name|1|10\n")
    
    def test_game_save_file_rewrite_two_player_record(self):
        mock = mock_open()
        with patch("builtins.open", mock):
            player1 = PlayerRecord("Name", "1", "10")
            player2 = PlayerRecord("Bob", "2", "8")
            game_save = GameSave()
            game_save.records.append(player1)
            game_save.records.append(player2)
            game_save.file_rewrite()
            mock().write.assert_has_calls([
                call("Name|1|10\n"),
                call("Bob|2|8\n")
            ])
            self.assertEqual(mock().write.call_count, 2)
    
    def test_create_player_record(self):
        game_save = GameSave()
        game_save.create_player_record("Name", "2", "0")
        self.assertEqual(game_save.records[0].name, "Name")
        self.assertEqual(game_save.records[0].difficulty_mode, "2")
        self.assertEqual(game_save.records[0].score, "0")
    
    def test_game_save_add_record(self):
        game_save = GameSave()
        game_save.add_record("Name", "2", "0")
        self.assertEqual(game_save.records[0].name, "Name")
        self.assertEqual(game_save.records[0].difficulty_mode, "2")
        self.assertEqual(game_save.records[0].score, "0")
            
    
    def test_game_save_add_record_two_players_different_mode_different_name(self):
        game_save = GameSave()
        game_save.add_record("Name", "2", "0")
        game_save.add_record("Alice", "1", "3")
        self.assertEqual(game_save.records[0].name, "Name")
        self.assertEqual(game_save.records[0].difficulty_mode, "2")
        self.assertEqual(game_save.records[0].score, "0")
        self.assertEqual(game_save.records[1].name, "Alice")
        self.assertEqual(game_save.records[1].difficulty_mode, "1")
        self.assertEqual(game_save.records[1].score, "3")
    
    def test_game_save_add_record_two_players_same_mode_different_name(self):
        game_save = GameSave()
        game_save.add_record("Name", "2", "0")
        game_save.add_record("Alice", "2", "3")
        self.assertEqual(game_save.records[0].name, "Name")
        self.assertEqual(game_save.records[0].difficulty_mode, "2")
        self.assertEqual(game_save.records[0].score, "0")
        self.assertEqual(game_save.records[1].name, "Alice")
        self.assertEqual(game_save.records[1].difficulty_mode, "2")
        self.assertEqual(game_save.records[1].score, "3")
    
    def test_game_save_add_record_two_players_different_mode_same_name(self):
        game_save = GameSave()
        game_save.add_record("Alice", "1", "0")
        game_save.add_record("Alice", "2", "3")
        self.assertEqual(game_save.records[0].name, "Alice")
        self.assertEqual(game_save.records[0].difficulty_mode, "1")
        self.assertEqual(game_save.records[0].score, "0")
        self.assertEqual(game_save.records[1].name, "Alice")
        self.assertEqual(game_save.records[1].difficulty_mode, "2")
        self.assertEqual(game_save.records[1].score, "3")
    
    def test_game_save_add_record_two_players_same_mode_same_name(self):
        game_save = GameSave()
        game_save.add_record("Alice", "1", "0")
        game_save.add_record("Alice", "1", "3")
        self.assertEqual(game_save.records[0].name, "Alice")
        self.assertEqual(game_save.records[0].difficulty_mode, "1")
        self.assertEqual(game_save.records[0].score, "3")

    def test_game_save_prepare_record(self):
        game_save = GameSave()
        game_save.add_record("Name", "2", "0")
        game_save.add_record("Alice", "1", "3") 
        game_save.prepare_record()
        self.assertEqual(game_save.records[0].name, "Alice")
        self.assertEqual(game_save.records[0].difficulty_mode, "1")
        self.assertEqual(game_save.records[0].score, "3")  
        self.assertEqual(game_save.records[1].name, "Name")
        self.assertEqual(game_save.records[1].difficulty_mode, "2")
        self.assertEqual(game_save.records[1].score, "0")  

    def test_game_save_prepare_record_same_names(self):
        game_save = GameSave()
        game_save.add_record("Alice", "2", "0")
        game_save.add_record("Alice", "1", "3") 
        game_save.prepare_record()
        self.assertEqual(game_save.records[0].name, "Alice")
        self.assertEqual(game_save.records[0].difficulty_mode, "1")
        self.assertEqual(game_save.records[0].score, "3")  
        self.assertEqual(game_save.records[1].name, "Alice")
        self.assertEqual(game_save.records[1].difficulty_mode, "2")
        self.assertEqual(game_save.records[1].score, "0") 

    def test_game_save_prepare_record_same_names_same_mode(self):
        game_save = GameSave()
        game_save.add_record("Alice", "2", "0")
        game_save.add_record("Alice", "2", "3") 
        game_save.prepare_record()
        self.assertEqual(game_save.records[0].name, "Alice")
        self.assertEqual(game_save.records[0].difficulty_mode, "2")
        self.assertEqual(game_save.records[0].score, "3")  


class TestReadScoreFile(unittest.TestCase):

    def test_read_score_file_init(self):
        file = ReadScoreFile()
        self.assertEqual(file.file_name, "scores.txt")
    
    def test_read_score_file_read_file_empty(self):
        mock = mock_open()
        with patch("builtins.open", mock):
            file = ReadScoreFile()
            file_text = file.read_file()
            self.assertEqual(file_text, [])

    def test_read_score_file_read_file(self):
        mock = mock_open(read_data="Name|1|10\nBob|2|8\n")
        with patch("builtins.open", mock):
            file = ReadScoreFile()
            file_text = file.read_file()
            self.assertEqual(file_text, ["Name|1|10\n", "Bob|2|8\n"])
    
    def test_read_score_file_read_empty_file(self):
        mock = mock_open()
        with patch("builtins.open", mock):
            game_save = GameSave()
            file = ReadScoreFile()
            file_text = file.read(game_save)
            self.assertEqual(file_text, None)
    
    def test_read_score_file_read_not_empty_file(self):
        mock = mock_open(read_data="Name|1|10\nBob|2|8\n")
        with patch("builtins.open", mock):
            game_save = GameSave()
            file = ReadScoreFile()
            file.read(game_save)
            self.assertEqual(game_save.records[0].name, "Name")
            self.assertEqual(game_save.records[0].difficulty_mode, "1")
            self.assertEqual(game_save.records[0].score, 10)
            self.assertEqual(game_save.records[1].name, "Bob")
            self.assertEqual(game_save.records[1].difficulty_mode, "2")
            self.assertEqual(game_save.records[1].score, 8)
    
    def test_read_score_file_read_not_empty_file_strip_name(self):
        mock = mock_open(read_data="   Name      |1|10\n    Bob    |2|8\n")
        with patch("builtins.open", mock):
            game_save = GameSave()
            file = ReadScoreFile()
            file.read(game_save)
            self.assertEqual(game_save.records[0].name, "Name")
            self.assertEqual(game_save.records[0].difficulty_mode, "1")
            self.assertEqual(game_save.records[0].score, 10)
            self.assertEqual(game_save.records[1].name, "Bob")
            self.assertEqual(game_save.records[1].difficulty_mode, "2")
            self.assertEqual(game_save.records[1].score, 8)
    
    def test_read_score_file_read_not_empty_file_strip_diffiulty_mode(self):
        mock = mock_open(read_data="Name|     1     |10\nBob|     2 |8\n")
        with patch("builtins.open", mock):
            game_save = GameSave()
            file = ReadScoreFile()
            file.read(game_save)
            self.assertEqual(game_save.records[0].name, "Name")
            self.assertEqual(game_save.records[0].difficulty_mode, "1")
            self.assertEqual(game_save.records[0].score, 10)
            self.assertEqual(game_save.records[1].name, "Bob")
            self.assertEqual(game_save.records[1].difficulty_mode, "2")
            self.assertEqual(game_save.records[1].score, 8)
    
    def test_read_score_file_read_not_empty_file_strip_score(self):
        mock = mock_open(read_data="Name|1|        10\nBob|2|8          \n")
        with patch("builtins.open", mock):
            game_save = GameSave()
            file = ReadScoreFile()
            file.read(game_save)
            self.assertEqual(game_save.records[0].name, "Name")
            self.assertEqual(game_save.records[0].difficulty_mode, "1")
            self.assertEqual(game_save.records[0].score, 10)
            self.assertEqual(game_save.records[1].name, "Bob")
            self.assertEqual(game_save.records[1].difficulty_mode, "2")
            self.assertEqual(game_save.records[1].score, 8)
    
class TestSaveRecord(unittest.TestCase):

    def test_save_record_init(self):
        game = SaveRecord()
        self.assertIsInstance(game.game_record, GameSave)
        self.assertIsInstance(game.read_score_file, ReadScoreFile)
    
    def test_save_record_save_one_empty_file(self):
        mock = mock_open()
        with patch("builtins.open", mock):
            game = SaveRecord()
            game.save("Name", "2", 0)
            self.assertEqual(game.game_record.records[0].name, "Name")
            self.assertEqual(game.game_record.records[0].difficulty_mode, "2")
            self.assertEqual(game.game_record.records[0].score, 0)
            mock().write.assert_has_calls([
                call("Name|2|0\n"),
            ])
    
    def test_save_record_save_one_not_empty_file_different_names_different_modes(self):
        mock = mock_open(read_data="Alice|1|10\nBob|2|8\n")
        with patch("builtins.open", mock):
            game = SaveRecord()
            game.save("Name", "2", 0)
            self.assertEqual(game.game_record.records[2].name, "Name")
            self.assertEqual(game.game_record.records[2].difficulty_mode, "2")
            self.assertEqual(game.game_record.records[2].score, 0)
            mock().write.assert_has_calls([
                call("Alice|1|10\n"),
                call("Bob|2|8\n"),
                call("Name|2|0\n")   
            ])
    
    def test_save_record_save_one_not_empty_file_same_names_different_modes(self):
        mock = mock_open(read_data="Name|1|10\nBob|2|8\n")
        with patch("builtins.open", mock):
            game = SaveRecord()
            game.save("Name", "2", 0)
            self.assertEqual(game.game_record.records[2].name, "Name")
            self.assertEqual(game.game_record.records[2].difficulty_mode, "2")
            self.assertEqual(game.game_record.records[2].score, 0)
            mock().write.assert_has_calls([
                call("Name|1|10\n"),
                call("Bob|2|8\n"),
                call("Name|2|0\n")   
            ])
    
    def test_save_record_save_one_not_empty_file_different_names_same_modes(self):
        mock = mock_open(read_data="Alice|2|10\nBob|2|8\n")
        with patch("builtins.open", mock):
            game = SaveRecord()
            game.save("Name", "2", 0)
            self.assertEqual(game.game_record.records[2].name, "Name")
            self.assertEqual(game.game_record.records[2].difficulty_mode, "2")
            self.assertEqual(game.game_record.records[2].score, 0)
            mock().write.assert_has_calls([
                call("Alice|2|10\n"),
                call("Bob|2|8\n"),
                call("Name|2|0\n")   
            ])
    
    def test_save_record_save_one_not_empty_file_same_names_same_modes(self):
        mock = mock_open(read_data="Name|2|10\nBob|2|8\n")
        with patch("builtins.open", mock):
            game = SaveRecord()
            game.save("Name", "2", 17)
            self.assertEqual(game.game_record.records[0].name, "Name")
            self.assertEqual(game.game_record.records[0].difficulty_mode, "2")
            self.assertEqual(game.game_record.records[0].score, 17)
            mock().write.assert_has_calls([
                call("Name|2|17\n"),
                call("Bob|2|8\n"),  
            ])
        
    def test_display_records_empty(self):
        open_mock = mock_open()
        with patch("builtins.open", open_mock):
            with patch("builtins.print") as mock_print:
                game = SaveRecord()
                game.display_records()
                mock_print.assert_has_calls([call("\nThere aren't any written scores in file\n")])
    
    def test_display_records_not_empty(self):
        open_mock = mock_open(read_data="Name|2|10\nBob|2|8\n")
        with patch("builtins.open", open_mock):
            with patch("builtins.print") as mock_print:
                game = SaveRecord()
                game.display_records()
                mock_print.assert_has_calls([
    call('Name, Hard mode, 10 score'),
    call('Bob, Hard mode, 8 score')
])

        
class TestMain(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open) 
    def test_show_scores_empty(self, mock_open):
        with patch("builtins.print") as mock_print:
            show_scores()
            mock_print.assert_has_calls([call("\nThere aren't any written scores in file\n")])

    @patch('builtins.open', new_callable=mock_open, read_data="Alice|2|10\nBob|1|7\n") 
    def test_show_scores_not_empty(self, mock_open_func):
        with patch("builtins.print") as mock_print:
            show_scores()
            mock_print.assert_has_calls([
            call("Alice, Hard mode, 10 score"),
            call("Bob, Normal mode, 7 score")
        ])
    
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["4", "3"])
    def test_main_invalid_input(self, mock_input, mock_print):
        main()
        mock_print.assert_any_call("Please try again")

               

