"""
🐍💧🔫 Snake Water Gun Game
Features:
  - Emoji for each option
  - Win/Lose/Draw statistics
  - Sound effects (beep-based, cross-platform)
  - Input validation
  - 5-second timer (timeout = opponent wins)
"""

import random
import time
import sys
import os
import threading

# ──────────────────────────────────────────────────────────
# Platform-aware sound
# ──────────────────────────────────────────────────────────
def play_sound(sound_type: str):
    """Play a simple beep sound using cross-platform methods."""
    try:
        if sys.platform == "win32":
            import winsound
            if sound_type == "win":
                for freq, dur in [(523, 150), (659, 150), (784, 300)]:   # C-E-G ascending
                    winsound.Beep(freq, dur)
            elif sound_type == "lose":
                for freq, dur in [(400, 200), (300, 300)]:               # descending sad tones
                    winsound.Beep(freq, dur)
            elif sound_type == "draw":
                winsound.Beep(440, 300)                                   # single neutral A
            elif sound_type == "tick":
                winsound.Beep(800, 80)
            elif sound_type == "timeout":
                for freq, dur in [(300, 150), (250, 150), (200, 400)]:
                    winsound.Beep(freq, dur)
        else:
            # Linux / macOS – use 'print \a' bell character + optional system tools
            if sound_type == "win":
                tones = [("G5", 150), ("C6", 150), ("E6", 300)]
            elif sound_type == "lose":
                tones = [("A3", 200), ("F3", 400)]
            elif sound_type == "draw":
                tones = [("A4", 300)]
            elif sound_type == "tick":
                tones = [("C6", 80)]
            elif sound_type == "timeout":
                tones = [("D3", 150), ("B2", 150), ("G2", 400)]
            else:
                tones = []

            played = False
            # Try 'beep' command (Linux)
            if not played and sys.platform.startswith("linux"):
                try:
                    note_map = {
                        "G2": 98, "B2": 123, "D3": 147, "F3": 175, "A3": 220,
                        "A4": 440, "G5": 784, "C6": 1047, "E6": 1319,
                    }
                    cmd_parts = []
                    for note, dur in tones:
                        freq = note_map.get(note, 440)
                        cmd_parts.append(f"-f {freq} -l {dur}")
                    cmd = "beep " + " -n ".join(cmd_parts) + " 2>/dev/null"
                    ret = os.system(cmd)
                    if ret == 0:
                        played = True
                except Exception:
                    pass

            # Try 'afplay' / 'say' on macOS (silent fallback – just use terminal bell)
            if not played:
                # Terminal bell as last resort
                count = len(tones)
                for _ in range(count):
                    print("\a", end="", flush=True)
                    time.sleep(0.12)
    except Exception:
        # Never crash the game over sound failures
        pass


# ──────────────────────────────────────────────────────────
# Game data
# ──────────────────────────────────────────────────────────
OPTIONS = {
    "1": ("Snake", "🐍"),
    "2": ("Water", "💧"),
    "3": ("Gun",   "🔫"),
}

# Who beats whom: winner[a][b] → True means 'a' beats 'b'
BEATS = {
    "Snake": {"Water": True,  "Gun":   False, "Snake": False},
    "Water": {"Snake": False, "Gun":   True,  "Water": False},
    "Gun":   {"Snake": True,  "Water": False, "Gun":   False},
}

RULES_TEXT = """
  🐍 Snake  drinks  💧 Water   → Snake wins
  💧 Water  douses  🔫 Gun     → Water wins
  🔫 Gun    shoots  🐍 Snake   → Gun wins
"""


# ──────────────────────────────────────────────────────────
# Timer input (5-second countdown)
# ──────────────────────────────────────────────────────────
class TimedInput:
    """Read a line from stdin within `timeout` seconds."""

    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.result = None
        self._thread = None

    def _read(self):
        try:
            self.result = input()
        except EOFError:
            self.result = ""

    def get(self, prompt: str) -> str | None:
        """
        Display `prompt`, start countdown in background, read input.
        Returns the string if entered in time, or None on timeout.
        """
        print(prompt, end="", flush=True)
        self._thread = threading.Thread(target=self._read, daemon=True)
        self._thread.start()

        # Tick every second while waiting
        deadline = time.time() + self.timeout
        while self._thread.is_alive():
            remaining = deadline - time.time()
            if remaining <= 0:
                break
            # Print countdown on the same line (works in most terminals)
            secs_left = int(remaining) + 1
            print(f"\r{prompt}  ⏱  {secs_left}s ", end="", flush=True)
            if remaining <= 3:
                threading.Thread(target=play_sound, args=("tick",), daemon=True).start()
            self._thread.join(timeout=1)

        print()  # newline after input / timeout

        if self.result is not None:
            return self.result.strip()
        return None          # timed out


# ──────────────────────────────────────────────────────────
# Display helpers
# ──────────────────────────────────────────────────────────
DIVIDER   = "─" * 48
BOLD      = "\033[1m"
RESET     = "\033[0m"
GREEN     = "\033[92m"
RED       = "\033[91m"
YELLOW    = "\033[93m"
CYAN      = "\033[96m"
MAGENTA   = "\033[95m"

def clear():
    os.system("cls" if sys.platform == "win32" else "clear")

def header():
    print(f"\n{CYAN}{BOLD}{'🐍  SNAKE  •  WATER  •  GUN  🔫':^48}{RESET}")
    print(f"{CYAN}{DIVIDER}{RESET}\n")

def print_rules():
    print(f"{YELLOW}Rules:{RESET}{RULES_TEXT}")

def print_options():
    print(f"{BOLD}Choose your weapon:{RESET}")
    for key, (name, emoji) in OPTIONS.items():
        print(f"  [{key}]  {emoji}  {name}")
    print(f"  [q]  🚪  Quit\n")

def print_stats(stats: dict):
    total = stats["win"] + stats["lose"] + stats["draw"]
    print(f"\n{CYAN}{DIVIDER}{RESET}")
    print(f"{BOLD}📊 Statistics  (total rounds: {total}){RESET}")
    print(f"  {GREEN}✅  Wins  : {stats['win']}{RESET}")
    print(f"  {RED}❌  Losses: {stats['lose']}{RESET}")
    print(f"  {YELLOW}🤝  Draws : {stats['draw']}{RESET}")
    if total > 0:
        pct = stats["win"] / total * 100
        bar_filled = int(pct / 5)          # 20 chars → 100 %
        bar = "█" * bar_filled + "░" * (20 - bar_filled)
        print(f"  🏆  Win rate: [{bar}] {pct:.1f}%")
    print(f"{CYAN}{DIVIDER}{RESET}\n")


# ──────────────────────────────────────────────────────────
# Core game round
# ──────────────────────────────────────────────────────────
def play_round(stats: dict):
    print_options()

    ti = TimedInput(timeout=5)
    raw = ti.get("Your choice (1/2/3) → ")

    # ── Timeout ──────────────────────────────────────────
    if raw is None:
        print(f"\n{RED}{BOLD}⏰  Time's up! You took too long — Opponent wins this round!{RESET}\n")
        threading.Thread(target=play_sound, args=("timeout",), daemon=True).start()
        stats["lose"] += 1
        return

    # ── Quit ─────────────────────────────────────────────
    if raw.lower() == "q":
        print(f"\n{MAGENTA}👋  Thanks for playing! Final stats below.{RESET}")
        print_stats(stats)
        sys.exit(0)

    # ── Input validation ─────────────────────────────────
    if raw not in OPTIONS:
        print(f"\n{YELLOW}⚠️  Invalid input '{raw}'. "
              f"Please enter 1, 2, 3, or q.{RESET}\n")
        return          # don't count invalid input as a round

    # ── Valid choice ──────────────────────────────────────
    player_name, player_emoji = OPTIONS[raw]
    cpu_key    = random.choice(list(OPTIONS.keys()))
    cpu_name, cpu_emoji = OPTIONS[cpu_key]

    print(f"\n  You      →  {player_emoji}  {player_name}")
    print(f"  Opponent →  {cpu_emoji}  {cpu_name}\n")
    time.sleep(0.5)

    # ── Determine outcome ─────────────────────────────────
    if player_name == cpu_name:
        outcome = "draw"
        print(f"{YELLOW}{BOLD}🤝  It's a Draw!{RESET}\n")
        threading.Thread(target=play_sound, args=("draw",), daemon=True).start()

    elif BEATS[player_name][cpu_name]:
        outcome = "win"
        print(f"{GREEN}{BOLD}🎉  You Win!  {player_emoji} beats {cpu_emoji}{RESET}\n")
        threading.Thread(target=play_sound, args=("win",), daemon=True).start()

    else:
        outcome = "lose"
        print(f"{RED}{BOLD}💀  You Lose!  {cpu_emoji} beats {player_emoji}{RESET}\n")
        threading.Thread(target=play_sound, args=("lose",), daemon=True).start()

    stats[outcome] += 1


# ──────────────────────────────────────────────────────────
# Main loop
# ──────────────────────────────────────────────────────────
def main():
    stats = {"win": 0, "lose": 0, "draw": 0}

    clear()
    header()
    print_rules()
    input(f"  Press {BOLD}Enter{RESET} to start… ")

    while True:
        clear()
        header()
        print_stats(stats)
        play_round(stats)
        input(f"  Press {BOLD}Enter{RESET} for next round… ")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{MAGENTA}Game interrupted. Goodbye! 👋{RESET}\n")
        sys.exit(0)

