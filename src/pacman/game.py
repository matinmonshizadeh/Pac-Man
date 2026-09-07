"""Game state: the maze contents, score, power-pellet timer and the
playing / won / lost state machine. Knows nothing about GLFW or OpenGL."""

import math

from pacman.config import (
    FOOD,
    FOOD_SCORE,
    FRIGHTENED_GHOST_COLOR,
    GHOST_COLORS,
    GHOST_RADIUS,
    GHOST_SPAWN_CELLS,
    PACMAN_RADIUS,
    POWER_DURATION,
    POWER_FOOD_SCORE,
    STATE_DURATION,
)
from pacman.entities import Ghost, PacMan

PLAYING = "playing"
WON = "won"
LOST = "lost"


class Game:
    def __init__(self, ghost_speed, now):
        self.ghost_speed = ghost_speed
        self.pacman = PacMan()
        self.ghosts = [Ghost(cell, color) for cell, color in zip(GHOST_SPAWN_CELLS, GHOST_COLORS)]
        self.restart(now)

    def restart(self, now):
        self.food = [row[:] for row in FOOD]
        self.score = 0
        self.power_active = False
        self.power_start_time = 0.0
        self.pacman.reset()
        for ghost in self.ghosts:
            ghost.reset()
        self._set_state(PLAYING, now)

    def handle_direction_key(self, direction):
        if self.state == PLAYING:
            self.pacman.request_direction(direction)

    def update(self, dt, now):
        if self.state != PLAYING:
            if now - self.state_start_time >= STATE_DURATION:
                self.restart(now)
            return

        if self.power_active and now - self.power_start_time >= POWER_DURATION:
            self._end_power_mode()

        self.pacman.update(dt)
        if self.pacman.moving:
            self._eat_food(now)
        if self.state != PLAYING:
            return

        target = (self.pacman.x, self.pacman.y)
        for ghost in self.ghosts:
            ghost.update(dt, self.ghost_speed, target, self.power_active, self.ghosts)
        self._check_ghost_collisions(now)

    def _eat_food(self, now):
        row, col = self.pacman.cell()
        pellet = self.food[row][col]
        if pellet == 0:
            return
        self.food[row][col] = 0
        if pellet == 1:
            self.score += FOOD_SCORE
        else:
            self.score += POWER_FOOD_SCORE
            self._start_power_mode(now)
        if not any(pellet for row in self.food for pellet in row):
            self._set_state(WON, now)

    def _start_power_mode(self, now):
        self.power_active = True
        self.power_start_time = now
        for ghost in self.ghosts:
            ghost.color = FRIGHTENED_GHOST_COLOR

    def _end_power_mode(self):
        self.power_active = False
        for ghost in self.ghosts:
            ghost.color = ghost.normal_color

    def _check_ghost_collisions(self, now):
        for ghost in self.ghosts:
            distance = math.hypot(ghost.x - self.pacman.x, ghost.y - self.pacman.y)
            if distance >= PACMAN_RADIUS + GHOST_RADIUS:
                continue
            if self.power_active:
                ghost.reset()  # Eaten: back to the ghost house
                ghost.color = FRIGHTENED_GHOST_COLOR
            else:
                self._set_state(LOST, now)
                return

    def _set_state(self, state, now):
        self.state = state
        self.state_start_time = now
