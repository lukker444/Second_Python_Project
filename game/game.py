from game.models import Player, Enemy
from .settings import ATTACK_PAIRS_OUTCOME
from .exceptions import EnemyDown, GameOver
from game.score import SaveRecord


class Game:
    player: object
    enemy: object
    difficulty_mode: str

    def __init__(self) -> None:
        while True:
            self.difficulty_mode = input("Choose difficulty mode (1 or 2): ")
            if self.difficulty_mode == "1" or self.difficulty_mode == "2":
                break
            else:
                print("Try again")
        self.player = Player()
        self.enemy = Enemy(self.difficulty_mode)

    def create_enemy(self) -> None: 
        self.enemy.recreate_enemy(self.difficulty_mode)

    def fight(self) -> int:
        enemy_attack = self.enemy.enemy_attack()
        player_attack = self.player.select_attack()
        return ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)]

    def handle_fight_result(self, result: int) -> None:
        if result == 1:
            self.enemy.decrease_lives()
            self.player.add_score_for_fight(self.difficulty_mode)
            print(f"You won fight, you have {self.player.score} points")

        elif result == -1:
            self.player.decrease_lives()
            print(f"You lost fight, you have {self.player.lives} hp")

        elif result == 0:
            print("You have draw")
            
    def play(self) -> None:
        
        while True:
            try:
                result = self.fight()
                self.handle_fight_result(result)

            except(EnemyDown):
                self.player.restart_lives()
                self.player.add_score_for_killing(self.difficulty_mode)
                self.enemy.recreate_enemy(self.difficulty_mode)
                print(f"You won enemy, now you have {self.player.score} points")

            except(GameOver):
                print("Game Over")
                print(f"You got {self.player.score} points")
                save_record = SaveRecord()
                save_record.save(self.player.name, self.difficulty_mode, self.player.score)
                break
                



