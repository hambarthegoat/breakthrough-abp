from typing import Callable, Optional, Tuple

from model import GameRules, GameState, MoveValidator, PositionEvaluator


class MinimaxAlgorithm:
    def __init__(self, human_player: int = None):
        self.nodes_visited = 0
        self.evaluation_callback = None
        self.move_evaluation_callback = None
        self.human_player = human_player

    def find_best_move(
        self,
        state: GameState,
        player: int,
        depth: int,
        evaluation_callback: Optional[Callable] = None,
        move_evaluation_callback: Optional[Callable] = None,
    ) -> Tuple[float, Optional[Tuple[Tuple[int, int], Tuple[int, int]]]]:
        self.nodes_visited = 0
        self.evaluation_callback = evaluation_callback
        self.move_evaluation_callback = move_evaluation_callback

        return self._minimax(state, depth, float("-inf"), float("inf"), True, player)

    def _minimax(
        self,
        state: GameState,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
        original_player: int,
    ) -> Tuple[float, Optional[Tuple[Tuple[int, int], Tuple[int, int]]]]:
        self.nodes_visited += 1

        if depth == 0 or GameRules.is_game_over(state):
            evaluation = PositionEvaluator.evaluate(
                state, original_player, self.human_player
            )
            if self.evaluation_callback:
                self.evaluation_callback(evaluation)
            return evaluation, None

        current_player = state.current_player
        valid_moves = MoveValidator.get_all_valid_moves(state, current_player)

        if not valid_moves:
            evaluation = PositionEvaluator.evaluate(
                state, original_player, self.human_player
            )
            return evaluation, None

        best_move = None

        if maximizing:
            max_eval = float("-inf")

            for move in valid_moves:
                if self.move_evaluation_callback:
                    self.move_evaluation_callback(move[0], move[1])

                next_state = state.copy()
                GameRules.execute_move(next_state, move[0], move[1], self.human_player)

                eval_score, _ = self._minimax(
                    next_state, depth - 1, alpha, beta, False, original_player
                )

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

                # Update alpha
                alpha = max(alpha, eval_score)

                # Beta cutoff
                if beta <= alpha:
                    break

            return max_eval, best_move

        else:
            min_eval = float("inf")

            for move in valid_moves:
                if self.move_evaluation_callback:
                    self.move_evaluation_callback(move[0], move[1])

                next_state = state.copy()
                GameRules.execute_move(next_state, move[0], move[1], self.human_player)

                eval_score, _ = self._minimax(
                    next_state, depth - 1, alpha, beta, True, original_player
                )

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move

                # Update beta
                beta = min(beta, eval_score)

                # Alpha cutoff
                if beta <= alpha:
                    break

            return min_eval, best_move

    def get_nodes_visited(self) -> int:
        return self.nodes_visited
