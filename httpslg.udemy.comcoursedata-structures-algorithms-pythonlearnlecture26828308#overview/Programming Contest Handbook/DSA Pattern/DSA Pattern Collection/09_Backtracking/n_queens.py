"""
N-Queens
Place n queens on an n x n chessboard so that no two queens attack each other.
Return all distinct solutions.

Idea: place one queen per row. Track occupied columns and the two diagonals
(main diagonal: col - row, anti-diagonal: col + row). Backtrack when a
placement conflicts.

Time: O(n!) with pruning
Space: O(n)
"""


def solve_n_queens(n):
    cols = set()
    diag1 = set()   # r - c
    diag2 = set()   # r + c
    board = [["."] * n for _ in range(n)]
    result = []

    def backtrack(row):
        if row == n:
            result.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board[row][col] = "Q"
            backtrack(row + 1)
            board[row][col] = "."
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return result


if __name__ == "__main__":
    solutions = solve_n_queens(4)
    print(len(solutions))   # 2
    for s in solutions:
        print(s)
        print()
