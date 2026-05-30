# 🎮 Tic-Tac-Toe CLI (Terminal Edition)

A modern, minimal, and professional command-line interface (CLI) implementation of the classic Tic-Tac-Toe game. Written in Python with zero external dependencies, featuring rich ANSI colors, interactive board navigation, and an unbeatable AI opponent.

---

## ✨ Features

- **🎮 Interactive Control System**: Play using **Arrow Keys / WASD** and press **Enter / Space** to place your mark. No more typing manual grid coordinates!
- **🎨 Modern Visual Styling**: Sleek, high-fidelity board layout using Unicode box-drawing characters and curated ANSI color palettes.
- **🤖 Three Gameplay Modes**:
  - **PVP (Local)**: Play against a friend sitting next to you.
  - **PVE (Casual AI)**: Play against a relaxed computer opponent that blocks wins but makes occasional mistakes.
  - **PVE (Beast AI)**: Test your skills against an unbeatable AI powered by the **Minimax algorithm**.
- **💡 How-to-Play Guide**: Quick instruction screen built directly into the game menu.
- **🛡️ Clean Terminal Exit**: Graceful handling of `Ctrl+C` and automated restoration of terminal settings.

---

## 🚀 How to Play

### Prerequisites
- Python 3.x installed on your Linux system.

### Running the Game
1. Open your terminal.
2. Navigate to the game folder on your Desktop:
   ```bash
   cd ~/Desktop/tic-tac-toe
   ```
3. Run the script:
   ```bash
   ./game.py
   ```
   *(Alternatively, you can run `python3 game.py`)*

---

## 🛠️ Project Structure
```
tic-tac-toe/
├── game.py       # Main Python game script
├── README.md     # Project documentation
├── .gitignore    # Standard git ignores for Python
└── LICENSE       # MIT License
```

---

## 📤 Pushing to GitHub

To publish this game to your GitHub profile, run the following commands in your terminal:

1. **Initialize Git Repository**:
   ```bash
   cd ~/Desktop/tic-tac-toe
   git init
   ```

2. **Add all files & Commit**:
   ```bash
   git add .
   git commit -m "Initial commit: Minimal and Professional Tic-Tac-Toe terminal game"
   ```

3. **Link to GitHub & Push**:
   Create a new blank repository on [GitHub](https://github.com/new) and run:
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
   git push -u origin main
   ```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
