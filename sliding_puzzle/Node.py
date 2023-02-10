import Puzzle


class Node:
    def __init__(self, current_state: Puzzle.Puzzle, depth: int, heuristics: int, move: str,
                 previous_state: Puzzle.Puzzle):
        self.current_state = current_state
        self.move = move
        self.depth = depth
        self.heuristics = heuristics
        self.previous_state = previous_state

    def get_heuristics(self):
        return self.depth + self.heuristics
