from .settings import PLAYER_LIVES, POINTS_FOR_FIGHT, POINTS_FOR_KILLING, ALLOWED_ATTACKS, MODE_MULTIPLIER
import random
from .exceptions import EnemyDown, GameOver



class Player:

    name: str
    lives: int 
    score: int 

    def __init__(self) -> None:

        """
        Инициалезирует обьект игрока
        Принимает имя
        Задает кол-во жизней (изначательно 2)
        Задает кол-во поинтов (изначательно 0)
        Ничего не возвращяет
        """
        while True:
            self.name = input("What is your name: ").strip()
            if self.name.strip():
                break
            else:
                print("Try again")
        self.lives = PLAYER_LIVES
        self.score = 0

    def select_attack(self) -> str:

        """
        Выбираешь атаку (1, 2 или 3)
        Превращается в строку (Камень, Ножницы, Бумага) которое потом используется в методе fight()
        Возвращяет строку
        """
        while True:
            choosing_attack = input("Choose Paper|Stone|Scissors (1,2,3): ").strip()
            if choosing_attack == "1" or choosing_attack == "2" or choosing_attack == "3":
                break
            else:
                print("Try again")

        return ALLOWED_ATTACKS[choosing_attack]


    def decrease_lives(self) -> None:

        """
        Снижает кол-во жизней
        Ничего не возвращяет
        """

        self.lives -= 1
        if self.lives == 0:
            raise GameOver
        
    def add_score_for_fight(self, difficulty_mode: str) -> None:

        """
        Метод принимает уровень сложности (1 или 2)
        Добавляет кол-во очков за отнимание хп у врага
        Ничего не возвращяет
        """

        self.score += POINTS_FOR_FIGHT * MODE_MULTIPLIER[difficulty_mode]

    def add_score_for_killing(self, difficulty_mode: str) -> None:

         """
        Метод принимает уровень сложности (1 или 2)
        Добавляет кол-во очков за убийство врага
        Ничего не возвращяет
        """

         self.score += POINTS_FOR_KILLING * MODE_MULTIPLIER[difficulty_mode]

    def restart_lives(self):
        self.lives = PLAYER_LIVES

class Enemy:

    lives: int
    level: int

    def __init__(self, difficulty_mode: str) -> None:

        """
        Инициалезирует обьект врага
        Принимает имя
        Задает кол-во жизней (уровень * сложность)
        Задает уровень (изначательно 1)
        Ничего не возвращяет
        """

        self.level = 1
        self.lives = self.level * MODE_MULTIPLIER[difficulty_mode]

    def enemy_attack(self) -> str:

        """
        Рандомно генерирует число (от 1 до 3)
        Превращается в строку (Камень, Ножницы, Бумага) которое потом используется в методе fight()
        Возвращяет строку
        """

        enemy_attack = str(random.randint(1, 3))
        return ALLOWED_ATTACKS[enemy_attack]

    def increase_level(self) -> None:

        """
        Метод добавляет уровень врагу
        Ничего не возвращяет
        """

        self.level += 1
    
    def restart_lives(self, difficulty_mode: str) -> None:

        """
        Метод принимает уровень сложности и задает кол-во хп (уровень * сложность)
        Ничего не возвращяет
        """

        self.lives = self.level * MODE_MULTIPLIER[difficulty_mode]

    def recreate_enemy(self, difficulty_mode: str) -> None:

        """
        Метод принимает обьект игрока
        Метод принимает уровень сложности
        Метод пересоздает врага
        Увеличевает уровень
        Задает кол-во жизней
        Добавляет кол-во очков за победу врага
        Ничего не возвращяет
        """

        self.increase_level()
        self.restart_lives(difficulty_mode)
         
        

    def decrease_lives(self) -> None:

        """
        Снижает кол-во жизней
        Добавляет кол-во очков за победу врага
        Ничего не возвращяет
        """

        self.lives -= 1
        if self.lives == 0:
            raise EnemyDown
            