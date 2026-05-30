#!/usr/bin/env python3
import sys
import tty
import termios
import time
import random

# Color Codes (ANSI Escape Sequences)
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[38;5;51m"
MAGENTA = "\033[38;5;201m"
YELLOW = "\033[38;5;226m"
GREEN = "\033[38;5;82m"
RED = "\033[38;5;196m"
BORDER = "\033[38;5;244m"
SEL_BG = "\033[48;5;236m"
WHITE = "\033[38;5;255m"

class TicTacToe:
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = None
        self.reset_game()

    def reset_game(self):
        self.board = [' '] * 9
        self.cursor = 4  # Start in the center cell
        self.turn = 'X'
        self.mode = None  # 'pvp', 'casual', 'beast'
        self.winner = None
        self.winning_line = None
        self.menu_cursor = 0  # 0: PvP, 1: PvE Casual, 2: PvE Beast, 3: How to Play, 4: Quit

    def enable_raw_mode(self):
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setcbreak(self.fd)
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def disable_raw_mode(self):
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        if self.old_settings:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

    def get_key(self):
        ch = sys.stdin.read(1)
        if ch == '\x03':  # Ctrl+C
            raise KeyboardInterrupt
        if ch == '\x1b':
            ch2 = sys.stdin.read(1)
            if ch2 == '[':
                ch3 = sys.stdin.read(1)
                if ch3 == 'A': return 'up'
                if ch3 == 'B': return 'down'
                if ch3 == 'C': return 'right'
                if ch3 == 'D': return 'left'
            return 'esc'
        if ch in ('\r', '\n'):
            return 'enter'
        if ch == ' ':
            return 'space'
        if ch.lower() == 'q':
            return 'quit'
        # WASD support
        if ch.lower() == 'w': return 'up'
        if ch.lower() == 's': return 'down'
        if ch.lower() == 'd': return 'right'
        if ch.lower() == 'a': return 'left'
        return ch.lower()

    def check_win(self):
        win_states = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # cols
            [0, 4, 8], [2, 4, 6]             # diagonals
        ]
        for win in win_states:
            if self.board[win[0]] == self.board[win[1]] == self.board[win[2]] != ' ':
                return self.board[win[0]], win
        if ' ' not in self.board:
            return 'tie', None
        return None, None

    # Minimax AI for Beast Mode
    def minimax(self, depth, is_maximizing):
        winner, _ = self.check_win()
        if winner == 'O':  # AI is O
            return 10 - depth
        if winner == 'X':  # Human is X
            return depth - 10
        if winner == 'tie':
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = 'O'
                    score = self.minimax(depth + 1, False)
                    self.board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = 'X'
                    score = self.minimax(depth + 1, True)
                    self.board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    def get_best_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                score = self.minimax(0, False)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def get_casual_move(self):
        # 1. Can AI win in this turn?
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                winner, _ = self.check_win()
                self.board[i] = ' '
                if winner == 'O':
                    return i
        # 2. Can Human win in this turn? Block it.
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'X'
                winner, _ = self.check_win()
                self.board[i] = ' '
                if winner == 'X':
                    return i
        # 3. Otherwise play randomly
        empty_cells = [i for i, x in enumerate(self.board) if x == ' ']
        return random.choice(empty_cells)

    def draw_menu(self):
        menu = [
            f"\033[H\033[J",
            f"    {BOLD}{CYAN}T I C   {MAGENTA}T A C   {YELLOW}T O E{RESET}   {DIM}(Terminal Edition){RESET}",
            f"    {DIM}─────────────────────────────────────────────────{RESET}",
            "",
            f"          {DIM}Use Arrow Keys / WASD to navigate{RESET}",
            f"          {DIM}Press Enter / Space to select{RESET}",
            "",
            f"          {BORDER}┌─────────────────────────────────┐{RESET}"
        ]

        options = [
            "1. Player vs Player (Local)",
            "2. Player vs AI (Casual Mode)",
            "3. Player vs AI (Beast Mode)",
            "4. How to Play",
            "5. Exit"
        ]

        for idx, option in enumerate(options):
            if idx == self.menu_cursor:
                menu.append(f"        {YELLOW}>{RESET} {SEL_BG}  {option.ljust(29)}  {RESET}")
            else:
                menu.append(f"          {WHITE}  {option.ljust(29)}  {RESET}")

        menu.extend([
            f"          {BORDER}└─────────────────────────────────┘{RESET}",
            "",
            f"    {DIM}Created by xorin | Minimal & Professional CLI{RESET}",
            ""
        ])
        sys.stdout.write("\n".join(menu))
        sys.stdout.flush()

    def draw_how_to_play(self):
        info = [
            f"\033[H\033[J",
            f"    {BOLD}{YELLOW}H O W   T O   P L A Y{RESET}",
            f"    {DIM}─────────────────────────────────────────────────{RESET}",
            "",
            f"    {BOLD}Controls:{RESET}",
            f"    • Move Cursor: {CYAN}Arrow Keys{RESET} or {CYAN}WASD{RESET}",
            f"    • Place Mark:  {CYAN}Enter{RESET} or {CYAN}Space{RESET}",
            f"    • Return to Menu / Quit: {RED}Q{RESET}",
            "",
            f"    {BOLD}Rules:{RESET}",
            f"    • Player 1 is {CYAN}X{RESET} and Player 2 / AI is {MAGENTA}O{RESET}.",
            f"    • Take turns placing your mark in empty cells.",
            f"    • The first player to align 3 of their marks",
            f"      horizontally, vertically, or diagonally wins!",
            "",
            f"    {BOLD}AI Modes:{RESET}",
            f"    • {GREEN}Casual Mode{RESET}: The AI plays smart moves but makes mistakes.",
            f"    • {RED}Beast Mode{RESET}: Unbeatable Minimax AI. You cannot win!",
            "",
            f"    {YELLOW}Press any key to return to the Main Menu...{RESET}"
        ]
        sys.stdout.write("\n".join(info))
        sys.stdout.flush()

    def draw_board_state(self):
        lines = [
            f"\033[H\033[J",
            f"    {BOLD}{CYAN}T I C   {MAGENTA}T A C   {YELLOW}T O E{RESET}   {DIM}(Terminal Edition){RESET}",
            f"    {DIM}─────────────────────────────────────────────────{RESET}",
            ""
        ]

        # Status Line
        if self.winner:
            if self.winner == 'tie':
                status = f"    {BOLD}{YELLOW}It's a Tie!{RESET}"
            elif self.mode != 'pvp' and self.winner == 'O':
                status = f"    {BOLD}{RED}AI Wins! Better luck next time.{RESET}"
            else:
                color = CYAN if self.winner == 'X' else MAGENTA
                status = f"    {BOLD}{color}Player {self.winner} Wins! 🎉{RESET}"
        else:
            color = CYAN if self.turn == 'X' else MAGENTA
            if self.mode != 'pvp' and self.turn == 'O':
                status = f"    {DIM}AI ({MAGENTA}O{DIM}) is thinking...{RESET}"
            else:
                player_lbl = "Player 1" if self.turn == 'X' else ("Player 2" if self.mode == 'pvp' else "AI")
                status = f"    Current Turn: {BOLD}{color}{player_lbl} ({self.turn}){RESET}"
        
        lines.append(status)
        lines.append("")

        # Helper to color and format cell content
        def get_cell_char(i):
            char = self.board[i]
            if self.winning_line and i in self.winning_line:
                color = f"{BOLD}{YELLOW}"
            elif char == 'X':
                color = f"{BOLD}{CYAN}"
            elif char == 'O':
                color = f"{BOLD}{MAGENTA}"
            else:
                color = RESET
            return f"{color}{char}{RESET}"

        # Board Drawing
        grid_str = []
        grid_str.append(f"         {BORDER}┌─────────┬─────────┬─────────┐{RESET}")
        
        for r in range(3):
            line_a = f"         {BORDER}│{RESET}"
            line_b = f"         {BORDER}│{RESET}"
            line_c = f"         {BORDER}│{RESET}"
            
            for c in range(3):
                idx = r * 3 + c
                is_selected = (idx == self.cursor and not self.winner)
                bg = SEL_BG if is_selected else ""
                val_char = get_cell_char(idx)
                
                if is_selected:
                    cell_a = f"{bg}         {RESET}"
                    cell_b = f"{bg}    {RESET}{val_char}{bg}    {RESET}"
                    cell_c = f"{bg}         {RESET}"
                else:
                    cell_a = "         "
                    cell_b = f"    {val_char}    "
                    cell_c = "         "
                    
                line_a += cell_a + f"{BORDER}│{RESET}"
                line_b += cell_b + f"{BORDER}│{RESET}"
                line_c += cell_c + f"{BORDER}│{RESET}"
                
            grid_str.append(line_a)
            grid_str.append(line_b)
            grid_str.append(line_c)
            
            if r < 2:
                grid_str.append(f"         {BORDER}├─────────┼─────────┼─────────┤{RESET}")
            else:
                grid_str.append(f"         {BORDER}└─────────┴─────────┴─────────┘{RESET}")
                
        lines.extend(grid_str)
        lines.append("")
        
        if self.winner:
            lines.append(f"    {YELLOW}Press Enter/Space to play again, or Q to go to Menu.{RESET}")
        else:
            lines.append(f"    {DIM}Use Arrow Keys/WASD to move | Enter/Space to place | Q to Exit{RESET}")
            
        sys.stdout.write("\n".join(lines))
        sys.stdout.flush()

    def run(self):
        try:
            self.enable_raw_mode()
            while True:
                if self.mode is None:
                    # MAIN MENU
                    self.draw_menu()
                    key = self.get_key()
                    if key == 'up':
                        self.menu_cursor = (self.menu_cursor - 1) % 5
                    elif key == 'down':
                        self.menu_cursor = (self.menu_cursor + 1) % 5
                    elif key in ('enter', 'space'):
                        if self.menu_cursor == 0:
                            self.mode = 'pvp'
                        elif self.menu_cursor == 1:
                            self.mode = 'casual'
                        elif self.menu_cursor == 2:
                            self.mode = 'beast'
                        elif self.menu_cursor == 3:
                            self.mode = 'instructions'
                        elif self.menu_cursor == 4:
                            break
                    elif key == 'quit':
                        break
                elif self.mode == 'instructions':
                    # HOW TO PLAY
                    self.draw_how_to_play()
                    self.get_key()
                    self.mode = None
                else:
                    # PLAYING THE GAME
                    self.draw_board_state()
                    
                    # If it's AI turn (and game is not over)
                    if self.mode != 'pvp' and self.turn == 'O' and not self.winner:
                        time.sleep(0.6)  # Simulate AI thinking
                        if self.mode == 'beast':
                            move = self.get_best_move()
                        else:
                            move = self.get_casual_move()
                        
                        if move is not None:
                            self.board[move] = 'O'
                            self.winner, self.winning_line = self.check_win()
                            self.turn = 'X'
                        continue
                    
                    # Human/Local Player Turn
                    key = self.get_key()
                    
                    if key == 'quit':
                        self.reset_game()
                        continue
                        
                    if self.winner:
                        if key in ('enter', 'space'):
                            m = self.mode
                            self.reset_game()
                            self.mode = m
                        continue

                    # Navigation
                    if key == 'up':
                        self.cursor = (self.cursor - 3) % 9
                    elif key == 'down':
                        self.cursor = (self.cursor + 3) % 9
                    elif key == 'left':
                        self.cursor = (self.cursor - 1) if self.cursor % 3 != 0 else self.cursor + 2
                    elif key == 'right':
                        self.cursor = (self.cursor + 1) if (self.cursor + 1) % 3 != 0 else self.cursor - 2
                    elif key in ('enter', 'space'):
                        if self.board[self.cursor] == ' ':
                            self.board[self.cursor] = self.turn
                            self.winner, self.winning_line = self.check_win()
                            if not self.winner:
                                self.turn = 'O' if self.turn == 'X' else 'X'

        except KeyboardInterrupt:
            pass
        finally:
            self.disable_raw_mode()
            # Clean exit and reset cursor/screen positioning
            sys.stdout.write(f"{RESET}\n    Thanks for playing Tic-Tac-Toe! Goodbye.\n\n")
            sys.stdout.flush()

if __name__ == '__main__':
    # Add a check to ensure python is run interactively in a tty
    if not sys.stdin.isatty():
        print("Error: This game must be run in an interactive terminal.")
        sys.exit(1)
        
    game = TicTacToe()
    game.run()
