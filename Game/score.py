from .settings import SCORE_FILE, MODES


class PlayerRecord:
    name: str
    difficulty_mode: str
    score: int

    def __init__(self, name, difficulty_mode, score):
        self.name = name
        self.difficulty_mode = difficulty_mode
        self.score = score
    
    def __str__(self):
        return f"{self.name}, {MODES[self.difficulty_mode]} mode, {self.score} score"
    
    def __gt__(self, other):
        return self.score > other.score


class GameSave:
    records: list

    def __init__(self):
        self.records = []
    
    def add_line(self, name, difficulty_mode, score):
        with open(SCORE_FILE, "a") as file:
            file.write(f"{name}|{difficulty_mode}|{score}")
    
    def file_rewrite(self):
        with open(SCORE_FILE, "w") as file:
            for player in self.records:
                file.write(f"{player.name}|{player.difficulty_mode}|{player.score}\n")
    
    def add_record(self, name, difficulty_mode, score):
        for player in self.records:
            if player.name == name and player.difficulty_mode == difficulty_mode:
                if score > player.score: 
                    player.score = score
                return
        new_player = PlayerRecord(name, difficulty_mode, score)
        self.records.append(new_player)
        self.add_line(name, difficulty_mode, score)

    def prepare_record(self):
        self.records.sort(reverse=True, key=lambda x: x.score)


class ReadScoreFile:
    
    file_name: str

    def __init__(self):
        self.file_name = SCORE_FILE         

    def read_file(self):
        with open(self.file_name, "r") as file:
            file_text = file.readlines()
            return file_text

    def read(self, name, difficulty_mode, score, game_save):
        lines = self.read_file()
        if not lines:
            return None
        else:
            for line in lines:
                parts = line.strip().split("|")
                name = parts[0].strip()
                difficulty_mode = parts[1].strip()
                score = int(parts[2].strip())
                player = PlayerRecord(name, difficulty_mode, score)
                game_save.records.append(player)
    

class SaveRecord:
    game_record: object
    read_score_file: object

    def __init__(self):
        self.game_record = GameSave()
        self.read_score_file = ReadScoreFile()
    
    def save(self, name, difficulty_mode, score):
        self.read_score_file.read(name, difficulty_mode, score, self.game_record)
        self.game_record.add_record(name, difficulty_mode, score)
        self.game_record.prepare_record()
        self.game_record.file_rewrite()
    
    







        



