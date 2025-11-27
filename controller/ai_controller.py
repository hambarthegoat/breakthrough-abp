import math
import time

from PyQt6.QtCore import QThread, pyqtSignal

from controller.ai_algorithm import MinimaxAlgorithm
from model import GameState


class AIController(QThread):
    move_decided = pyqtSignal(tuple, tuple)  # (from_pos, to_pos)
    thinking_update = pyqtSignal(tuple, tuple)
    metrics_update = pyqtSignal(dict)

    def __init__(
        self, state: GameState, player: int, depth: int = 3, human_player: int = None
    ):
        super().__init__()

        self.state = state.copy()
        self.player = player
        self.depth = depth
        self.human_player = human_player

        self.algorithm = MinimaxAlgorithm(human_player)
        self.start_time = 0
        self.branching_factor = 0

    def run(self):
        self.start_time = time.time()

        best_score, best_move = self.algorithm.find_best_move(
            self.state,
            self.player,
            self.depth,
            evaluation_callback=None,
            move_evaluation_callback=self._on_move_evaluation,
        )

        execution_time = time.time() - self.start_time
        nodes_visited = self.algorithm.get_nodes_visited()

        if self.depth > 0 and nodes_visited > 1:
            self.branching_factor = math.pow(nodes_visited, 1.0 / self.depth)

        self._emit_metrics(
            depth=self.depth,
            nodes_visited=nodes_visited,
            execution_time=execution_time,
            branching_factor=self.branching_factor,
            evaluation=best_score,
        )

        if best_move:
            self.move_decided.emit(best_move[0], best_move[1])

    def _on_move_evaluation(self, from_pos: tuple, to_pos: tuple):
        self.thinking_update.emit(from_pos, to_pos)

    def _emit_metrics(self, **metrics):
        self.metrics_update.emit(metrics)

    def set_depth(self, depth: int):
        self.depth = max(1, min(depth, 6))
