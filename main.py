from game.models import Player, Enemy
from game.game import Game
from game.score import SaveRecord

def game() -> None:
    game_start = Game()
    game_start.play()

def show_scores() -> None:
    print()
    show_scores = SaveRecord()
    show_scores.display_records()
    print()
        
def main() -> None:
    while True:
        number = int(input("Play game - 1\nSee points - 2\nQuit game - 3\n").strip())
        if number == 1:
            game()
        elif number == 2:
            show_scores()
        elif number == 3:
            break
        else:
            print("Please try again")

if __name__ == '__main__':
    main() 