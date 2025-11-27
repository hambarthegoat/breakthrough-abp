import sys

from PyQt6.QtWidgets import QApplication

from controller import GameController


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Breakthrough")
    app.setOrganizationName("AI Games")

    controller = GameController()
    controller.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
