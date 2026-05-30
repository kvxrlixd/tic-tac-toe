# Tic-Tac-Toe CLI

A modern command-line implementation of the classic Tic-Tac-Toe game written in Python. The project requires no external dependencies and features keyboard-based navigation, ANSI color support, and multiple AI difficulty levels.

## Features

* Keyboard-based controls using Arrow Keys or WASD.
* Enter or Space to place a mark.
* ANSI-colored interface with Unicode board rendering.
* Multiple game modes:

  * Player vs Player
  * Player vs Computer (Casual AI)
  * Player vs Computer (Minimax AI)
* Built-in gameplay instructions.
* Graceful terminal cleanup and Ctrl+C handling.
* No third-party libraries required.

## Requirements

* Python 3.x
* Git

Verify that both are installed:

```bash
python3 --version
git --version
```

## Installation

Clone the repository:

```bash
git clone https://github.com/kvxrlixd/tic-tac-toe.git
```

Enter the project directory:

```bash
cd tic-tac-toe
```

Make the script executable (if needed):

```bash
chmod +x game.py
```

## Running the Game

Start the game with:

```bash
./game.py
```

Or run it with Python:

```bash
python3 game.py
```

## Controls

| Key               | Action      |
| ----------------- | ----------- |
| Arrow Keys / WASD | Move cursor |
| Enter / Space     | Place mark  |
| Ctrl+C            | Exit game   |

## Project Structure

```text
tic-tac-toe/
├── game.py
├── README.md
├── .gitignore
└── LICENSE
```

## Repository

https://github.com/kvxrlixd/tic-tac-toe

## License

This project is licensed under the MIT License. See the LICENSE file for details.
