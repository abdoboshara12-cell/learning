#!/usr/bin/env python3

import curses
import random

BOARD_WIDTH = 40
BOARD_HEIGHT = 20


def spawn_food(board_width, board_height):
    return [
        random.randint(1, board_width - 2),
        random.randint(1, board_height - 2),
    ]


def get_board_size(stdscr):
    height, width = stdscr.getmaxyx()
    board_height = min(BOARD_HEIGHT, max(5, height - 1))
    board_width = min(BOARD_WIDTH, max(10, width - 1))
    return board_height, board_width


def draw_board(stdscr, fish_pos, food_pos, score, board_width, board_height):
    stdscr.erase()

    for x in range(board_width):
        try:
            stdscr.addstr(0, x, "-")
            stdscr.addstr(board_height - 1, x, "-")
        except curses.error:
            pass

    for y in range(board_height):
        try:
            stdscr.addstr(y, 0, "|")
            stdscr.addstr(y, board_width - 1, "|")
        except curses.error:
            pass

    try:
        stdscr.addstr(food_pos[1], food_pos[0], "*")
        stdscr.addstr(fish_pos[1], fish_pos[0], "><>")
        stdscr.addstr(0, 2, f"Score: {score}")
        stdscr.addstr(0, max(2, min(18, board_width - 10)), "Q to quit")
    except curses.error:
        pass

    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    stdscr.timeout(120)

    board_height, board_width = get_board_size(stdscr)
    fish_pos = [board_width // 2, board_height // 2]
    food_pos = spawn_food(board_width, board_height)
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

        board_height, board_width = get_board_size(stdscr)
        fish_pos[0] = max(1, min(fish_pos[0], board_width - 2))
        fish_pos[1] = max(1, min(fish_pos[1], board_height - 2))

        if fish_pos == food_pos:
            score += 1
            food_pos = spawn_food(board_width, board_height)

        draw_board(stdscr, fish_pos, food_pos, score, board_width, board_height)

    stdscr.erase()
    try:
        stdscr.addstr(board_height // 2, max(0, board_width // 2 - 6), "Game Over")
        stdscr.addstr(board_height // 2 + 1, max(0, board_width // 2 - 9), "Press any key to exit")
    except curses.error:
        pass
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
