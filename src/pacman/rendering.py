"""Immediate-mode OpenGL drawing of the maze, Pac-Man, ghosts and screens."""

import math

import OpenGL.GL as gl

from pacman.config import (
    BACKGROUND_COLOR,
    CELL_SIZE,
    EYE_BLACK,
    EYE_WHITE,
    FOOD_COLOR,
    GHOST_RADIUS,
    GRID_SIZE,
    PACMAN_COLOR,
    PACMAN_RADIUS,
    WALLS,
    WALL_COLOR,
    cell_center,
)

CIRCLE_SEGMENTS = 100


def setup_projection():
    """2D orthographic projection covering clip space -1..1 on both axes."""
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glClearColor(*BACKGROUND_COLOR, 1.0)


def set_viewport(width, height):
    """Keep the maze square and centred whatever the window size."""
    size = min(width, height)
    gl.glViewport((width - size) // 2, (height - size) // 2, size, size)


def clear():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glLoadIdentity()


def draw_rectangle(x, y, width, height):
    gl.glBegin(gl.GL_QUADS)
    gl.glVertex2f(x, y)
    gl.glVertex2f(x + width, y)
    gl.glVertex2f(x + width, y + height)
    gl.glVertex2f(x, y + height)
    gl.glEnd()


def draw_circle(x, y, radius, segments=CIRCLE_SEGMENTS):
    gl.glBegin(gl.GL_TRIANGLE_FAN)
    for i in range(segments):
        angle = 2.0 * math.pi * i / segments
        gl.glVertex2f(x + radius * math.cos(angle), y + radius * math.sin(angle))
    gl.glEnd()


def draw_pacman(pacman):
    """A disc with a wedge cut out for the mouth, facing the move direction."""
    mouth_angle = math.pi / 4 if pacman.mouth_open else 0.0
    facing = {"RIGHT": 0.0, "UP": math.pi / 2, "LEFT": math.pi, "DOWN": -math.pi / 2}[pacman.direction]
    start_angle = facing + mouth_angle
    end_angle = facing + 2 * math.pi - mouth_angle

    gl.glColor3f(*PACMAN_COLOR)
    gl.glBegin(gl.GL_TRIANGLE_FAN)
    gl.glVertex2f(pacman.x, pacman.y)  # Centre of the fan
    for i in range(CIRCLE_SEGMENTS + 1):
        angle = start_angle + i * (end_angle - start_angle) / CIRCLE_SEGMENTS
        gl.glVertex2f(pacman.x + PACMAN_RADIUS * math.cos(angle), pacman.y + PACMAN_RADIUS * math.sin(angle))
    gl.glEnd()


def draw_ghost(ghost):
    """A rounded top over a rectangular body, with two eyes."""
    radius = GHOST_RADIUS
    gl.glColor3f(*ghost.color)
    draw_rectangle(ghost.x - radius, ghost.y - radius, radius * 2, radius)
    draw_circle(ghost.x, ghost.y, radius)

    eye_radius = radius / 4
    eye_offset = radius / 3
    for side in (-1, 1):
        gl.glColor3f(*EYE_WHITE)
        draw_circle(ghost.x + side * eye_offset, ghost.y + eye_offset, eye_radius)
        gl.glColor3f(*EYE_BLACK)
        draw_circle(ghost.x + side * eye_offset, ghost.y + eye_offset, eye_radius / 2)


def draw_maze(food):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if WALLS[row][col] == 1:
                gl.glColor3f(*WALL_COLOR)
                draw_rectangle(-1.0 + col * CELL_SIZE, 1.0 - (row + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            elif food[row][col] == 1:
                gl.glColor3f(*FOOD_COLOR)
                draw_circle(*cell_center(row, col), CELL_SIZE / 8, 10)
            elif food[row][col] == 2:
                gl.glColor3f(*FOOD_COLOR)
                draw_circle(*cell_center(row, col), CELL_SIZE / 3, 15)


def draw_game(game):
    draw_maze(game.food)
    draw_pacman(game.pacman)
    for ghost in game.ghosts:
        draw_ghost(ghost)


def draw_screen(pixels, color):
    """Draw a pixel-art message: one square per lit cell of the 28x28 grid."""
    gl.glColor3f(*color)
    for row in range(len(pixels)):
        for col in range(len(pixels[row])):
            if pixels[row][col] == 1:
                x, y = cell_center(row, col)
                draw_rectangle(x, y, CELL_SIZE, CELL_SIZE)
