import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


# List of possible writing prompts you can get for each dificulty

difficulty = ""
score = 0
currPrompt = ""

prompts = {"easy": [
    "The cat sleeps on the mat",
    "I have a red ball",
    "She likes to read books",
    "The dog runs fast",
    "It is sunny today"], 
    "med": [
    "The little girl smiled at the puppy in the park",
    "He quickly finished his homework before dinner",
    "The teacher asked the students to write a short story",
    "They played soccer in the big, green field",
    "The weather was warm and perfect for a walk in the woods"], 
    "hard": [
    "Despite the heavy rain, the children continued to play outside until sunset",
    "The scientist carefully analyzed the data to draw meaningful conclusions",
    "The ancient ruins stood tall, silently telling stories of the past civilization",
    "She struggled to comprehend the complex instructions for assembling the furniture",
    "The orchestra played a symphony that captivated the audience with its beauty and complexity"]
}

class FirstWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle('Title')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: lightblue;")

        # Label the window
        label = QLabel('See How Fast You Can Type', self)
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
        global difficulty
        difficulty = "easy"
        self.easy_game = SecondWindow(self)
        self.easy_game.show()
        self.hide()

    def med_game(self):
        global difficulty
        difficulty = "med"
        self.med_game = SecondWindow(self)
        self.med_game.show()
        self.hide()

    def hard_game(self):
        global difficulty
        difficulty = "hard"
        self.hard_game = SecondWindow(self)
        self.hard_game.show()
        self.hide()

class SecondWindow(QWidget):
    def __init__(self, first_window):
        super().__init__()

        self.setWindowTitle("Game")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: yellow;")

        self.label = QLabel('Ready?', self)
        self.label.setFont(QFont('Arial', 24))
        self.label.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.first_window = first_window

    def keyPressEvent(self, event):
        key = event.key()
        global currPrompt
        if key == Qt.Key_Return:
            self.setStyleSheet("background-color: green;")
            self.layout.removeWidget(self.label)
            self.label.deleteLater()

            currPrompt = random.choice(prompts[difficulty])

            self.label = QLabel(currPrompt, self)
            self.label.setFont(QFont('Arial', 16))
            self.label.setAlignment(Qt.AlignCenter)

            self.text = QLineEdit(self)

            self.layout.addWidget(self.label)
            self.layout.addWidget(self.text)
            self.text.setFocus()

            self.scoreLabel = QLabel(str(score), self)
            self.scoreLabel.setFont(QFont('Arial', 16))
            self.layout.addWidget(self.scoreLabel)

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.compareText)
            self.timer.timeout.connect(self.updateScore)
            self.timer.start(10)

    def updateScore(self):
        global score
        score = round(score + 0.01, 2)
        self.scoreLabel.setText(str(score))

    def compareText(self):
        userText = self.text.text()
        global currPrompt
        if userText == currPrompt:
            self.timer.stop()
            currPrompt = ""
            self.setStyleSheet("background-color: red;")
            self.layout.removeWidget(self.label)
            self.layout.removeWidget(self.text)
            self.layout.removeWidget(self.scoreLabel)

            self.label = QLabel("Well done!", self)
            self.scoreLabel = QLabel("Score: " + str(score), self)
            self.label.setAlignment(Qt.AlignCenter)
            self.scoreLabel.setAlignment(Qt.AlignCenter)
            self.label.setFont(QFont('Arial', 24))
            self.scoreLabel.setFont(QFont('Arial', 24))

            self.homePage = QPushButton('Return', self)
            self.homePage.clicked.connect(self.close_window)

            self.layout.addWidget(self.label)
            self.layout.addWidget(self.scoreLabel)
            self.layout.addWidget(self.homePage)

    def close_window(self):
        global score
        score = 0
        self.close()
        self.first_window.show()


def main():
    # Show the window
    app = QApplication(sys.argv)

    first_window = FirstWindow()
    first_window.show()

    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()
