from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from view.board_view import BoardView
from view.metrics_panel import MetricsPanel
from view.styles import Dimensions, StyleSheets


class GameWindow(QMainWindow):
    new_game_requested = pyqtSignal()
    depth_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.board_view = None
        self.metrics_panel = None
        self.info_label = None
        self.new_game_btn = None
        self.depth_slider = None

        self._setup_window()
        self._create_ui()

    def _setup_window(self):
        self.setWindowTitle("Breakthrough - AI Game")
        self.setFixedSize(Dimensions.WINDOW_WIDTH, Dimensions.WINDOW_HEIGHT)
        self.setStyleSheet(StyleSheets.MAIN_WINDOW)

    def _create_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(Dimensions.SECTION_SPACING)

        left_panel = self._create_left_panel()
        main_layout.addLayout(left_panel)

        right_panel = self._create_right_panel()
        main_layout.addLayout(right_panel)

        central.setLayout(main_layout)

    def _create_left_panel(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(Dimensions.LAYOUT_SPACING)

        self.info_label = QLabel("Welcome to Breakthrough!")
        self.info_label.setStyleSheet(StyleSheets.LABEL_PRIMARY)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setMinimumHeight(Dimensions.LABEL_HEIGHT)
        layout.addWidget(self.info_label)

        self.board_view = BoardView()
        layout.addWidget(self.board_view)

        controls = self._create_controls()
        layout.addLayout(controls)

        return layout

    def _create_controls(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self.new_game_btn = QPushButton("New Game")
        self.new_game_btn.setStyleSheet(StyleSheets.BUTTON_PRIMARY)
        self.new_game_btn.setMinimumHeight(Dimensions.BUTTON_HEIGHT)
        self.new_game_btn.clicked.connect(self.new_game_requested.emit)

        layout.addWidget(self.new_game_btn)

        return layout

    def _create_right_panel(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(Dimensions.SECTION_SPACING)

        self.metrics_panel = MetricsPanel()
        layout.addWidget(self.metrics_panel)

        settings = self._create_settings_panel()
        layout.addWidget(settings)

        layout.addStretch()

        return layout

    def _create_settings_panel(self) -> QGroupBox:
        settings_group = QGroupBox("AI Settings")
        settings_group.setStyleSheet(StyleSheets.GROUP_BOX)

        settings_layout = QVBoxLayout()
        settings_layout.setSpacing(10)
        settings_layout.setContentsMargins(15, 20, 15, 20)

        # Difficulty level label
        difficulty_label = QLabel("Difficulty:")
        difficulty_label.setStyleSheet("color: #A0A0A0; font-size: 14px;")
        settings_layout.addWidget(difficulty_label)

        # Main difficulty display
        self.depth_label = QLabel("Medium")
        self.depth_label.setStyleSheet(
            "color: #FFB347; font-size: 24px; font-weight: bold; padding: 10px;"
        )
        self.depth_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_layout.addWidget(self.depth_label)

        # Search depth info
        self.depth_info = QLabel("Search Depth: 3")
        self.depth_info.setStyleSheet("color: #808080; font-size: 13px; padding: 5px;")
        self.depth_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_layout.addWidget(self.depth_info)

        settings_group.setLayout(settings_layout)

        return settings_group

    def set_info_text(self, text: str):
        self.info_label.setText(text)

    def get_board_view(self) -> BoardView:
        return self.board_view

    def get_metrics_panel(self) -> MetricsPanel:
        return self.metrics_panel
