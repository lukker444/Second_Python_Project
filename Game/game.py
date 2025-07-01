from models import Player, Enemy
from settings import ATTACK_PAIRS_OUTCOME


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

        self.mode = input("Choose difficulty mode: ")
        self.player = Player()
        self.enemy = Enemy(self.difficulty_mode)

    def create_enemy(self) -> None: 

        """
        Метод пересоздает врага
        Ничего не возвращает
        """

        self.enemy.recreate_enemy(self.player, self.difficulty_mode)

    def fight(self) -> int:

        """
        Метод создает 2 переменные
        Первое это аттака врага (вернет Камень, Ножници или Бумагу)
        Второе это аттака врага (вернет Камень, Ножници или Бумагу)
        Из переменных делаем кортеж 
        Возвращает число(WIN = 1, LOSE = -1, DRAW = 0) 
        """

        enemy_attack = self.enemy.select_attack()
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
            self.enemy.decrease_lives(self.player, self.difficulty_mode)
        elif result == -1:
            self.player.decrease_lives()
            
    def play(self) -> None:

        """
        Начало игры 
        Проверяет если кол-во хп игрока или врага не меньше нуля
        Если кол-во хп врага меньше нуля то тогда пересоздет врага
        Если кол-во хп игрока меньше нуля то тогда игра окончена
        Ничего не возвращает
        """
        
        while True:

            result = self.fight()
            self.handle_fight_result(result)

            if result == 1:
                print("You won")
                print(f"Enemy has {self.enemy.lives} hp")
                print(f"You have got {self.player.score} point")

            elif result == -1:
                print("You lost")
                print(f"Now you have {self.player.lives} hp")

            elif result == 0:
                print("You got draw")

            if self.enemy.lives == 0:
                self.create_enemy()
                

            elif self.player.lives == 0:
                self.player.game_over()
                



game_start = Game()
game_start.play()