from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QButtonGroup,
    QRadioButton,
)

from view.styles import StyleSheets, Dimensions


class DifficultyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.selected_depth = 3  # Default to medium
        
        self._setup_dialog()
        self._create_ui()
    
    def _setup_dialog(self):
        self.setWindowTitle("Select AI Difficulty")
        self.setModal(True)
        self.setFixedSize(400, 300)
        self.setStyleSheet(StyleSheets.MAIN_WINDOW)
    
    def _create_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Choose AI Difficulty")
        title.setStyleSheet(
            "color: #FFFFFF; font-size: 20px; font-weight: bold; padding: 10px; line-height: 1.5;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFixedHeight(60)
        layout.addWidget(title)
        
        # Radio buttons for difficulty
        self.button_group = QButtonGroup()
        
        # Easy
        easy_btn = QRadioButton("Easy (Search Depth: 1)")
        easy_btn.setStyleSheet(
            "color: #90EE90; font-size: 14px; padding: 8px;"
        )
        easy_btn.setProperty("depth", 1)
        self.button_group.addButton(easy_btn)
        layout.addWidget(easy_btn)
        
        # Medium
        medium_btn = QRadioButton("Medium (Search Depth: 3)")
        medium_btn.setStyleSheet(
            "color: #FFB347; font-size: 14px; padding: 8px;"
        )
        medium_btn.setProperty("depth", 3)
        medium_btn.setChecked(True)  # Default selection
        self.button_group.addButton(medium_btn)
        layout.addWidget(medium_btn)
        
        # Hard
        hard_btn = QRadioButton("Hard (Search Depth: 5)")
        hard_btn.setStyleSheet(
            "color: #FF6B6B; font-size: 14px; padding: 8px;"
        )
        hard_btn.setProperty("depth", 5)
        self.button_group.addButton(hard_btn)
        layout.addWidget(hard_btn)
        
        layout.addStretch()
        
        # Start button
        start_btn = QPushButton("Start Game")
        start_btn.setStyleSheet(StyleSheets.BUTTON_PRIMARY)
        start_btn.setMinimumHeight(Dimensions.BUTTON_HEIGHT)
        start_btn.clicked.connect(self._on_start_clicked)
        layout.addWidget(start_btn)
        
        self.setLayout(layout)
    
    def _on_start_clicked(self):
        # Get the selected difficulty
        selected_button = self.button_group.checkedButton()
        if selected_button:
            self.selected_depth = selected_button.property("depth")
        self.accept()
    
    def get_selected_depth(self) -> int:
        return self.selected_depth
