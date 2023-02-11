import copy
import random


class Puzzle:
    def __init__(self, size: int, state: list, space_coordinates: list):
        self.size = size
        self.state = state
        self.space_coordinates = space_coordinates
        self.end = ""

    def up(self):
        if self.space_coordinates[0] > 0:
            self.state[self.space_coordinates[0]][self.space_coordinates[1]], \
                self.state[self.space_coordinates[0] - 1][self.space_coordinates[1]] = \
                self.state[self.space_coordinates[0] - 1][self.space_coordinates[1]], \
                self.state[self.space_coordinates[0]][self.space_coordinates[1]]
            self.space_coordinates[0] -= 1

    def down(self):
        if self.space_coordinates[0] < self.size - 1:
            self.state[self.space_coordinates[0]][self.space_coordinates[1]], \
                self.state[self.space_coordinates[0] + 1][self.space_coordinates[1]] = \
                self.state[self.space_coordinates[0] + 1][self.space_coordinates[1]], \
                self.state[self.space_coordinates[0]][self.space_coordinates[1]]
            self.space_coordinates[0] += 1

    def right(self):
        if self.space_coordinates[1] < self.size - 1:
            self.state[self.space_coordinates[0]][self.space_coordinates[1]], \
                self.state[self.space_coordinates[0]][self.space_coordinates[1] + 1] = \
                self.state[self.space_coordinates[0]][self.space_coordinates[1] + 1], \
                self.state[self.space_coordinates[0]][self.space_coordinates[1]]
            self.space_coordinates[1] += 1

    def left(self):
        if self.space_coordinates[1] > 0:
            self.state[self.space_coordinates[0]][self.space_coordinates[1]], \
                self.state[self.space_coordinates[0]][self.space_coordinates[1] - 1] = \
                self.state[self.space_coordinates[0]][self.space_coordinates[1] - 1], \
                self.state[self.space_coordinates[0]][self.space_coordinates[1]]
            self.space_coordinates[1] -= 1

    def scramble(self):
        switchers = {
            0: self.up,
            1: self.down,
            2: self.left,
            3: self.right
        }
        movements = list()
        for times in range(100):
            function = switchers.get(random.randint(0, 3))
            movements.append(function.__name__)
            function()
        print("CURRENT STATE : ")
        self.print_puzzle()
        return movements

    def solved(self):
        return str(self.state) == str(self.end)

    def print_puzzle(self):
        space_value = 0
        if self.size > 3:
            space_value = 1
            space_value += (2 - len(str((self.size * self.size) - 1)))
        bias2 = (self.size * (4 + (0 if self.size < 4 else 1)) + 1)
        bias = (self.size * (4 + space_value) + 1)
        for i in range(bias):
            print("+" if i == 0 or i == bias - 1 else "-", end="")
        print()
        for row in self.state:
            print("|", end="")
            for column in row:
                zeros = ""
                if self.size > 3:
                    r = abs(len(str(column)) - len(str((self.size * self.size) - 1)))
                    for _ in range(r):
                        zeros += "0"
                print(" " + zeros + str(column) + " |", end="")
            print()
            for i in range(bias):
                print("+" if i == 0 or i == bias - 1 else "-", end="")
            print()

    def populate(self):
        value = 1
        for i in range(self.size):
            for j in range(self.size):
                self.state[i][j] = value
                value += 1
        self.state[self.space_coordinates[0]][self.space_coordinates[1]] = 0
        self.end = copy.deepcopy(self.state)

    def set_new_puzzle(self, puzzle):
        self.state = puzzle.state
        self.space_coordinates = puzzle.space_coordinates
