import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class FirstWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle('Title')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: lightblue;")

        # Label the window
        label = QLabel('See How Fast You Can Type!', self)
        label.setFont(QFont('Arial', 24))
        label.setAlignment(Qt.AlignCenter)

        # Create buttons
        buttons = QHBoxLayout()

        easy = QPushButton('Easy', self)
        medium = QPushButton('Medium', self)
        hard = QPushButton('Hard', self)

        easy.setStyleSheet("background-color: white")
        easy.clicked.connect(self.easy_game)
        medium.setStyleSheet("background-color: white")
        medium.clicked.connect(self.med_game)
        hard.setStyleSheet("background-color: white")
        hard.clicked.connect(self.hard_game)

        buttons.addWidget(easy)
        buttons.addWidget(medium)
        buttons.addWidget(hard)

        # Set layout for title and buttons
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addLayout(buttons)
        vbox.setAlignment(Qt.AlignCenter)
        self.setLayout(vbox)

    def easy_game(self):
        self.easy_game = SecondWindow()
        self.easy_game.show()
        self.close()

    def med_game(self):
        self.med_game = SecondWindow()
        self.med_game.show()
        self.close()

    def hard_game(self):
        self.hard_game = SecondWindow()
        self.hard_game.show()
        self.close()

class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Game")
        self.setGeometry(100, 100, 600, 400)

def main():
    # Show the window
    app = QApplication(sys.argv)

    first_window = FirstWindow()
    first_window.show()

    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()

