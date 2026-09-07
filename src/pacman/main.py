"""Entry point: GLFW windows, input mapping and the frame loop."""

import glfw

from pacman import rendering
from pacman.config import (
    DIFFICULTY_SCREEN,
    DIFFICULTY_SCREEN_COLOR,
    DIFFICULTY_TITLE,
    GHOST_SPEEDS,
    LOST_SCREEN,
    LOST_SCREEN_COLOR,
    MAX_DELTA_TIME,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH,
    WON_SCREEN,
    WON_SCREEN_COLOR,
)
from pacman.game import LOST, WON, Game

DIFFICULTY_KEYS = {glfw.KEY_1: "easy", glfw.KEY_2: "normal", glfw.KEY_3: "hard"}
DIRECTION_KEYS = {
    glfw.KEY_LEFT: "LEFT",
    glfw.KEY_RIGHT: "RIGHT",
    glfw.KEY_UP: "UP",
    glfw.KEY_DOWN: "DOWN",
}


def create_window(title):
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, title, None, None)
    if not window:
        raise RuntimeError("Could not create the GLFW window")
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, lambda _window, w, h: rendering.set_viewport(w, h))
    rendering.setup_projection()
    return window


def select_difficulty():
    """Show the difficulty screen until the player presses 1, 2 or 3.
    Returns the difficulty name, or None if the window was closed."""
    window = create_window(DIFFICULTY_TITLE)
    difficulty = None
    while difficulty is None and not glfw.window_should_close(window):
        rendering.clear()
        rendering.draw_screen(DIFFICULTY_SCREEN, DIFFICULTY_SCREEN_COLOR)
        glfw.swap_buffers(window)
        glfw.poll_events()
        for key, name in DIFFICULTY_KEYS.items():
            if glfw.get_key(window, key) == glfw.PRESS:
                difficulty = name
    glfw.destroy_window(window)
    return difficulty


def play(difficulty):
    game = Game(GHOST_SPEEDS[difficulty], glfw.get_time())
    window = create_window(f"{WINDOW_TITLE} | Score: 0")

    def on_key(_window, key, _scancode, action, _mods):
        if action == glfw.PRESS and key in DIRECTION_KEYS:
            game.handle_direction_key(DIRECTION_KEYS[key])

    glfw.set_key_callback(window, on_key)

    shown_score = 0
    last_time = glfw.get_time()
    while not glfw.window_should_close(window):
        now = glfw.get_time()
        dt = min(now - last_time, MAX_DELTA_TIME)
        last_time = now

        game.update(dt, now)
        if game.score != shown_score:
            shown_score = game.score
            glfw.set_window_title(window, f"{WINDOW_TITLE} | Score: {shown_score}")

        rendering.clear()
        if game.state == WON:
            rendering.draw_screen(WON_SCREEN, WON_SCREEN_COLOR)
        elif game.state == LOST:
            rendering.draw_screen(LOST_SCREEN, LOST_SCREEN_COLOR)
        else:
            rendering.draw_game(game)
        glfw.swap_buffers(window)
        glfw.poll_events()


def main():
    if not glfw.init():
        raise SystemExit("Could not initialise GLFW")
    try:
        difficulty = select_difficulty()
        if difficulty is not None:
            play(difficulty)
    finally:
        glfw.terminate()


if __name__ == "__main__":
    main()
