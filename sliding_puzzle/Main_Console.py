import Puzzle
import Bot


def main():
    size = int(input("Enter the size of puzzle : "))
    puzzle = Puzzle.Puzzle(size, [[0 for _ in range(size)] for _ in range(size)], [size - 1, size - 1])
    puzzle.populate()
    moves = puzzle.scramble()
    print("SCRAMBLED PUZZLE : ")
    puzzle.print_puzzle()
    print("SOLVED : ", end=" ")
    Bot.Bot(puzzle).solve()


if __name__ == '__main__':
    main()
