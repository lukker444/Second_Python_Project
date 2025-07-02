from game.models import Player, Enemy
from .settings import ATTACK_PAIRS_OUTCOME
from .exceptions import EnemyDown, GameOver

class Game:
    player: object
    enemy: object
    difficulty_mode: str

    def __init__(self) -> None:
        
        """
        Инициалезирует обьект игры
        Принимает уровень сложности
        Создает обьект игрока 
        Создает обьект врага 
        Ничего не возвращяет
        """
        while True:
            self.difficulty_mode = input("Choose difficulty mode (1 or 2): ")
            if self.difficulty_mode == "1" or self.difficulty_mode == "2":
                break
            else:
                print("Try again")
        self.player = Player()
        self.enemy = Enemy(self.difficulty_mode)

    def create_enemy(self) -> None: 

        """
        Метод пересоздает врага
        Ничего не возвращает
        """

        self.enemy.recreate_enemy(self.difficulty_mode)

    def fight(self) -> int:

        """
        Метод создает 2 переменные
        Первое это аттака врага (вернет Камень, Ножници или Бумагу)
        Второе это аттака врага (вернет Камень, Ножници или Бумагу)
        Из переменных делаем кортеж 
        Возвращает число(WIN = 1, LOSE = -1, DRAW = 0) 
        """

        enemy_attack = self.enemy.enemy_attack()
        player_attack = self.player.select_attack()
        return ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)]

    def handle_fight_result(self, result: int) -> None:

        """
        Принимает число из метода fight()
        Если число = 1, враг теряет хп
        Если число = -1, игрок теряет хп
        Ничего не возвращает
        """

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

        """
        Начало игры 
        Проверяет если кол-во хп игрока или врага не меньше нуля
        Если кол-во хп врага меньше нуля то тогда пересоздет врага
        Если кол-во хп игрока меньше нуля то тогда игра окончена
        Ничего не возвращает 
        """
        
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
                break
                



