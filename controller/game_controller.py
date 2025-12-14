import random

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMessageBox

from controller.ai_controller import AIController
from model import GameRules, GameState, MoveValidator
from view import GameWindow, DifficultyDialog


class GameController:
    def __init__(self):
        self.game_state = None

        self.window = GameWindow()

        self.human_player = None
        self.ai_player = None
        self.ai_depth = 3
        self.ai_thread = None
        self.selected_piece = None
        self.game_started = False

        self._connect_signals()

        self._start_new_game()

    def _connect_signals(self):
        self.window.board_view.square_clicked.connect(self._on_square_clicked)

        self.window.new_game_requested.connect(self._start_new_game)

    def show(self):
        self.window.show()

    def _start_new_game(self):
        # Show difficulty selection dialog
        dialog = DifficultyDialog(self.window)
        if dialog.exec():
            self.ai_depth = dialog.get_selected_depth()
            self._update_difficulty_display()
        else:
            # If dialog was cancelled, don't start a new game
            if not self.game_started:
                # If this is the first game and user cancelled, close the application
                self.window.close()
            return
        
        self.selected_piece = None
        self.game_started = True

        if random.choice([True, False]):
            self.human_player = GameState.WHITE
            self.ai_player = GameState.BLACK
            self.window.set_info_text("You are White. Your turn!")
            self.window.metrics_panel.set_status("Your Turn", "#90EE90")
        else:
            self.human_player = GameState.BLACK
            self.ai_player = GameState.WHITE
            self.window.set_info_text("You are Black. AI goes first...")
            self.window.metrics_panel.set_status("AI Thinking...", "#FFB347")
        
        self.game_state = GameState()
        GameRules.setup_initial_position(self.game_state, self.human_player)
        self.game_state.human_player = self.human_player
        
        if self.human_player == GameState.BLACK:
            QTimer.singleShot(500, self._trigger_ai_move)

        self.window.board_view.update_board(self.game_state.board)
        self.window.board_view.clear_highlights()
        self.window.metrics_panel.reset_metrics()

    def _on_square_clicked(self, row: int, col: int):
        if not self.game_started or GameRules.is_game_over(self.game_state):
            return

        if self.game_state.current_player != self.human_player:
            return

        clicked_piece = self.game_state.get_piece(row, col)

        if clicked_piece == self.human_player:
            self._select_piece(row, col)

        elif self.selected_piece:
            self._attempt_player_move(row, col)

    def _select_piece(self, row: int, col: int):
        self.selected_piece = (row, col)
        valid_moves = MoveValidator.get_valid_moves(self.game_state, row, col)

        self.window.board_view.clear_highlights()
        self.window.board_view.show_selected(row, col)
        self.window.board_view.show_valid_moves(valid_moves)

    def _attempt_player_move(self, row: int, col: int):
        from_pos = self.selected_piece
        to_pos = (row, col)

        if GameRules.execute_move(self.game_state, from_pos, to_pos, self.human_player):
            self.window.board_view.update_board(self.game_state.board)
            self.window.board_view.clear_highlights()
            self.window.board_view.show_last_move(from_pos, to_pos)

            self.selected_piece = None

            if GameRules.is_game_over(self.game_state):
                self._handle_game_over()
            else:
                self.window.set_info_text("AI is thinking...")
                self.window.metrics_panel.set_status("AI Thinking...", "#FFB347")
                QTimer.singleShot(300, self._trigger_ai_move)
        else:
            self.selected_piece = None
            self.window.board_view.clear_highlights()

    def _trigger_ai_move(self):
        if GameRules.is_game_over(self.game_state):
            return

        self.ai_thread = AIController(
            self.game_state, self.ai_player, self.ai_depth, self.human_player
        )

        self.ai_thread.thinking_update.connect(self._on_ai_thinking)
        self.ai_thread.metrics_update.connect(self._on_ai_metrics)
        self.ai_thread.move_decided.connect(self._on_ai_move)

        self.ai_thread.start()

    def _on_ai_thinking(self, from_pos: tuple, to_pos: tuple):
        if random.random() < 0.5:  # Show ~50% of evaluations
            self.window.board_view.show_thinking(from_pos, to_pos)

    def _on_ai_metrics(self, metrics: dict):
        self.window.metrics_panel.update_metrics(metrics)

    def _on_ai_move(self, from_pos: tuple, to_pos: tuple):
        if GameRules.execute_move(self.game_state, from_pos, to_pos, self.human_player):
            self.window.board_view.update_board(self.game_state.board)
            self.window.board_view.clear_highlights()
            self.window.board_view.show_last_move(from_pos, to_pos)

            if GameRules.is_game_over(self.game_state):
                self._handle_game_over()
            else:
                self.window.set_info_text("Your turn!")
                self.window.metrics_panel.set_status("Your Turn", "#90EE90")

    def _handle_game_over(self):
        winner = self.game_state.get_winner()

        if winner == self.human_player:
            message = "Congratulations! You won!"
            self.window.set_info_text("You won!")
            self.window.metrics_panel.set_status("You Won!", "#FFD700")
        else:
            message = "AI wins! Better luck next time."
            self.window.set_info_text("AI won!")
            self.window.metrics_panel.set_status("AI Won", "#FF6B6B")

        QTimer.singleShot(500, lambda: self._show_game_over_dialog(message))

    def _show_game_over_dialog(self, message: str):
        msg_box = QMessageBox(self.window)
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def _update_difficulty_display(self):
        """Update the difficulty display based on current AI depth"""
        if self.ai_depth == 1:
            difficulty_name = "Easy"
            difficulty_color = "#90EE90"
        elif self.ai_depth == 3:
            difficulty_name = "Medium"
            difficulty_color = "#FFB347"
        elif self.ai_depth == 5:
            difficulty_name = "Hard"
            difficulty_color = "#FF6B6B"
        else:
            difficulty_name = f"Custom"
            difficulty_color = "#D0D0D0"
        
        self.window.depth_label.setText(difficulty_name)
        self.window.depth_label.setStyleSheet(
            f"color: {difficulty_color}; font-size: 24px; font-weight: bold; padding: 10px;"
        )
        self.window.depth_info.setText(f"Search Depth: {self.ai_depth}")
