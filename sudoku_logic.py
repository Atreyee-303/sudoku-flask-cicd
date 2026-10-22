
import random

SIZE = 9

def is_valid(board, row, col, num):
    """Check whether num can be placed at the given position."""
    for i in range(SIZE):
        if board[row][i] == num:
            return False
        if board[i][col] == num:
            return False

    start_row = (row // 3) * 3
    start_col = (col // 3) * 3

    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False

    return True

def solve_board(board):
    """Fill an empty Sudoku board using backtracking."""
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == 0:
                numbers = list(range(1, 10))
                random.shuffle(numbers)

                for num in numbers:
                    if is_valid(board, row, col, num):
                        board[row][col] = num

                        if solve_board(board):
                            return True

                        board[row][col] = 0

                return False

    return True

def generate_game():
    """Generate a completed Sudoku solution and a playable puzzle."""
    solution = [[0] * SIZE for _ in range(SIZE)]
    solve_board(solution)

    puzzle = [row[:] for row in solution]

    # Remove 40 cells to create the puzzle.
    cells = [(r, c) for r in range(SIZE) for c in range(SIZE)]
    random.shuffle(cells)

    for row, col in cells[:40]:
        puzzle[row][col] = 0

    return puzzle, solution
