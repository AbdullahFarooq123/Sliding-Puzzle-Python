import copy
import math
import Node
import Puzzle as Puzzle


class Bot:
    def __init__(self, puzzle: Puzzle.Puzzle):
        self.puzzle = puzzle

    def calculate_heuristics(self, puzzle):
        heuristics = 0
        for row in range(puzzle.size):
            for column in range(puzzle.size):
                if not puzzle.state[row][column] == 0:
                    heuristics += self.get_distance(puzzle.state[row][column], [row, column])
        return heuristics

    def get_distance(self, tile, location):
        for row in range(self.puzzle.size):
            for column in range(self.puzzle.size):
                if self.puzzle.end[row][column] == tile:
                    return abs(location[0] - row) + abs(location[1] - column)
        return math.inf

    def get_next_states(self, current_state: Node.Node):
        states = list()
        moves = {'up': [-1, 0], 'down': [1, 0], 'left': [0, -1], 'right': [0, 1]}
        for move in moves:
            new_space_coordinates = [current_state.current_state.space_coordinates[0] + moves.get(move)[0],
                                     current_state.current_state.space_coordinates[1] + moves.get(move)[1]]
            if 0 <= new_space_coordinates[0] < self.puzzle.size and \
                    0 <= new_space_coordinates[1] < self.puzzle.size:
                states.append(self.get_new_state(move, copy.deepcopy(current_state)))
        return states

    def get_new_state(self, move_name: str, current_state: Node.Node):
        current_state.depth += 1
        current_state.previous_state = copy.deepcopy(current_state.current_state)
        current_state.move = move_name
        if move_name == 'up':
            current_state.current_state.up()
        elif move_name == 'down':
            current_state.current_state.down()
        elif move_name == 'right':
            current_state.current_state.right()
        else:
            current_state.current_state.left()
        current_state.heuristics = self.calculate_heuristics(current_state.current_state)
        return current_state

    @staticmethod
    def get_best_state(states_to_visit: dict) -> Node.Node:
        best_state = None
        best_heuristics = math.inf
        for state in states_to_visit.values():
            if state.get_heuristics() < best_heuristics:
                best_state = state
                best_heuristics = best_state.get_heuristics()
        return best_state

    def print_path(self, visited_states: dir):
        steps = list()
        moves = list()
        state = visited_states[str(self.puzzle.end)]
        while True:
            if state.move == '':
                steps.append(state)
                break
            steps.append(state)
            state = visited_states[str(state.previous_state.state)]
        steps.reverse()
        for step in steps:
            self.print_puzzle(step)
            if step.move not in '':
                moves.append(step.move)
        return moves

    @staticmethod
    def print_puzzle(state: Node.Node):
        if state.move == '':
            print("--|INPUT|--")
        else:
            print("--|"+state.move+"|--")
        state.current_state.print_puzzle()

    def solve(self):
        states_to_visit = {str(self.puzzle.state): Node.Node(self.puzzle, 0, self.calculate_heuristics(self.puzzle),
                                                             '', self.puzzle)}
        visited_states = {}
        while True:
            test_state = self.get_best_state(states_to_visit)
            visited_states[str(test_state.current_state.state)] = test_state
            if test_state.current_state.solved():
                print("STEPS : " + str(test_state.depth))
                return self.print_path(visited_states), test_state.current_state
            next_states = self.get_next_states(test_state)
            for state in next_states:
                if not (str(state.current_state.state) in visited_states.keys()
                        or (str(state.current_state.state) in states_to_visit.keys()
                            and (states_to_visit[str(state.current_state.state)]).get_heuristics() <
                            state.get_heuristics())):
                    states_to_visit[str(state.current_state.state)] = state
            del states_to_visit[str(test_state.current_state.state)]
