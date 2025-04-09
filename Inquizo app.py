import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont
import random

class TitlePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()

        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)
        title_layout.setSpacing(0)

        logo = QLabel()
        pixmap = QPixmap("Inquizo-logo.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)

        title = QLabel("Inquizo")
        title.setFont(QFont("Segoe UI", 40, QFont.Bold))
        title.setStyleSheet("color: white; font-size: 40px; font-weight: bold;")

        title_layout.addWidget(logo)
        title_layout.addWidget(title)

        play_button = QPushButton("Play")
        play_button.clicked.connect(self.goto_game_mode_selection)

        layout.addLayout(title_layout)
        layout.addWidget(play_button)
        self.setLayout(layout)

    def goto_game_mode_selection(self):
        self.stacked_widget.setCurrentIndex(1)

class GameModePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()

        label = QLabel("Choose Your Game Mode")
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")

        classic_btn = QPushButton("Classic Mode")
        timerush_btn = QPushButton("Time Rush Mode")
        back_btn = QPushButton("Back to Title")

        classic_btn.clicked.connect(self.goto_classic)
        timerush_btn.clicked.connect(self.goto_timerush_info)
        back_btn.clicked.connect(self.go_back_to_title)

        layout.addWidget(label)
        layout.addSpacing(20)
        layout.addWidget(classic_btn)
        layout.addWidget(timerush_btn)
        layout.addSpacing(10)
        layout.addWidget(back_btn)
        self.setLayout(layout)

    def goto_classic(self):
        self.stacked_widget.setCurrentIndex(2)

    def goto_timerush_info(self):
        self.stacked_widget.setCurrentIndex(3)

    def go_back_to_title(self):
        self.stacked_widget.setCurrentIndex(0)
class ThemeSelectionPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()

        label = QLabel("Select a Theme:")
        label.setAlignment(Qt.AlignCenter)

        music_btn = QPushButton("Music")
        bodybuilding_btn = QPushButton("Bodybuilding")
        general_btn = QPushButton("General Knowledge")
        back_btn = QPushButton("Back to Game Mode")

        music_btn.clicked.connect(lambda: self.select_theme("music"))
        bodybuilding_btn.clicked.connect(lambda: self.select_theme("bodybuilding"))
        general_btn.clicked.connect(lambda: self.select_theme("general"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        layout.addWidget(label)
        layout.addWidget(music_btn)
        layout.addWidget(bodybuilding_btn)
        layout.addWidget(general_btn)
        layout.addSpacing(10)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def select_theme(self, theme):
        self.stacked_widget.difficulty_page.set_theme(theme)
        self.stacked_widget.setCurrentIndex(4)  
class DifficultySelectionPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.theme = None

        layout = QVBoxLayout()

        label = QLabel("Select Difficulty:")
        label.setAlignment(Qt.AlignCenter)

        easy_btn = QPushButton("Easy")
        medium_btn = QPushButton("Medium")
        hard_btn = QPushButton("Hard")
        impossible_btn = QPushButton("Impossible")
        back_btn = QPushButton("Back to Theme Selection")

        easy_btn.clicked.connect(lambda: self.start_quiz("easy"))
        medium_btn.clicked.connect(lambda: self.start_quiz("medium"))
        hard_btn.clicked.connect(lambda: self.start_quiz("hard"))
        impossible_btn.clicked.connect(lambda: self.start_quiz("impossible"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        layout.addWidget(label)
        layout.addWidget(easy_btn)
        layout.addWidget(medium_btn)
        layout.addWidget(hard_btn)
        layout.addWidget(impossible_btn)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def set_theme(self, theme):
        self.theme = theme

    def start_quiz(self, difficulty):
        self.stacked_widget.quiz_page.load_questions(self.theme, difficulty)
        self.stacked_widget.setCurrentIndex(5)  # Go to QuizPage
class QuizPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.progress_label = QLabel()
        self.layout.addWidget(self.progress_label)

        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.layout.addWidget(self.question_label)

        self.feedback_label = QLabel("")
        self.feedback_label.setStyleSheet("font-size: 16px; color: yellow;")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.feedback_label)

        self.choice_buttons = []
        self.current_question_index = 0
        self.score = 0
        self.questions = []
        self.theme = None
        self.difficulty = None

        for _ in range(4):
            btn = QPushButton()
            btn.setCheckable(True)
            btn.clicked.connect(self.on_choice_clicked)
            self.choice_buttons.append(btn)
            self.layout.addWidget(btn)

    def load_questions(self, theme, difficulty):
        self.current_question_index = 0
        self.score = 0
        self.theme = theme
        self.difficulty = difficulty

        with open("Inquizo-questions.json", "r") as f:
            data = json.load(f)
            self.questions = data[theme][difficulty]

        self.show_question()

    def show_question(self):
        if self.current_question_index < len(self.questions):
            total_questions = len(self.questions)
            self.progress_label.setText(f"Question {self.current_question_index + 1} of {total_questions}")
            question_data = self.questions[self.current_question_index]
            self.question_label.setText(question_data["question"])

            choices = question_data["choices"][:]
            random.shuffle(choices)
            for i, choice in enumerate(choices):
                self.choice_buttons[i].setText(choice)
                self.choice_buttons[i].setChecked(False)
        else:
            self.stacked_widget.final_page.set_score(self.score, len(self.questions))
            self.stacked_widget.setCurrentIndex(6)

    def on_choice_clicked(self):
        clicked = self.sender()
        for btn in self.choice_buttons:
            if btn != clicked:
                btn.setChecked(False)

        selected = clicked.text()
        correct = self.questions[self.current_question_index]["answer"]

        if selected == correct:
            self.score += 1
            self.feedback_label.setText("✅ Correct!")
        else:
            self.feedback_label.setText(f"❌ Correct answer: {correct}")

        QTimer.singleShot(1000, self.next_question)

    def next_question(self):
        self.feedback_label.setText("")
        self.current_question_index += 1
        self.show_question()

class TimeRushInfoPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()

        description = QLabel("Time Rush Mode: You have 40 seconds to answer as many random questions as possible.")
        description.setWordWrap(True)
        layout.addWidget(description)

        start_button = QPushButton("Start Time Rush")
        start_button.clicked.connect(self.start_time_rush)
        layout.addWidget(start_button)

        self.setLayout(layout)

    def start_time_rush(self):
        self.stacked_widget.time_rush_page.start_quiz()
        self.stacked_widget.setCurrentIndex(7)

class TimeRushPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.timer_label = QLabel("Time Left: 40s")
        self.timer_label.setStyleSheet("font-size: 22px; color: white;")
        self.layout.addWidget(self.timer_label)

        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-size: 18px; color: white;")
        self.layout.addWidget(self.question_label)

        self.feedback_label = QLabel("")
        self.feedback_label.setStyleSheet("font-size: 16px; color: yellow;")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.feedback_label)

        self.choice_buttons = []
        for _ in range(4):
            btn = QPushButton()
            btn.clicked.connect(self.on_choice_clicked)
            self.choice_buttons.append(btn)
            self.layout.addWidget(btn)

        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.total_answered = 0
        self.time_left = 40
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def start_quiz(self):
        self.load_random_questions()
        self.current_question_index = 0
        self.score = 0
        self.total_answered = 0
        self.time_left = 40
        self.timer.start(1000)
        self.show_question()

    def load_random_questions(self):
        with open("Inquizo-questions.json", "r") as f:
            data = json.load(f)
            all_questions = []
            for theme in data.values():
                for difficulty in theme.values():
                    all_questions.extend(difficulty)
            random.shuffle(all_questions)
            self.questions = all_questions[:50]  # limit just in case

    def show_question(self):
        if self.current_question_index < len(self.questions):
            q = self.questions[self.current_question_index]
            self.question_label.setText(q["question"])
            self.feedback_label.setText("")
            choices = q["choices"][:]
            random.shuffle(choices)
            for btn, choice in zip(self.choice_buttons, choices):
                btn.setText(choice)
                btn.setEnabled(True)
        else:
            self.end_quiz()

    def on_choice_clicked(self):
        sender = self.sender()
        selected = sender.text()
        correct = self.questions[self.current_question_index]["answer"]
        if selected == correct:
            self.score += 1
            self.feedback_label.setText("✅ Correct!")
        else:
            self.feedback_label.setText(f"❌ Correct answer: {correct}")

        self.total_answered += 1
        for btn in self.choice_buttons:
            btn.setEnabled(False)
        QTimer.singleShot(800, self.next_question)

    def next_question(self):
        self.current_question_index += 1
        self.show_question()

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Time Left: {self.time_left}s")
        if self.time_left <= 0:
            self.timer.stop()
            self.end_quiz()

    def end_quiz(self):
        self.timer.stop()
        self.stacked_widget.final_page.set_score(self.score, self.total_answered)
        self.stacked_widget.setCurrentIndex(6)

class FinalScorePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()

        self.score_label = QLabel()
        layout.addWidget(self.score_label)

        restart_btn = QPushButton("Restart Quiz")
        restart_btn.clicked.connect(self.restart_quiz)
        layout.addWidget(restart_btn)

        theme_btn = QPushButton("Change Theme")
        theme_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        layout.addWidget(theme_btn)

        difficulty_btn = QPushButton("Change Difficulty")
        difficulty_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        layout.addWidget(difficulty_btn)

        gamemode_btn = QPushButton("Change Game Mode")
        gamemode_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(gamemode_btn)

        self.setLayout(layout)

    def set_score(self, score, total):
        self.score_label.setText(f"Your Score: {score}/{total}")

    def restart_quiz(self):
        self.stacked_widget.quiz_page.load_questions(
            self.stacked_widget.quiz_page.theme,
            self.stacked_widget.quiz_page.difficulty
        )
        self.stacked_widget.setCurrentIndex(5)

class QuizApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.title_page = TitlePage(self)
        self.game_mode_page = GameModePage(self)
        self.theme_page = ThemeSelectionPage(self)
        self.time_rush_info_page = TimeRushInfoPage(self)
        self.difficulty_page = DifficultySelectionPage(self)
        self.quiz_page = QuizPage(self)
        self.final_page = FinalScorePage(self)
        self.time_rush_page = TimeRushPage(self)

        self.addWidget(self.title_page)       # 0
        self.addWidget(self.game_mode_page)   # 1
        self.addWidget(self.theme_page)       # 2
        self.addWidget(self.time_rush_info_page)  # 3
        self.addWidget(self.difficulty_page)  # 4
        self.addWidget(self.quiz_page)        # 5
        self.addWidget(self.final_page)       # 6
        self.addWidget(self.time_rush_page)   # 7

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
    QWidget {
        background-color: #0e1229;
        color: white;
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
    }
    QLabel {
        font-size: 20px;
        font-weight: bold;
        padding: 10px;
        qproperty-alignment: AlignCenter;
    }
    QPushButton {
        background-color: transparent;
        color: white;
        border: 2px solid #3b82f6;
        border-radius: 12px;
        padding: 12px;
        margin: 8px;
        font-size: 16px;
    }
    QPushButton:hover {
        background-color: #1e293b;
        border: 2px solid #60a5fa;
    }
    QPushButton:pressed {
        background-color: #2563eb;
        border: 2px solid #3b82f6;
    }
    """)
    main_app = QuizApp()
    main_app.setWindowTitle("Inquizo")
    main_app.resize(800, 600)
    main_app.show()
    sys.exit(app.exec_())
