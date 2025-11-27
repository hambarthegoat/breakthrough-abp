from model.game_state import GameState
from model.move_validator import MoveValidator


class PositionEvaluator:
    MATERIAL_VALUE = 100
    ADVANCEMENT_VALUE = 10
    MOBILITY_VALUE = 5
    WIN_VALUE = 10000

    @staticmethod
    def evaluate(state: GameState, player: int, human_player: int = None) -> float:
        if state.winner == player:
            return PositionEvaluator.WIN_VALUE
        elif state.winner is not None:
            return -PositionEvaluator.WIN_VALUE

        opponent = GameState.BLACK if player == GameState.WHITE else GameState.WHITE
        score = 0.0

        score += PositionEvaluator._evaluate_material_and_position(
            state, player, human_player
        )
        score -= PositionEvaluator._evaluate_material_and_position(
            state, opponent, human_player
        )

        score += PositionEvaluator._evaluate_mobility(state, player, opponent)

        return score

    @staticmethod
    def _evaluate_material_and_position(
        state: GameState, player: int, human_player: int = None
    ) -> float:
        score = 0.0

        for row in range(state.BOARD_SIZE):
            for col in range(state.BOARD_SIZE):
                piece = state.get_piece(row, col)

                if piece == player:
                    score += PositionEvaluator.MATERIAL_VALUE

                    advancement = PositionEvaluator._calculate_advancement(
                        row, player, state.BOARD_SIZE, human_player
                    )
                    score += advancement * PositionEvaluator.ADVANCEMENT_VALUE

        return score

    @staticmethod
    def _calculate_advancement(
        row: int, player: int, board_size: int, human_player: int = None
    ) -> int:
        if human_player == GameState.WHITE:
            if player == GameState.WHITE:
                return (board_size - 1) - row
            else:
                return row
        else:
            if player == GameState.WHITE:
                return row
            else:
                return (board_size - 1) - row

    @staticmethod
    def _evaluate_mobility(state: GameState, player: int, opponent: int) -> float:
        player_moves = len(MoveValidator.get_all_valid_moves(state, player))
        opponent_moves = len(MoveValidator.get_all_valid_moves(state, opponent))

        return (player_moves - opponent_moves) * PositionEvaluator.MOBILITY_VALUE

    @staticmethod
    def quick_evaluate(
        state: GameState, player: int, human_player: int = None
    ) -> float:
        if state.winner == player:
            return PositionEvaluator.WIN_VALUE
        elif state.winner is not None:
            return -PositionEvaluator.WIN_VALUE

        opponent = GameState.BLACK if player == GameState.WHITE else GameState.WHITE

        score = PositionEvaluator._evaluate_material_and_position(
            state, player, human_player
        )
        score -= PositionEvaluator._evaluate_material_and_position(
            state, opponent, human_player
        )

        return score
