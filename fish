#!/usr/bin/env python3

import curses
import random

BOARD_WIDTH = 40
BOARD_HEIGHT = 20


def spawn_food():
    return [
        random.randint(1, BOARD_WIDTH - 2),
        random.randint(1, BOARD_HEIGHT - 2),
    ]


def draw_board(stdscr, fish_pos, food_pos, score):
    stdscr.erase()

    for x in range(BOARD_WIDTH):
        stdscr.addstr(0, x, "-")
        stdscr.addstr(BOARD_HEIGHT - 1, x, "-")

    for y in range(BOARD_HEIGHT):
        stdscr.addstr(y, 0, "|")
        stdscr.addstr(y, BOARD_WIDTH - 1, "|")

    stdscr.addstr(food_pos[1], food_pos[0], "*")
    stdscr.addstr(fish_pos[1], fish_pos[0], "><>")
    stdscr.addstr(0, 2, f"Score: {score}")
    stdscr.addstr(0, 18, "Q to quit")
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    stdscr.timeout(120)

    fish_pos = [BOARD_WIDTH // 2, BOARD_HEIGHT // 2]
    food_pos = spawn_food()
    score = 0

    while True:
        key = stdscr.getch()

        if key in (ord("q"), ord("Q")):
            break
        elif key == curses.KEY_LEFT:
            fish_pos[0] -= 1
        elif key == curses.KEY_RIGHT:
            fish_pos[0] += 1
        elif key == curses.KEY_UP:
            fish_pos[1] -= 1
        elif key == curses.KEY_DOWN:
            fish_pos[1] += 1

        fish_pos[0] = max(1, min(fish_pos[0], BOARD_WIDTH - 2))
        fish_pos[1] = max(1, min(fish_pos[1], BOARD_HEIGHT - 2))

        if fish_pos == food_pos:
            score += 1
            food_pos = spawn_food()

        draw_board(stdscr, fish_pos, food_pos, score)

    stdscr.erase()
    stdscr.addstr(BOARD_HEIGHT // 2, BOARD_WIDTH // 2 - 6, "Game Over")
    stdscr.addstr(BOARD_HEIGHT // 2 + 1, BOARD_WIDTH // 2 - 9, "Press any key to exit")
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)