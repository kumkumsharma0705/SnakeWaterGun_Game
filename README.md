# 🐍💧🔫 Snake Water Gun — Python Game

A fun, feature-rich terminal-based twist on the classic Rock Paper Scissors game — built in pure Python with no external libraries required.

---

## 📋 Table of Contents

- [About the Game](#about-the-game)
- [Game Rules](#game-rules)
- [Features](#features)
- [Requirements](#requirements)
- [How to Run](#how-to-run)
- [How to Play](#how-to-play)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## 🎮 About the Game

Snake Water Gun is a 2-player game where **you** play against the **computer**. The computer picks randomly, and you have **5 seconds** to make your choice — or the opponent wins the round automatically!

---

## 📜 Game Rules

| Player A  | Player B  | Winner   |
|-----------|-----------|----------|
| 🐍 Snake  | 💧 Water  | Snake    |
| 💧 Water  | 🔫 Gun    | Water    |
| 🔫 Gun    | 🐍 Snake  | Gun      |
| Any       | Same      | Draw 🤝  |

> **Logic:** Snake drinks Water ▸ Water douses Gun ▸ Gun shoots Snake

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎨 **Emoji display** | Each option shown with its emoji (🐍 💧 🔫) in the menu and results |
| 📊 **Live statistics** | Tracks total Wins, Losses, Draws + a win-rate progress bar |
| 🔊 **Sound effects** | Different sounds for Win, Lose, Draw, Timeout, and countdown ticks |
| ✅ **Input validation** | Invalid input shows a warning and doesn't count as a round |
| ⏱️ **5-second timer** | Live countdown displayed; timeout = opponent wins the round |
| 🚪 **Quit anytime** | Type `q` to exit and see your final stats |
| 🎨 **Colored output** | Green for wins, red for losses, yellow for draws |

---

## 🛠️ Requirements

- **Python 3.6+** (recommended: Python 3.10 or above)
- No external packages needed — uses only the Python standard library

Check your Python version:
```bash
python --version
```

---

## ▶️ How to Run

### Step 1 — Download the file

Save `snakeWaterGun.py` to a folder on your computer.

### Step 2 — Open a terminal

- **Windows:** Press `Win + R`, type `cmd`, press Enter
- **Mac/Linux:** Open Terminal

### Step 3 — Navigate to the folder

```bash
# Example — replace with your actual path
cd C:\Users\Admin\Desktop\Python\myPyProjects
```

### Step 4 — Run the game

```bash
python snakeWaterGun.py
```

> **VS Code users:** Open the integrated terminal (`Ctrl + \``) and run the command above directly. Avoid using the ▶ Run button if you encounter Python extension errors.

---

## 🕹️ How to Play

```
🐍  SNAKE  •  WATER  •  GUN  🔫

Choose your weapon:
  [1]  🐍  Snake
  [2]  💧  Water
  [3]  🔫  Gun
  [q]  🚪  Quit

Your choice (1/2/3) →  ⏱  4s
```

1. Press **1**, **2**, or **3** and hit Enter within 5 seconds
2. The computer picks a random option
3. The result is shown with colored text and a sound effect
4. Stats update after every valid round
5. Press **q** anytime to quit and see your final score

---

## 🗂️ Project Structure

```
myPyProjects/
└── snakeWaterGun.py    ← Main game file (single file, no dependencies)
```

---

## 🔊 Sound Support

| Platform | Method Used |
|---|---|
| Windows | `winsound.Beep()` — built into Python |
| Linux | `beep` command (install via `sudo apt install beep`) |
| macOS / fallback | Terminal bell character (`\a`) |

Sounds will still work as terminal bells even if no audio driver is configured.

---

## 🐛 Troubleshooting

### ❌ "No such file or directory"
Your terminal is in the wrong folder. Use `cd` to navigate to where `snakeWaterGun.py` is saved:
```bash
cd C:\Users\Admin\Desktop\Python\myPyProjects
python snakeWaterGun.py
```

### ❌ "python is not recognized"
Try using `python3` instead:
```bash
python3 snakeWaterGun.py
```

### ❌ VS Code: "Command 'python.setInterpreter' not found"
- Go to Extensions → find **Python** → click **Uninstall**, then **Reinstall**
- Press `Ctrl+Shift+P` → type `Reload Window` → press Enter
- Then press `Ctrl+Shift+P` → `Python: Select Interpreter` → choose Python 3.x

### ❌ Timer not working properly
The timer uses Python threads. Make sure you're running the file directly in a real terminal (cmd, PowerShell, or bash) — not inside an IDE's limited console.

---

## 👤 Author

Made with ❤️ in Python — no libraries, just vibes.

---

## 📄 License

Free to use and modify for personal or educational purposes.
