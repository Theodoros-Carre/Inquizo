# 🧠 Inquizo - Interactive Quiz Game

Welcome to **Inquizo**, a stylish and engaging quiz game built with PyQt5. Test your knowledge across multiple themes and difficulties, and challenge yourself with the fast-paced Time Rush mode.

---

## 🎮 Features

- **Multiple Game Modes**
  - 🎯 **Classic Mode**: Choose a theme and difficulty. Answer a fixed set of questions with instant feedback.
  - ⚡ **Time Rush Mode**: Beat the clock! You have 40 seconds to answer as many questions as you can.

- **Themes & Difficulties**
  - 3 Themes: Music, Bodybuilding, General Knowledge
  - 4 Difficulties: Easy, Medium, Hard, Impossible

- **Feedback System**
  - Instant feedback after each answer (Correct ✅ or Incorrect ❌)
  - Tracks your progress and displays your final score

- **Responsive UI**
  - Clean interface with stacked widgets
  - Smooth transitions between game states
  - Optimized for readability and clarity

---

## 🛠️ Requirements

- Python 3.x
- PyQt5

Install requirements with:

```bash
pip install pyqt5
```

---

## 🚀 Getting Started

1. **Clone the repository or download the source code**

2. **Open file in python editor of choice**  

3. **Run the app**

---

## 📂 Project Structure

```
Inquizo/
├── Brain_logo.png              # Logo for title screen
├── questions180.json           # Quiz data (can be replaced or expanded)
├── main.py                     # Application entry point
└── README.md                   # You're reading this!
```

---

## ✨ Customization

- ⏱️ Change Time Rush duration:  
  Edit `self.time_left = 40` in the `TimeRushQuizPage` class.

- 🎨 Modify button or background colors:  
  Scroll to the `app.setStyleSheet(...)` section at the bottom of the script.

- 🔤 Change text or labels:  
  All UI strings are defined within class initializations like `TitlePage`, `GameModePage`, etc.

- 📂 Change your question file:
    - Format: JSON (e.g., `questions180.json`)
    - Edit `with open("questions180.json", "r")` in the `TimeRushQuizPage` and `QuizPage` class

---

## 👥 Contributors  
**The Team** : Thedoros CARRE, Luis RAMIREZ RAMIREZ, Yousuf HOSNY

---

## 📜 License  
This project is licensed under the **ESME License** – Free to use and modify.
