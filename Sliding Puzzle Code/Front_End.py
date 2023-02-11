import pygame


class GUI:
    move_list = list()

    def __init__(self, image_file_name, image_size, puzzle_size, pos, show_scramble=False) -> None:
        self.loaded_image = pygame.image.load(image_file_name)
        self.loaded_image = pygame.transform.scale(self.loaded_image, image_size)

        self.pos = pos
        self.dim = image_size
        self.solve = False
        self.scrambling = False
        self.size = puzzle_size

        self.puzzle = []
        for i in range(puzzle_size[0]):
            self.puzzle.append([])
            for j in range(puzzle_size[1]):
                self.puzzle[i].append((i, j))


        self.void = (puzzle_size[0] - 1, puzzle_size[1] - 1)
        self.puzzle[self.void[0]][self.void[1]] = (-1, -1)

        self.show_scramble = show_scramble
        self.scramble_moves = 0
        self.moves = [self.move_up, self.move_down, self.move_left, self.move_right]

        self.animating = None
        self.buffer = (0, 0)
        self.ANIMATION_SPEED = 0.1

        self.revealing = False
        self.revealing_animation = 0
        self.REVEALING_ANIMATION_SPEED = 5

    def render(self, screen):
        pos = self.pos
        dim = self.dim
        cell_width = dim[0] // self.size[0]
        cell_height = dim[1] // self.size[1]

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.animating == (i, j):
                    screen.blit(self.loaded_image, (pos[0] + i * cell_width + int(self.buffer[0] * cell_width),
                                                    pos[1] + j * cell_height + int(self.buffer[1] * cell_height)), (
                                    self.puzzle[i][j][0] * cell_width, self.puzzle[i][j][1] * cell_height, cell_width,
                                    cell_height))
                else:
                    screen.blit(self.loaded_image, (pos[0] + i * cell_width, pos[1] + j * cell_height), (
                        self.puzzle[i][j][0] * cell_width, self.puzzle[i][j][1] * cell_height, cell_width, cell_height))

        for i in range(self.size[0] + 1):
            pygame.draw.line(screen, [0] * 3, (pos[0] + i * cell_width, pos[1]),
                             (pos[0] + i * cell_width, pos[1] + self.size[1] * cell_height), 10)

        for j in range(self.size[1] + 1):
            pygame.draw.line(screen, [0] * 3, (pos[0], pos[1] + j * cell_height),
                             (pos[0] + self.size[0] * cell_width, pos[1] + j * cell_height), 10)

    def reveal(self, screen):
        if not self.revealing:
            self.revealing = True
            self.revealing_animation = 255

        image = self.loaded_image.copy()
        image.set_alpha(255 - self.revealing_animation)
        screen.blit(image, self.pos)

    def __reduce_buffer(self):
        if self.buffer[0] > 0:
            self.buffer = (max(0.0, self.buffer[0] - self.ANIMATION_SPEED), self.buffer[1])

        if self.buffer[0] < 0:
            self.buffer = (min(0.0, self.buffer[0] + self.ANIMATION_SPEED), self.buffer[1])

        if self.buffer[1] > 0:
            self.buffer = (self.buffer[0], max(0.0, self.buffer[1] - self.ANIMATION_SPEED))

        if self.buffer[1] < 0:
            self.buffer = (self.buffer[0], min(0.0, self.buffer[1] + self.ANIMATION_SPEED))

    def move_up(self, animate=True, anim_time=1):
        if self.void[1] < self.size[1] - 1:
            self.puzzle[self.void[0]][self.void[1]] = self.puzzle[self.void[0]][self.void[1] + 1]
            self.puzzle[self.void[0]][self.void[1] + 1] = (-1, -1)
            self.void = (self.void[0], self.void[1] + 1)
            if animate:
                self.animating = (self.void[0], self.void[1] - 1)
                self.buffer = (0, 1 * anim_time)

    def move_down(self, animate=True, anim_time=1):
        if self.void[1] > 0:
            self.puzzle[self.void[0]][self.void[1]] = self.puzzle[self.void[0]][self.void[1] - 1]
            self.puzzle[self.void[0]][self.void[1] - 1] = (-1, -1)
            self.void = (self.void[0], self.void[1] - 1)
            if animate:
                self.animating = (self.void[0], self.void[1] + 1)
                self.buffer = (0, -1 * anim_time)

    def move_left(self, animate=True, anim_time=1):
        if self.void[0] < self.size[0] - 1:
            self.puzzle[self.void[0]][self.void[1]] = self.puzzle[self.void[0] + 1][self.void[1]]
            self.puzzle[self.void[0] + 1][self.void[1]] = (-1, -1)
            self.void = (self.void[0] + 1, self.void[1])
            if animate:
                self.animating = (self.void[0] - 1, self.void[1])
                self.buffer = (1 * anim_time, 0)

    def move_right(self, animate=True, anim_time=1):
        if self.void[0] > 0:
            self.puzzle[self.void[0]][self.void[1]] = self.puzzle[self.void[0] - 1][self.void[1]]
            self.puzzle[self.void[0] - 1][self.void[1]] = (-1, -1)
            self.void = (self.void[0] - 1, self.void[1])
            if animate:
                self.animating = (self.void[0] + 1, self.void[1])
                self.buffer = (-1 * anim_time, 0)

    def is_solved(self, animate=True):
        if self.scramble_moves > 0:
            return False
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.puzzle[i][j] != (-1, -1) and self.puzzle[i][j] != (i, j):
                    return False
        return True

    def update(self):
        if self.animating is not None:
            self.__reduce_buffer()
            if self.buffer == (0, 0):
                self.animating = None
        elif (len(self.move_list) > 0) and self.scrambling:
            self.scramble()
        elif (len(self.move_list) > 0) and self.solve:
            self.solve_puzzle()
        elif self.revealing:
            if self.revealing_animation > 0:
                self.revealing_animation = max(0, self.revealing_animation - self.REVEALING_ANIMATION_SPEED)

    def moves_allowed(self):
        if len(self.move_list) > 0:
            return False
        if self.animating is not None:
            return False
        if self.is_solved():
            return False
        return True

    def scramble(self):
        scrambles = {
            'up': self.move_down,
            'down': self.move_up,
            'left': self.move_right,
            'right': self.move_left
        }
        scrambles.get(self.move_list.pop(0))(anim_time=0)
        if len(self.move_list) == 0:
            self.scrambling = False

    def solve_puzzle(self):
        scrambles = {
            'up': self.move_down,
            'down': self.move_up,
            'left': self.move_right,
            'right': self.move_left
        }
        scrambles.get(self.move_list.pop(0))(anim_time=1)
        if len(self.move_list) == 0:
            self.solve = False

