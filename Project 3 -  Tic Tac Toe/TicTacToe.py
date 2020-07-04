"""
Tic Tac Toe
Jimmy Tran
"""

import time
from enum import Enum


class GameBoardPlayer(Enum):
    """
    An enum that represents a player on a game board; it's used to denote:
    . which player occupies a space on the board (can be NONE if unoccupied)
    . which player is the winner of the game (can be DRAW)
    """
    NONE = 0
    X = 1
    O = 2
    DRAW = 3

    def __str__(self):
        if self in [self.X, self.O, self.DRAW]:
            return self.name
        elif self == self.NONE:
            return " "


class ArrayGameBoard:
    """A class that represents a rectangular game board"""

    def __init__(self, nrows, ncols):
        if not (int(nrows) > 0 and int(ncols) > 0):
            raise ValueError("At least one of these is not a positive integer.")
        self.nrows = nrows
        self.ncols = ncols
        self.board = [[GameBoardPlayer.NONE] * self.ncols for _ in range(self.nrows)]

    def get_nrows(self):
        return len(self.board)

    def get_ncols(self):
        return len(self.board[1])

    def set(self, row, col, value):
        self.board[row][col] = value

    def get(self, row, col):
        return self.board[row][col]

    def __str__(self):
        borders = "+".join(["-"] * self.get_ncols())
        board_str = ""
        first = True
        for row in range(self.get_nrows()):
            if first:
                first = False
            else:
                board_str += f"{borders}\n"
            second = True
            for col in range(self.get_ncols()):
                if second:
                    second = False
                else:
                    board_str += "|"
                board_str += f"{self.get(row, col)}"
            board_str += "\n"
        return board_str

    def get_winner(self):
        one_dimensional_board = []
        for row in range(self.get_nrows()):
            for col in range(self.get_ncols()):
                one_dimensional_board.append(self.get(row, col))
        if GameBoardPlayer.NONE not in one_dimensional_board:
            return GameBoardPlayer.DRAW
        else:
            # check columns
            for j in range(self.get_ncols()):
                tiny_list = one_dimensional_board[j::self.get_ncols()]
                tiny_set = set(tiny_list)
                if len(tiny_set) == 1 & \
                        GameBoardPlayer(tiny_list[0]).value is not GameBoardPlayer.NONE.value:
                    return GameBoardPlayer(tiny_list[0])
            for k in range(self.get_nrows()):
                factor = self.get_ncols() * k
                tiny_list = one_dimensional_board[0 + factor:self.get_ncols() + factor]
                tiny_set = set(tiny_list)
                if len(tiny_set) == 1 & \
                        GameBoardPlayer(tiny_list[0]).value in [GameBoardPlayer.X.value, GameBoardPlayer.O.value]:
                    return GameBoardPlayer(tiny_list[0])
            # check diagonals if square
            if self.get_nrows() == self.get_ncols():
                # first diagonal
                tiny_list = one_dimensional_board[0::self.get_ncols() + 1]
                tiny_set = set(tiny_list)
                if len(tiny_set) == 1 & \
                        GameBoardPlayer(tiny_list[0]).value in [GameBoardPlayer.X.value, GameBoardPlayer.O.value]:
                    return GameBoardPlayer(tiny_list[0])
                # second diagonal
                tiny_list = one_dimensional_board[self.get_ncols()::self.get_nrows() - 1]
                tiny_set = set(tiny_list)
                if len(tiny_set) == 1 & \
                        GameBoardPlayer(tiny_list[0]).value in [GameBoardPlayer.X.value, GameBoardPlayer.O.value]:
                    return GameBoardPlayer(tiny_list[0])
            return GameBoardPlayer.NONE


class BitGameBoard:
    """A class that represents a rectangular game board"""

    def __init__(self, nrows, ncols):
        if not (int(nrows) > 0 and int(ncols) > 0):
            raise ValueError("At least one of these is not a positive integer.")
        self.board = GameBoardPlayer.NONE.value
        self.nrows = nrows
        self.ncols = ncols

    def get_nrows(self):
        return self.nrows

    def get_ncols(self):
        return self.ncols

    def set(self, row, col, player):
        if (row < 0 or row > self.get_nrows()) & (col < 0 or col > self.get_ncols()):
            raise IndexError
        else:
            index = row * self.get_ncols() * 2 + col * 2
            mask = 0b11 << index
            self.board &= ~mask
            self.board |= player.value << index

    def get(self, row, col):
        if (row < 0 or row > self.get_nrows()) & (col < 0 or col > self.get_ncols()):
            raise IndexError
        else:
            index = row * self.get_ncols() * 2 + col * 2
            mask = 0b11
            new_board = self.board >> index
            new_board &= mask
            return GameBoardPlayer(new_board)

    def __str__(self):
        borders = "+".join(["-"] * self.get_ncols())
        board_str = ""
        first = True
        for row in range(self.get_nrows()):
            if first:
                first = False
            else:
                board_str += f"{borders}\n"
            second = True
            for col in range(self.get_ncols()):
                if second:
                    second = False
                else:
                    board_str += "|"
                board_str += f"{self.get(row, col)}"
            board_str += "\n"
        return board_str

    def get_winner(self):
        one_dimensional_board = []
        for row in range(self.get_nrows()):
            for col in range(self.get_ncols()):
                one_dimensional_board.append(self.get(row, col))
        if GameBoardPlayer.NONE not in one_dimensional_board:
            return GameBoardPlayer.DRAW
        else:
            # check columns
            for j in range(self.get_ncols()):
                tiny_list = one_dimensional_board[j::self.get_ncols()]
                tiny_set = set(tiny_list)
                if len(tiny_set) == 1 & \
                        GameBoardPlayer(tiny_list[0]).value is not GameBoardPlayer.NONE.value:
                    return GameBoardPlayer(tiny_list[0])
            for k in range(self.get_nrows()):
                factor = self.get_ncols() * k
                tiny_list = one_dimensional_board[0 + factor:self.get_ncols() + factor]
                tiny_set = set(tiny_list)
                if len(tiny_set) == 1 & \
                        GameBoardPlayer(tiny_list[0]).value in [GameBoardPlayer.X.value, GameBoardPlayer.O.value]:
                    return GameBoardPlayer(tiny_list[0])
            # check diagonals if square
            if self.get_nrows() == self.get_ncols():
                # first diagonal
                tiny_list = one_dimensional_board[0::self.get_ncols() + 1]
                tiny_set = set(tiny_list)
                if len(tiny_set) == 1 & \
                        GameBoardPlayer(tiny_list[0]).value in [GameBoardPlayer.X.value, GameBoardPlayer.O.value]:
                    return GameBoardPlayer(tiny_list[0])
                # second diagonal
                tiny_list = one_dimensional_board[self.get_ncols()::self.get_nrows() - 1]
                tiny_set = set(tiny_list)
                if len(tiny_set) == 1 & \
                        GameBoardPlayer(tiny_list[0]).value in [GameBoardPlayer.X.value, GameBoardPlayer.O.value]:
                    return GameBoardPlayer(tiny_list[0])
            return GameBoardPlayer.NONE


class TicTacToeBoard:
    """
    A class that represents a Tic Tac Toe game board.
    It's a thin wrapper around the actual game board
    """
    NROWS = 3
    NCOLS = 3

    def __init__(self):
        # The two game boards can be used interchangeably.
        # self.board = ArrayGameBoard(self.NROWS, self.NCOLS)
        self.board = BitGameBoard(self.NROWS, self.NCOLS)

    def set(self, row, col, value):
        if self.board.get(row, col) != GameBoardPlayer.NONE:
            raise ValueError(f"{row} {col} already has {self.board.get(row, col)}")
        self.board.set(row, col, value)

    def get(self, row, col):
        return self.board.get(row, col)

    def get_winner(self):
        return self.board.get_winner()

    def __str__(self):
        return self.board.__str__()


class HumanPlayer:
    """A class that represents a human planer"""

    def __init__(self, side):
        self.side = side

    def __str__(self):
        return f"Human player {self.side}"

    def get_move(self, board):
        """Get a move from the player; the board parameter is unused for now"""
        start = time.perf_counter()
        while True:
            try:
                moves = input(f"Please input move for {self} (row column): ")
                row, col = moves.split()
                return int(row), int(col), (time.perf_counter() - start)
            except ValueError as e:
                print(f"Invalid input '{moves}':", e)


def ttt_game():
    """
    Play a round of Tic Tac Toe, until there's either a winner, or the game
    is a draw.
    """
    ttt_board = TicTacToeBoard()
    player1 = HumanPlayer(GameBoardPlayer.X)
    player2 = HumanPlayer(GameBoardPlayer.O)
    current_player = player1

    print(ttt_board)
    while True:
        row, col, duration = current_player.get_move(ttt_board)
        print(f"{current_player} makes move ({row} {col}) in {duration:.6f} seconds")
        try:
            ttt_board.set(row, col, current_player.side)
        except (ValueError, IndexError) as e:
            # ValueError if the space is already occupied, IndexError if off-grid
            print(e)
            continue
        print(ttt_board)

        winner = ttt_board.get_winner()
        if winner is GameBoardPlayer.DRAW:
            print("Game is a draw")
            break
        elif winner is GameBoardPlayer.NONE:
            # Switch player
            current_player = player1 if current_player is player2 else player2
        else:
            # There's a winner
            print(f"{current_player} wins")
            break


def test_game_board():
    gb = ArrayGameBoard(3, 3)

    # get() and set() behave correctly when row and col are valid
    # get_winner() correctly returns the winner that occupies a row
    gb.set(0, 0, GameBoardPlayer.X)
    gb.set(0, 1, GameBoardPlayer.X)
    gb.set(0, 2, GameBoardPlayer.X)
    print("gb.get(0, 0) returns", gb.get(0, 0))
    print("gb.get(0, 1) returns", gb.get(0, 1))
    print("gb.get(0, 2) returns", gb.get(0, 2))
    # __str__() is implemented properly
    print(gb)
    # get_winner() correctly returns the winner that occupies a row
    print(f"winner of board with 1 row of X is '{gb.get_winner()}'")

    gb = ArrayGameBoard(3, 3)
    # get_winner() correctly returns the winner that occupies a column
    gb.set(0, 0, GameBoardPlayer.X)
    gb.set(1, 0, GameBoardPlayer.X)
    gb.set(2, 0, GameBoardPlayer.X)
    # __str__() is implemented properly
    print(gb)
    # get_winner() correctly returns the winner that occupies a row
    print(f"winner of board with 1 row of X is '{gb.get_winner()}'")

    # get_winner() correctly returns the winner that occupies a diagonal
    gb = ArrayGameBoard(3, 3)
    gb.set(0, 0, GameBoardPlayer.X)
    gb.set(1, 1, GameBoardPlayer.X)
    gb.set(2, 2, GameBoardPlayer.X)
    # __str__() is implemented properly
    print(gb)
    # get_winner() correctly returns the winner that occupies a row
    print(f"winner of board with 1 row of X is '{gb.get_winner()}'")

    # get_winner() correctly returns DRAW if the game has no winner and there is not more unoccupied space
    gb = ArrayGameBoard(3, 3)
    gb.set(0, 0, GameBoardPlayer.X)
    # __str__() is implemented properly
    print(gb)
    # get_winner() correctly returns the winner that occupies a row
    print(f"winner of board with 1 row of X is '{gb.get_winner()}'")

    # get_winner() correctly returns NONE if the game has no winner yet and there are more unoccupied spaces
    gb = ArrayGameBoard(3, 3)
    gb.set(0, 0, GameBoardPlayer.O)
    gb.set(0, 1, GameBoardPlayer.X)
    gb.set(0, 2, GameBoardPlayer.O)
    gb.set(1, 0, GameBoardPlayer.X)
    gb.set(1, 1, GameBoardPlayer.O)
    gb.set(1, 2, GameBoardPlayer.X)
    gb.set(2, 0, GameBoardPlayer.O)
    gb.set(2, 1, GameBoardPlayer.X)
    gb.set(2, 2, GameBoardPlayer.X)
    # __str__() is implemented properly
    print(gb)
    # get_winner() correctly returns the winner that occupies a row
    print(f"winner of board with 1 row of X is '{gb.get_winner()}'")

    # get() and set() raise IndexError when row and col are invalid
    try:
        gb.get(100, 100)
        print("gb.get(100, 100) fails to raise IndexError")
    except IndexError:
        print("gb.get(100, 100) correctly raises IndexError")

    try:
        gb.set(100, 100, GameBoardPlayer.X)
        print("gb.set(100, 100, GameBoardPlayer.X) fails to raise IndexError")
    except IndexError:
        print("gb.set(100, 100, GameBoardPlayer.X) correctly raises IndexError")


def test_game_board_bit():
    gb = BitGameBoard(3, 3)

    # get() and set() behave correctly when row and col are valid
    # get_winner() correctly returns the winner that occupies a row
    gb.set(0, 0, GameBoardPlayer.X)
    gb.set(0, 1, GameBoardPlayer.X)
    gb.set(0, 2, GameBoardPlayer.X)
    print("gb.get(0, 0) returns", gb.get(0, 0))
    print("gb.get(0, 1) returns", gb.get(0, 1))
    print("gb.get(0, 2) returns", gb.get(0, 2))
    # __str__() is implemented properly
    print(gb)
    # get_winner() correctly returns the winner that occupies a row
    print(f"winner of board with 1 row of X is '{gb.get_winner()}'")

    gb = BitGameBoard(3, 3)
    # get_winner() correctly returns the winner that occupies a column
    gb.set(0, 0, GameBoardPlayer.O)
    gb.set(1, 0, GameBoardPlayer.O)
    gb.set(2, 0, GameBoardPlayer.O)
    # __str__() is implemented properly
    print(gb)
    # get_winner() correctly returns the winner that occupies a row
    print(f"winner of board with 1 row of X is '{gb.get_winner()}'")

    # get_winner() correctly returns the winner that occupies a diagonal
    gb = BitGameBoard(3, 3)
    gb.set(0, 0, GameBoardPlayer.X)
    gb.set(1, 1, GameBoardPlayer.X)
    gb.set(2, 2, GameBoardPlayer.X)
    # __str__() is implemented properly
    print(gb)
    # get_winner() correctly returns the winner that occupies a row
    print(f"winner of board with 1 row of X is '{gb.get_winner()}'")

    # get_winner() correctly returns DRAW if the game has no winner and there is not more unoccupied space
    gb = BitGameBoard(3, 3)
    gb.set(0, 0, GameBoardPlayer.X)
    # __str__() is implemented properly
    print(gb)
    # get_winner() correctly returns the winner that occupies a row
    print(f"winner of board with 1 row of X is '{gb.get_winner()}'")

    # get_winner() correctly returns NONE if the game has no winner yet and there are more unoccupied spaces
    gb = BitGameBoard(3, 3)
    gb.set(0, 0, GameBoardPlayer.O)
    gb.set(0, 1, GameBoardPlayer.X)
    gb.set(0, 2, GameBoardPlayer.O)
    gb.set(1, 0, GameBoardPlayer.X)
    gb.set(1, 1, GameBoardPlayer.O)
    gb.set(1, 2, GameBoardPlayer.X)
    gb.set(2, 0, GameBoardPlayer.O)
    gb.set(2, 1, GameBoardPlayer.X)
    gb.set(2, 2, GameBoardPlayer.X)
    # __str__() is implemented properly
    print(gb)
    # get_winner() correctly returns the winner that occupies a row
    print(f"winner of board with 1 row of X is '{gb.get_winner()}'")

    # get() and set() raise IndexError when row and col are invalid
    try:
        gb.get(100, 100)
        print("gb.get(100, 100) fails to raise IndexError")
    except IndexError:
        print("gb.get(100, 100) correctly raises IndexError")

    try:
        gb.set(100, 100, GameBoardPlayer.X)
        print("gb.set(100, 100, GameBoardPlayer.X) fails to raise IndexError")
    except IndexError:
        print("gb.set(100, 100, GameBoardPlayer.X) correctly raises IndexError")


if __name__ == '__main__':
    # test_game_board()
    test_game_board_bit()
    # ttt_game()
    # ttt_game()
    # ttt_game()