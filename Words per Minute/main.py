import curses
from curses import wrapper
import time
import random

sample_texts = [
    "Typing is a skill that improves with practice.",
    "The quick brown fox jumps over the lazy dog.",
    "Accuracy and speed are crucial for typing tests.",
    "Improve your typing with consistent practice.",
    "A fast and accurate typist can be more productive.",
    "Practice makes perfect when it comes to typing.",
    "Consistency in typing practice boosts speed and accuracy.",
    "Typing accurately is as important as typing quickly.",
    "Proper finger positioning can improve typing skills.",
    "Typing tests can be fun and challenging to complete.",
    "The fox ran fast to avoid the hunter in the woods.",
    "Every journey begins with a single step forward.",
    "Learning to type fast can save a lot of time daily.",
    "Typing helps in communicating ideas effectively.",
    "Good typing skills are beneficial in many careers.",
]

def start_scr(stdscr):
    stdscr.clear()
    stdscr.addstr("~Welcome to the WPM test~")
    stdscr.addstr("\nPress any key to start the test (Press 'Esc' to quit).")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0, accuracy=0, time_left=60):
    stdscr.addstr(0, 0, target, curses.color_pair(3))
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1) if char == correct_char else curses.color_pair(2)
        stdscr.addstr(0, i, char, color)
    stdscr.addstr(2, 0, f"WPM: {wpm}")
    stdscr.addstr(3, 0, f"Accuracy: {accuracy}%")
    stdscr.addstr(4, 0, f"Time left: {time_left}s")

def wpm_test(stdscr):
    target_text = random.choice(sample_texts)
    current_text = []
    start_time = time.time()
    time_limit = 60
    while True:
        stdscr.clear()
        time_elapsed = time.time() - start_time
        time_left = max(0, int(time_limit - time_elapsed))
        if time_elapsed > 0:
            wpm = round((len(current_text) / 5) / (time_elapsed / 60))
            correct_chars = sum(1 for i, char in enumerate(current_text) if i < len(target_text) and char == target_text[i])
            accuracy = round((correct_chars / len(current_text)) * 100) if current_text else 0
        else:
            wpm = 0
            accuracy = 0
        display_text(stdscr, target_text, current_text, wpm, accuracy, time_left)
        stdscr.refresh()
        if time_left == 0:
            break
        key = stdscr.getkey()
        if ord(key) == 27:
            return False
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)
        if ''.join(current_text) == target_text:
            stdscr.clear()
            stdscr.addstr(2, 0, "Great job! Moving to the next text...")
            stdscr.refresh()
            time.sleep(2)
            target_text = random.choice(sample_texts)
            current_text = []
    stdscr.clear()
    stdscr.addstr(2, 0, f"Time's up!")
    stdscr.addstr(3, 0, f"Your typing speed was {wpm} WPM.")
    stdscr.addstr(4, 0, f"Your typing accuracy was {accuracy}%.")
    stdscr.addstr(6, 0, "Press 'R' to restart or 'Esc' to exit.")
    stdscr.refresh()
    while True:
        key = stdscr.getkey()
        if key.upper() == 'R':
            return True
        elif ord(key) == 27:
            return False

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    start_scr(stdscr)
    while True:
        if not wpm_test(stdscr):
            break

wrapper(main)
