from typing import List, Tuple

from model.game_state import GameState


class MoveValidator:
    @staticmethod
    def get_valid_moves(state: GameState, row: int, col: int) -> List[Tuple[int, int]]:
        piece = state.get_piece(row, col)

        if piece != state.current_player:
            return []

        moves = []

        # Determine direction based on board orientation
        if hasattr(state, 'human_player') and state.human_player == GameState.WHITE:
            # White at bottom (rows 6-7), moves up (decreasing row)
            direction = -1 if piece == GameState.WHITE else 1
        else:
            # White at top (rows 0-1), moves down (increasing row)
            direction = 1 if piece == GameState.WHITE else -1
        new_row = row + direction

        if state.is_valid_position(new_row, col):
            if state.get_piece(new_row, col) == GameState.EMPTY:
                moves.append((new_row, col))

        for col_offset in [-1, 1]:
            new_col = col + col_offset

            if state.is_valid_position(new_row, new_col):
                target = state.get_piece(new_row, new_col)

                if target == GameState.EMPTY:
                    moves.append((new_row, new_col))
                elif target != piece and target != GameState.EMPTY:
                    moves.append((new_row, new_col))

        return moves

    @staticmethod
    def get_all_valid_moves(
        state: GameState, player: int
    ) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        all_moves = []

        for row in range(state.BOARD_SIZE):
            for col in range(state.BOARD_SIZE):
                if state.get_piece(row, col) == player:
                    valid_destinations = MoveValidator.get_valid_moves(state, row, col)
                    for dest in valid_destinations:
                        all_moves.append(((row, col), dest))

        return all_moves

    @staticmethod
    def is_valid_move(
        state: GameState, from_pos: Tuple[int, int], to_pos: Tuple[int, int]
    ) -> bool:
        from_row, from_col = from_pos

        valid_moves = MoveValidator.get_valid_moves(state, from_row, from_col)
        return to_pos in valid_moves

    @staticmethod
    def has_valid_moves(state: GameState, player: int) -> bool:
        return len(MoveValidator.get_all_valid_moves(state, player)) > 0
