from typing import List, Tuple

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QPainter, QPen
from PyQt6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
)

from view.styles import Colors, Dimensions


class BoardView(QGraphicsView):
    square_clicked = pyqtSignal(int, int)  # (row, col)

    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.squares = []
        self.pieces = {}
        self.highlights = []

        self.thinking_moves = []

        self._setup_view()
        self._create_board()

    def _setup_view(self):
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        self.setBackgroundBrush(QBrush(Colors.BG_PRIMARY))

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        board_pixel_size = Dimensions.BOARD_SIZE * Dimensions.SQUARE_SIZE
        total_size = board_pixel_size + (Dimensions.BOARD_PADDING * 2)
        self.setFixedSize(total_size, total_size)

    def _create_board(self):
        for row in range(Dimensions.BOARD_SIZE):
            row_squares = []

            for col in range(Dimensions.BOARD_SIZE):
                if (row + col) % 2 == 0:
                    color = Colors.LIGHT_SQUARE
                else:
                    color = Colors.DARK_SQUARE

                x = col * Dimensions.SQUARE_SIZE
                y = row * Dimensions.SQUARE_SIZE

                square = QGraphicsRectItem(
                    x, y, Dimensions.SQUARE_SIZE, Dimensions.SQUARE_SIZE
                )
                square.setBrush(QBrush(color))
                square.setPen(QPen(Qt.PenStyle.NoPen))
                square.setZValue(Dimensions.Z_BOARD)

                self.scene.addItem(square)
                row_squares.append(square)

            self.squares.append(row_squares)

    def update_board(self, board: List[List[int]]):
        for piece in self.pieces.values():
            self.scene.removeItem(piece)
        self.pieces.clear()

        for row in range(Dimensions.BOARD_SIZE):
            for col in range(Dimensions.BOARD_SIZE):
                piece_type = board[row][col]
                if piece_type != 0:
                    self._create_piece(row, col, piece_type)

    def _create_piece(self, row: int, col: int, piece_type: int):
        x = col * Dimensions.SQUARE_SIZE + Dimensions.SQUARE_SIZE / 2
        y = row * Dimensions.SQUARE_SIZE + Dimensions.SQUARE_SIZE / 2

        piece = QGraphicsEllipseItem(
            x - Dimensions.PIECE_RADIUS,
            y - Dimensions.PIECE_RADIUS,
            Dimensions.PIECE_RADIUS * 2,
            Dimensions.PIECE_RADIUS * 2,
        )

        if piece_type == 1:  # White
            piece.setBrush(QBrush(Colors.WHITE_PIECE))
            piece.setPen(QPen(Colors.WHITE_PIECE_BORDER, 2))
        else:  # Black
            piece.setBrush(QBrush(Colors.BLACK_PIECE))
            piece.setPen(QPen(Colors.BLACK_PIECE_BORDER, 2))

        piece.setZValue(Dimensions.Z_PIECE)
        self.scene.addItem(piece)
        self.pieces[(row, col)] = piece

    def mousePressEvent(self, event):
        pos = self.mapToScene(event.pos())
        col = int(pos.x() // Dimensions.SQUARE_SIZE)
        row = int(pos.y() // Dimensions.SQUARE_SIZE)

        if 0 <= row < Dimensions.BOARD_SIZE and 0 <= col < Dimensions.BOARD_SIZE:
            self.square_clicked.emit(row, col)

    def highlight_square(self, row: int, col: int, color):
        x = col * Dimensions.SQUARE_SIZE
        y = row * Dimensions.SQUARE_SIZE

        highlight = QGraphicsRectItem(
            x, y, Dimensions.SQUARE_SIZE, Dimensions.SQUARE_SIZE
        )
        highlight.setBrush(QBrush(color))
        highlight.setPen(QPen(Qt.PenStyle.NoPen))
        highlight.setZValue(Dimensions.Z_HIGHLIGHT)

        self.scene.addItem(highlight)
        self.highlights.append(highlight)

    def clear_highlights(self):
        for highlight in self.highlights:
            self.scene.removeItem(highlight)
        self.highlights.clear()
        self.thinking_moves.clear()

    def show_selected(self, row: int, col: int):
        self.clear_highlights()
        self.highlight_square(row, col, Colors.SELECTED_HIGHLIGHT)

    def show_valid_moves(self, moves: List[Tuple[int, int]]):
        for row, col in moves:
            self.highlight_square(row, col, Colors.VALID_MOVE_HIGHLIGHT)

    def show_last_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]):
        self.highlight_square(from_pos[0], from_pos[1], Colors.LAST_MOVE_HIGHLIGHT)
        self.highlight_square(to_pos[0], to_pos[1], Colors.LAST_MOVE_HIGHLIGHT)

    def show_thinking(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]):
        if self.thinking_moves:
            for _ in range(min(2, len(self.highlights))):
                if self.highlights:
                    last = self.highlights[-1]
                    self.scene.removeItem(last)
                    self.highlights.pop()

        self.thinking_moves = [from_pos, to_pos]
        self.highlight_square(from_pos[0], from_pos[1], Colors.THINKING_HIGHLIGHT)
        self.highlight_square(to_pos[0], to_pos[1], Colors.THINKING_HIGHLIGHT)
