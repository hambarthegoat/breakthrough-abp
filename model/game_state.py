from copy import deepcopy
from typing import List, Optional


class GameState:
    EMPTY = 0
    WHITE = 1
    BLACK = 2

    BOARD_SIZE = 8

    def __init__(self, board: Optional[List[List[int]]] = None):
        if board is None:
            self.board = [
                [self.EMPTY for _ in range(self.BOARD_SIZE)]
                for _ in range(self.BOARD_SIZE)
            ]
        else:
            self.board = board

        self.current_player = self.WHITE
        self.winner = None
        self.move_history = []

    def get_piece(self, row: int, col: int) -> int:
        if self.is_valid_position(row, col):
            return self.board[row][col]
        return -1

    def set_piece(self, row: int, col: int, piece: int) -> None:
        if self.is_valid_position(row, col):
            self.board[row][col] = piece

    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE

    def switch_player(self) -> None:
        self.current_player = (
            self.BLACK if self.current_player == self.WHITE else self.WHITE
        )

    def set_winner(self, winner: int) -> None:
        self.winner = winner

    def get_winner(self) -> Optional[int]:
        return self.winner

    def add_to_history(self, from_pos: tuple, to_pos: tuple) -> None:
        self.move_history.append((from_pos, to_pos))

    def get_last_move(self) -> Optional[tuple]:
        return self.move_history[-1] if self.move_history else None

    def copy(self) -> "GameState":
        new_state = GameState(deepcopy(self.board))
        new_state.current_player = self.current_player
        new_state.winner = self.winner
        new_state.move_history = self.move_history.copy()
        return new_state

    def count_pieces(self, player: int) -> int:
        count = 0
        for row in self.board:
            for piece in row:
                if piece == player:
                    count += 1
        return count

    def get_piece_positions(self, player: int) -> List[tuple]:
        positions = []
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] == player:
                    positions.append((row, col))
        return positions
