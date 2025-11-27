from typing import Tuple

from model.game_state import GameState
from model.move_validator import MoveValidator


class GameRules:
    @staticmethod
    def setup_initial_position(state: GameState, human_player: int = None) -> None:
        if human_player == GameState.WHITE:
            for row in range(6, 8):
                for col in range(state.BOARD_SIZE):
                    state.set_piece(row, col, GameState.WHITE)

            for row in range(2):
                for col in range(state.BOARD_SIZE):
                    state.set_piece(row, col, GameState.BLACK)
        else:
            for row in range(2):
                for col in range(state.BOARD_SIZE):
                    state.set_piece(row, col, GameState.WHITE)

            for row in range(6, 8):
                for col in range(state.BOARD_SIZE):
                    state.set_piece(row, col, GameState.BLACK)

        state.current_player = GameState.WHITE

    @staticmethod
    def check_win_condition(
        state: GameState, row: int, piece: int, human_player: int = None
    ) -> bool:
        if human_player == GameState.WHITE:
            if piece == GameState.WHITE and row == 0:
                return True
            if piece == GameState.BLACK and row == state.BOARD_SIZE - 1:
                return True
        else:
            if piece == GameState.WHITE and row == state.BOARD_SIZE - 1:
                return True
            if piece == GameState.BLACK and row == 0:
                return True

        return False

    @staticmethod
    def is_game_over(state: GameState) -> bool:
        if state.winner is not None:
            return True

        if not MoveValidator.has_valid_moves(state, state.current_player):
            opponent = (
                GameState.BLACK
                if state.current_player == GameState.WHITE
                else GameState.WHITE
            )
            state.set_winner(opponent)
            return True

        return False

    @staticmethod
    def execute_move(
        state: GameState,
        from_pos: Tuple[int, int],
        to_pos: Tuple[int, int],
        human_player: int = None,
    ) -> bool:
        if not MoveValidator.is_valid_move(state, from_pos, to_pos):
            return False

        from_row, from_col = from_pos
        to_row, to_col = to_pos

        piece = state.get_piece(from_row, from_col)
        state.set_piece(to_row, to_col, piece)
        state.set_piece(from_row, from_col, GameState.EMPTY)

        state.add_to_history(from_pos, to_pos)

        if GameRules.check_win_condition(state, to_row, piece, human_player):
            state.set_winner(piece)
        else:
            state.switch_player()

        return True

    @staticmethod
    def get_opponent(player: int) -> int:
        return GameState.BLACK if player == GameState.WHITE else GameState.WHITE
