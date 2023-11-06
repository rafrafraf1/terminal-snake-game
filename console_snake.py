import os, time, keyboard
from random import choice

class Game:
    def __init__(self):
        self.game_width = 30
        self.game_height = 15
        self.refresh_rate = .1 # refresh every x seconds

        self.player_length = 3
        self.direction = "r"

        self.pos = [{
            "x": int(self.game_width/3),
            "y": int(self.game_height/1.5)
        }]
        self.food = {
            "x": int(self.game_width/1.5),
            "y": int(self.game_height/3)
        }

        self.box = []
        self.score = 0
        
        self.createBox()
        self.gameLoop()

    def printGame(self):
        os.system("cls")
        for line in self.box:
            tmp = ""
            for i in line:
                tmp += i*2 if i not in "+|●" else i
                tmp += " " if i == "●" else ""
            print(tmp)
        print(f"score: {self.score}")

    def createBox(self):
        w = self.game_width
        h = self.game_height
        for y in range(h):
            new_line = []
            for x in range(w):
                if (x == 0 or x == w-1) and (y == 0 or y == h-1):
                    new_line.append("+")
                elif x == 0 or x == w-1:
                    new_line.append("|")
                elif y == 0:
                    new_line.append("_")
                elif y == h-1:
                    new_line.append("‾")
                else:
                    new_line.append(" ")
            self.box.append(new_line)

    def placePlayer(self):
        xy = "x" if self.direction in "lr" else "y"
        mp = 1 if self.direction in "dr" else -1

        tmp = self.pos[-1].copy()
        if xy == "x":
            if (tmp[xy] + mp) >= self.game_width-1:
                tmp[xy] = 1
            elif (tmp[xy] + mp) <= 0:
                tmp[xy] = self.game_width - 2
            else:
                tmp[xy] += mp
        else:
            if (tmp[xy] + mp) >= self.game_height-1:
                tmp[xy] = 1
            elif (tmp[xy] + mp) <= 0:
                tmp[xy] = self.game_height - 2
            else:
                tmp[xy] += mp

        self.pos.append(tmp)
        if len(self.pos) > self.player_length:
            self.box[self.pos[0]["y"]][self.pos[0]["x"]] = " "
            self.pos.pop(0)

        if self.box[self.pos[-1]["y"]][self.pos[-1]["x"]] == "█": # ate self
            self.pos = []
            return
        
        for pos in self.pos:
            self.box[pos["y"]][pos["x"]] = "█"

        if self.pos[-1] == self.food: # eat food
            self.food = None
            self.player_length += 3
            self.score += 100

    def placeFood(self):
        if self.food:
            self.box[self.food["y"]][self.food["x"]] = "●"
        else: # food was eaten
            banned = [i for i in self.pos]
            options = []
            for y in range(1, self.game_height-1):
                for x in range(1, self.game_width-1):
                    tmp = {
                        "x": x,
                        "y": y
                    }
                    options.append(tmp) if tmp not in banned else None
            self.food = choice(options)

    def gameLoop(self):
        while True:
            self.printGame()
            time.sleep(self.refresh_rate)
            self.placePlayer()
            self.placeFood()

            if keyboard.is_pressed('enter'):
                break
            elif keyboard.is_pressed('w') and self.direction != "d":
                self.direction = "u"
            elif keyboard.is_pressed('s') and self.direction != "u":
                self.direction = "d"
            elif keyboard.is_pressed('a') and self.direction != "r":
                self.direction = "l"
            elif keyboard.is_pressed('d') and self.direction != "l":
                self.direction = "r"

game = Game()