"""Moving things: Pac-Man and the ghosts, plus wall collision."""

import math

from pacman.config import (
    DIRECTION_VECTORS,
    GRID_SIZE,
    MOUTH_INTERVAL,
    PACMAN_RADIUS,
    PACMAN_SPEED,
    PACMAN_START,
    WALLS,
    cell_at,
    cell_center,
)

GHOST_DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Right, Left, Up, Down


def is_move_valid(x, y, radius):
    """True if a square body of the given radius centred at (x, y) overlaps no
    wall. Columns wrap around horizontally, which turns the open-ended row into
    a tunnel."""
    corners = [
        (x - radius, y - radius),
        (x - radius, y + radius),
        (x + radius, y - radius),
        (x + radius, y + radius),
    ]
    for corner_x, corner_y in corners:
        row, col = cell_at(corner_x, corner_y)
        if not 0 <= row < GRID_SIZE:
            return False
        if WALLS[row][col % GRID_SIZE] == 1:
            return False
    return True


def snap_to_corridor(x, y, direction):
    """Align a point with the centre line of the corridor it is about to move
    along (cornering assist, so turns do not need pixel-perfect timing)."""
    row, col = cell_at(x, y)
    center_x, center_y = cell_center(row, col)
    dx, _ = DIRECTION_VECTORS[direction]
    return (x, center_y) if dx != 0 else (center_x, y)


class PacMan:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x, self.y = PACMAN_START
        self.direction = "RIGHT"        # Facing / moving direction
        self.wanted_direction = None    # Requested turn, taken at the next opening
        self.moving = False             # Waits for the first key press
        self.mouth_open = True
        self.mouth_timer = 0.0

    def cell(self):
        row, col = cell_at(self.x, self.y)
        return row, col % GRID_SIZE

    def _neighbour_is_open(self, dx, dy):
        # Pac-Man is smaller than a cell, so a single step can fit even when the
        # cell in that direction is a wall. Turning requires an open neighbour.
        row, col = self.cell()
        return WALLS[row - dy][(col + dx) % GRID_SIZE] == 0

    def request_direction(self, direction):
        if self.moving:
            self.wanted_direction = direction
        else:
            self.direction = direction
            self.moving = True

    def update(self, dt):
        if not self.moving:
            return
        step = PACMAN_SPEED * dt

        # Take the requested turn as soon as that corridor is open
        if self.wanted_direction is not None:
            x, y = snap_to_corridor(self.x, self.y, self.wanted_direction)
            dx, dy = DIRECTION_VECTORS[self.wanted_direction]
            if self._neighbour_is_open(dx, dy) and is_move_valid(x + dx * step, y + dy * step, PACMAN_RADIUS):
                self.x, self.y = x, y
                self.direction = self.wanted_direction
                self.wanted_direction = None

        dx, dy = DIRECTION_VECTORS[self.direction]
        new_x = self.x + dx * step
        new_y = self.y + dy * step
        if not is_move_valid(new_x, new_y, PACMAN_RADIUS):
            return  # Blocked by a wall: keep moving in place until a turn opens

        # Leaving one edge of the tunnel re-enters at the other
        if new_x < -1.0:
            new_x += 2.0
        elif new_x > 1.0:
            new_x -= 2.0
        self.x, self.y = new_x, new_y

        self.mouth_timer += dt
        if self.mouth_timer >= MOUTH_INTERVAL:
            self.mouth_timer = 0.0
            self.mouth_open = not self.mouth_open


class Ghost:
    def __init__(self, spawn_cell, color):
        self.spawn_cell = spawn_cell
        self.normal_color = color
        self.reset()

    def reset(self):
        self.x, self.y = cell_center(*self.spawn_cell)
        self.color = self.normal_color
        self.direction = None

    def cell(self):
        return cell_at(self.x, self.y)

    def update(self, dt, speed, target, frightened, ghosts):
        """Move along corridor centre lines; choose a new direction only when
        passing the centre of a cell."""
        step = speed * dt
        row, col = self.cell()
        center_x, center_y = cell_center(row, col)

        # Distance left before reaching the centre of the current cell
        if self.direction:
            to_center = (center_x - self.x) * self.direction[0] + (center_y - self.y) * self.direction[1]
        else:
            to_center = 0.0

        if self.direction is None or 0.0 <= to_center <= step:
            # Snap to the centre, pick the next corridor, use the remaining step
            self.direction = self._choose_direction(row, col, target, frightened, ghosts)
            self.x, self.y = center_x, center_y
            if self.direction:
                self.x += self.direction[0] * (step - to_center)
                self.y += self.direction[1] * (step - to_center)
        else:
            self.x += self.direction[0] * step
            self.y += self.direction[1] * step

    def _choose_direction(self, row, col, target, frightened, ghosts):
        """Greedy choice at a cell centre: of the free neighbouring cells, take
        the one closest to the target while chasing, or farthest while
        frightened. Never reverse unless it is a dead end, so the ghost commits
        to a corridor instead of oscillating when two moves are equally good."""
        reverse = (-self.direction[0], -self.direction[1]) if self.direction else None
        best_direction = None
        best_score = None
        for dx, dy in GHOST_DIRECTIONS:
            if (dx, dy) == reverse or not self._is_direction_free(row, col, dx, dy, ghosts):
                continue
            x, y = cell_center(row - dy, col + dx)
            distance = math.hypot(x - target[0], y - target[1])
            score = -distance if frightened else distance
            if best_score is None or score < best_score:
                best_score = score
                best_direction = (dx, dy)
        if best_direction is None and reverse and self._is_direction_free(row, col, *reverse, ghosts):
            best_direction = reverse
        return best_direction

    def _is_direction_free(self, row, col, dx, dy, ghosts):
        """The next cell must be inside the maze, not a wall, and not already
        taken by another ghost (in that cell, or ahead of us in this one)."""
        next_row, next_col = row - dy, col + dx
        if not (0 <= next_row < GRID_SIZE and 0 <= next_col < GRID_SIZE):
            return False
        if WALLS[next_row][next_col] == 1:
            return False
        for other in ghosts:
            if other is self:
                continue
            other_cell = other.cell()
            if other_cell == (next_row, next_col):
                return False
            if other_cell == (row, col) and (other.x - self.x) * dx + (other.y - self.y) * dy > 0:
                return False
        return True
