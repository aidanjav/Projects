import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

# ---------- TYPING GAME ----------
# Aidan Javier
# User will select difficulty. Once on the "Ready?" screen, begin the game by pressing the Enter/Return key.
# Doing so will immediately begin the game where the user will type the provided string
# DO NOT CLICK ENTER AFTER TYPING. If the typed line is correct the game will automatically end and display the score
# ---------------------------------

# Global variables declared for user difficulty selection, score each round, and the current prompt
difficulty = ""
score = 0
currPrompt = ""

# Dictionary pairing each difficulty with a list of possible prompts
# Prompts can be added here for each of the three categories
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

# First Window: Difficulty selection
# Choosing a difficulty in the first window will hide the first window and jump to the second
class FirstWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the properties of the first window
        self.setWindowTitle('Title')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: lightblue;")

        # Window title
        label = QLabel('See How Fast You Can Type', self)
        label.setFont(QFont('Arial', 24))
        label.setAlignment(Qt.AlignCenter)

        # Three buttons, one for each difficulty
        # Selecting a difficulty will bring you directly to the game screen
        buttons = QHBoxLayout()
        easy = QPushButton('Easy', self)
        medium = QPushButton('Medium', self)
        hard = QPushButton('Hard', self)
        easy.setStyleSheet("background-color: white")
        medium.setStyleSheet("background-color: white")
        hard.setStyleSheet("background-color: white")

        # Set commands for each button
        # Clicking a button will execute the respective function, creating the game screen object
        easy.clicked.connect(self.easy_game)
        medium.clicked.connect(self.med_game)
        hard.clicked.connect(self.hard_game)

        # Add buttons to HBox layout
        buttons.addWidget(easy)
        buttons.addWidget(medium)
        buttons.addWidget(hard)

        # Add title and buttons to the title screen
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addLayout(buttons)
        vbox.setAlignment(Qt.AlignCenter)
        self.setLayout(vbox)

    # Function to create the second window object for an easy game
    def easy_game(self):
        global difficulty
        difficulty = "easy"
        self.easy_game = SecondWindow(self)
        self.easy_game.show()
        self.hide()

    # Function to create the second window object for a medium game
    def med_game(self):
        global difficulty
        difficulty = "med"
        self.med_game = SecondWindow(self)
        self.med_game.show()
        self.hide()

    # Function to create the second window object for a hard game
    def hard_game(self):
        global difficulty
        difficulty = "hard"
        self.hard_game = SecondWindow(self)
        self.hard_game.show()
        self.hide()

# Second Window: Game window
# Game window object will initially display a "Ready" prompt
# Once the Enter/Return key is pressed, the game will immediately begin
class SecondWindow(QWidget):
    def __init__(self, first_window):
        super().__init__()

        # Set the properties of the second window
        self.setWindowTitle("Game")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: yellow;")

        # Create text for the second window
        self.label = QLabel('Ready?', self)
        self.label.setFont(QFont('Arial', 24))
        self.label.setAlignment(Qt.AlignCenter)

        self.begin = QLabel('Press Enter to Begin', self)
        self.begin.setFont(QFont('Arial', 12))
        self.begin.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.begin)
        self.setLayout(self.layout)

        # Important so that we can return back to the first window to begin another game
        self.first_window = first_window

    # Wait for the Enter/Return key to be pressed. Once pressed, begin the game
    def keyPressEvent(self, event):
        key = event.key()
        global currPrompt
        if key == Qt.Key_Return:

            # Enter/Return has been pressed, begin setting up the window for the user to begin typing
            self.setStyleSheet("background-color: green;")
            self.layout.removeWidget(self.label)
            self.layout.removeWidget(self.begin)
            self.label.deleteLater()

            # Select random prompt from chosen difficulty
            currPrompt = random.choice(prompts[difficulty])

            # Display prompt
            self.label = QLabel(currPrompt, self)
            self.label.setFont(QFont('Arial', 16))
            self.label.setAlignment(Qt.AlignCenter)

            # Create text box for the user to begin typing
            self.text = QLineEdit(self)

            # Add prompt and text box widgets to the window
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.text)
            self.text.setFocus()

            # Create score widget to be displayed as the user types
            self.scoreLabel = QLabel(str(score), self)
            self.scoreLabel.setFont(QFont('Arial', 16))
            self.layout.addWidget(self.scoreLabel)

            # Create a timer object
            # This is necessary so the two functions can be run while the user is typing
            # One will check to see if the user text matches the prompt
            # The other will constantly update the score
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.compareText)
            self.timer.timeout.connect(self.updateScore)
            self.timer.start(10)

    # Function to update the score
    # Score increments every 0.01 of a second
    def updateScore(self):
        global score
        score = round(score + 0.01, 2)
        self.scoreLabel.setText(str(score))

    # Function will immediately execute once the strings match
    def compareText(self):
        userText = self.text.text()
        global currPrompt
        if userText == currPrompt:

            # User string matches the prompt, display score
            # Begin by resetting the current prompt and stopping the timer
            self.timer.stop()
            currPrompt = ""

            # Remove current screen widgets and change window color
            self.setStyleSheet("background-color: red;")
            self.layout.removeWidget(self.label)
            self.layout.removeWidget(self.text)
            self.layout.removeWidget(self.scoreLabel)

            # Display the 'well done' text and the user's score, which was determined when the timer stopped
            self.label = QLabel("Well done!", self)
            self.scoreLabelFull = QLabel(f"Score: {score} seconds", self)
            self.label.setAlignment(Qt.AlignCenter)
            self.scoreLabelFull.setAlignment(Qt.AlignCenter)
            self.label.setFont(QFont('Arial', 24))
            self.scoreLabelFull.setFont(QFont('Arial', 24))

            # Create button to return to the original title window after completing the game
            self.homePage = QPushButton('Return', self)
            self.homePage.clicked.connect(self.close_window)

            self.layout.addWidget(self.label)
            self.layout.addWidget(self.scoreLabelFull)
            self.layout.addWidget(self.homePage)

    # Function to reset the score and return to the first window to play another game
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
