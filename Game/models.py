from settings import PLAYER_LIVES, POINTS_FOR_FIGHT, POINTS_FOR_KILLING, ALLOWED_ATTACKS, MODE_MULTIPLIER
import random

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

        self.name = input("What is your name: ")
        self.lives = PLAYER_LIVES
        self.score = 0

    def select_attack(self) -> str:

        """
        Выбираешь атаку (1, 2 или 3)
        Превращается в строку (Камень, Ножницы, Бумага) которое потом используется в методе fight()
        Возвращяет строку
        """

        choosing_attack = input("Choose Paper|Stone|Scissors (1,2,3): ")
        return ALLOWED_ATTACKS[choosing_attack]

    def game_over(self) -> None:

        """
        Метод остонавливает программу
        Ничего не возвращяет
        """

        print("You lost :(")
        print(f"You got {self.score} points")
        raise SystemExit  
    
    def decrease_lives(self) -> None:

        """
        Снижает кол-во жизней
        Ничего не возвращяет
        """

        self.lives -= 1
        
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

    def select_attack(self) -> str:

        """
        Рандомно генерирует число (от 1 до 3)
        Превращается в строку (Камень, Ножницы, Бумага) которое потом используется в методе fight()
        Возвращяет строку
        """

        random_number_attack = random.randint(1, 3)
        enemy_attack = str(random_number_attack)
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

    def recreate_enemy(self, player: object, difficulty_mode: str) -> None:

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
        self.restart_lives()
        player.add_score_for_killing(difficulty_mode) 
        print(f"You defeated enemy, enemy has now level {self.enemy.level} and {self.enemy.lives} hp")

    def decrease_lives(self, player: object, difficulty_mode: str) -> None:

        """
        Метод принимает обьект игрока и уровень сложности
        Снижает кол-во жизней
        Добавляет кол-во очков за победу врага
        Ничего не возвращяет
        """

        self.lives -= 1
        player.add_score_for_fight(difficulty_mode) 