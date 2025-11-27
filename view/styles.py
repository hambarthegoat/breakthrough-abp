from PyQt6.QtGui import QColor


class Colors:
    BG_PRIMARY = QColor(45, 45, 50)
    BG_SECONDARY = QColor(55, 60, 70)
    BG_TERTIARY = QColor(70, 75, 85)

    LIGHT_SQUARE = QColor(70, 75, 85)
    DARK_SQUARE = QColor(55, 60, 70)

    WHITE_PIECE = QColor(240, 230, 210)
    WHITE_PIECE_BORDER = QColor(200, 190, 170)
    BLACK_PIECE = QColor(90, 95, 110)
    BLACK_PIECE_BORDER = QColor(70, 75, 90)

    SELECTED_HIGHLIGHT = QColor(100, 200, 255, 120)
    VALID_MOVE_HIGHLIGHT = QColor(150, 255, 150, 100)
    LAST_MOVE_HIGHLIGHT = QColor(255, 200, 100, 100)
    THINKING_HIGHLIGHT = QColor(255, 150, 255, 80)

    TEXT_PRIMARY = QColor(224, 224, 224)
    TEXT_SECONDARY = QColor(176, 176, 176)
    TEXT_SUCCESS = QColor(144, 238, 144)
    TEXT_WARNING = QColor(255, 179, 71)
    TEXT_ERROR = QColor(255, 107, 107)
    TEXT_GOLD = QColor(255, 215, 0)

    BUTTON_BG = QColor(80, 80, 96)
    BUTTON_HOVER = QColor(96, 96, 112)
    BUTTON_PRESSED = QColor(64, 64, 80)

    BORDER_COLOR = QColor(80, 80, 80)
    ACCENT_COLOR = QColor(100, 149, 237)


class StyleSheets:
    MAIN_WINDOW = """
        QMainWindow {
            background-color: #2D2D32;
        }
    """

    LABEL_PRIMARY = """
        QLabel {
            color: #E0E0E0;
            font-size: 14px;
            font-weight: bold;
        }
    """

    LABEL_TITLE = """
        QLabel {
            font-size: 18px;
            font-weight: bold;
            color: #E0E0E0;
            padding: 10px;
        }
    """

    BUTTON_PRIMARY = """
        QPushButton {
            background-color: #505060;
            color: #E0E0E0;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: 13px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #606070;
        }
        QPushButton:pressed {
            background-color: #404050;
        }
    """

    GROUP_BOX = """
        QGroupBox {
            color: #B0B0B0;
            font-weight: bold;
            border: 2px solid #505050;
            border-radius: 8px;
            margin-top: 10px;
            padding: 15px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
    """

    METRIC_LABEL = """
        QLabel {
            font-size: 13px;
            color: #D0D0D0;
            padding: 5px;
            background-color: #404045;
            border-radius: 4px;
        }
    """

    STATUS_LABEL = """
        QLabel {{
            font-size: 14px;
            color: {color};
            padding: 10px;
            background-color: #3A3A3F;
            border-radius: 5px;
        }}
    """

    SLIDER = """
        QSlider::groove:horizontal {
            background: #404045;
            height: 8px;
            border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #6495ED;
            width: 18px;
            margin: -5px 0;
            border-radius: 9px;
        }
    """


class Dimensions:
    BOARD_SIZE = 8
    SQUARE_SIZE = 70
    PIECE_RADIUS = 28
    BOARD_PADDING = 2

    WINDOW_WIDTH = 1100
    WINDOW_HEIGHT = 650

    LAYOUT_SPACING = 15
    SECTION_SPACING = 20

    BUTTON_HEIGHT = 40
    LABEL_HEIGHT = 40

    Z_BOARD = 0
    Z_HIGHLIGHT = 0.5
    Z_PIECE = 1
