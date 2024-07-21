import glfw
import OpenGL.GL as gl  # PyOpenGL
import math


# Define the window size
window_width = 800
window_height = 800

# Pac-Man's position and movement
pacman_x = 0.0
pacman_y = -0.68
pacman_speed = 0.02
pacman_radius = 0.025
pacman_direction = 'RIGHT'  # Initial direction
mouth_open = True  # Initial state of Pac-Man's mouth

# Ghosts' positions and movement
ghosts = [
    {'x': -0.15, 'y': 0.0, 'color': (1.0, 0.0, 0.0), 'normal_color': (1.0, 0.0, 0.0)},     # Red ghost
    {'x': 0.15, 'y': 0.0, 'color': (1.0, 0.65, 0.0), 'normal_color': (1.0, 0.65, 0.0)},    # Orange ghost
    {'x': -0.15, 'y': -0.1, 'color': (1.0, 0.5, 0.5), 'normal_color': (1.0, 0.5, 0.5)},    # Pink ghost
    {'x': 0.15, 'y': -0.1, 'color': (0.0, 1.0, 1.0), 'normal_color': (0.0, 1.0, 1.0)},    # Cyan ghost
]
ghost_speed_easy = 0.0005
ghost_speed_normal = 0.001
ghost_speed_hard = 0.002
ghost_speed = ghost_speed_normal  # Default ghost speed

ghost_radius = 0.025

# Define the initial grid map (1: wall, 0: path)
initial_grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Define the initial food grid (2: special food, 1: food, 0: no food)
initial_food_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 2, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Initialize grids
grid = [row[:] for row in initial_grid]
food_grid = [row[:] for row in initial_food_grid]

# Cell size for the grid
cell_size = 2.0 / len(grid)  # Normalized size for OpenGL

# Time variables for special food effect
special_food_active = False
special_food_start_time = 0.0
special_food_duration = 5.0

# Game state variables
game_state = "playing"  # Can be "playing", "won", or "lost"
state_start_time = 0.0
state_duration = 3.0

# Score variable
score = 0

def draw_pacman(x, y, radius, direction, mouth_open):
    num_segments = 100
    mouth_angle = math.pi / 4 if mouth_open else 0

    start_angle = 0
    end_angle = 2 * math.pi

    if direction == 'LEFT':
        start_angle = math.pi + mouth_angle
        end_angle = 3 * math.pi - mouth_angle
    elif direction == 'RIGHT':
        start_angle = mouth_angle
        end_angle = 2 * math.pi - mouth_angle
    elif direction == 'UP':
        start_angle = math.pi / 2 + mouth_angle
        end_angle = 5 * math.pi / 2 - mouth_angle
    elif direction == 'DOWN':
        start_angle = -math.pi / 2 + mouth_angle
        end_angle = 3 * math.pi / 2 - mouth_angle

    gl.glBegin(gl.GL_TRIANGLE_FAN)
    gl.glVertex2f(x, y)  # Center of the fan
    for i in range(num_segments + 1):
        angle = start_angle + i * (end_angle - start_angle) / num_segments
        dx = radius * math.cos(angle)
        dy = radius * math.sin(angle)
        gl.glVertex2f(x + dx, y + dy)
    gl.glEnd()

def draw_circle(x, y, radius, num_segments):
    gl.glBegin(gl.GL_TRIANGLE_FAN)
    for i in range(num_segments):
        angle = 2.0 * math.pi * i / num_segments
        dx = radius * math.cos(angle)
        dy = radius * math.sin(angle)
        gl.glVertex2f(x + dx, y + dy)
    gl.glEnd()

def draw_rectangle(x, y, width, height):
    gl.glBegin(gl.GL_QUADS)
    gl.glVertex2f(x, y)
    gl.glVertex2f(x + width, y)
    gl.glVertex2f(x + width, y + height)
    gl.glVertex2f(x, y + height)
    gl.glEnd()

def draw_ghost(x, y, radius, num_segments):

    # Draw the body of the ghost
    draw_rectangle(x - ghost_radius, y - ghost_radius, ghost_radius*2, ghost_radius)
    draw_circle(x, y, radius, num_segments)

    # Draw the eyes of the ghost
    eye_radius = radius / 4
    eye_offset = radius / 3

    gl.glColor3f(1.0, 1.0, 1.0)  # White color for eyes
    draw_circle(x - eye_offset, y + eye_offset, eye_radius, num_segments)
    draw_circle(x + eye_offset, y + eye_offset, eye_radius, num_segments)
    gl.glColor3f(0.0, 0.0, 0.0)  # black color for eyes
    draw_circle(x - eye_offset, y + eye_offset, eye_radius / 2, num_segments)
    draw_circle(x + eye_offset, y + eye_offset, eye_radius / 2, num_segments)

def draw_map():
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 1:
                x = -1.0 + col * cell_size
                y = 1.0 - row * cell_size - cell_size
                gl.glColor3f(0.0, 0.0, 1.0)  # Blue color for walls
                draw_rectangle(x, y, cell_size, cell_size)
            elif food_grid[row][col] == 1:
                x = -1.0 + col * cell_size + cell_size / 2
                y = 1.0 - row * cell_size - cell_size / 2
                gl.glColor3f(1.0, 1.0, 1.0)  # White color for normal food
                draw_circle(x, y, cell_size / 8, 10)
            elif food_grid[row][col] == 2:
                x = -1.0 + col * cell_size + cell_size / 2
                y = 1.0 - row * cell_size - cell_size / 2
                gl.glColor3f(1.0, 1.0, 1.0)  # White color for special food
                draw_circle(x, y, cell_size / 3, 15)

def is_move_valid(new_x, new_y, radius):
    # Check four corners of Pac-Man's bounding box
    corners = [
        (new_x - radius, new_y - radius),
        (new_x - radius, new_y + radius),
        (new_x + radius, new_y - radius),
        (new_x + radius, new_y + radius)
    ]

    for (corner_x, corner_y) in corners:
        grid_col = int((corner_x + 1.0) / cell_size)
        grid_row = int((1.0 - corner_y) / cell_size)

        # Check if corner is outside the grid boundaries
        if grid_row < 0 or grid_row >= len(grid) or grid_col < 0 or grid_col >= len(grid[0]):
            return False

        # Check if corner is in a wall
        if grid[grid_row][grid_col] == 1:
            return False

    return True

def eat_food(x, y):
    global score
    # Check if Pac-Man's center overlaps with a food pellet's position
    grid_col = int((x + 1.0) / cell_size)
    grid_row = int((1.0 - y) / cell_size)

    if food_grid[grid_row][grid_col] == 1:
        food_grid[grid_row][grid_col] = 0
        score += 10  # Increment score for normal food
        update_window_title()
        return True
    elif food_grid[grid_row][grid_col] == 2:
        food_grid[grid_row][grid_col] = 0
        score += 50  # Increment score for special food
        update_window_title()
        activate_special_food()
        return True
    return False

def activate_special_food():
    global special_food_active, special_food_start_time

    special_food_active = True
    special_food_start_time = glfw.get_time()

    # Turn all ghosts' colors to blue
    for ghost in ghosts:
        ghost['color'] = (0.0, 0.0, 1.0)

def update_special_food():
    global special_food_active

    current_time = glfw.get_time()
    elapsed_time = current_time - special_food_start_time

    if elapsed_time >= special_food_duration:
        special_food_active = False

        # Revert ghosts' colors to their original
        for ghost in ghosts:
            ghost['color'] = ghost['normal_color']

def check_all_food_eaten():
    for row in food_grid:
        if 1 in row or 2 in row:
            return False
    return True

def restart_game():
    global grid, food_grid, pacman_x, pacman_y, ghosts, special_food_active, score

    grid = [row[:] for row in initial_grid]
    food_grid = [row[:] for row in initial_food_grid]
    pacman_x = 0.0
    pacman_y = -0.68
    special_food_active = False
    score = 0

    # Reset ghosts' positions and colors
    initial_positions = [(-0.15, 0.0), (0.15, 0.0), (-0.15, -0.1), (0.15, -0.1)]
    for i, ghost in enumerate(ghosts):
        ghost['x'], ghost['y'] = initial_positions[i]
        ghost['color'] = ghost['normal_color']

    update_window_title()
    trigger_game_state("playing")

def update_window_title():
    title = f"Pac-Man | Score: {score}"
    glfw.set_window_title(window, title)

def key_callback(window, key, scancode, action, mods):
    global pacman_x, pacman_y, pacman_direction, mouth_open
    if action == glfw.PRESS or action == glfw.REPEAT:
        new_x, new_y = pacman_x, pacman_y
        if key == glfw.KEY_LEFT:
            new_x -= pacman_speed
            pacman_direction = 'LEFT'
        elif key == glfw.KEY_RIGHT:
            new_x += pacman_speed
            pacman_direction = 'RIGHT'
        elif key == glfw.KEY_UP:
            new_y += pacman_speed
            pacman_direction = 'UP'
        elif key == glfw.KEY_DOWN:
            new_y -= pacman_speed
            pacman_direction = 'DOWN'

        # Check for collision and handle teleportation
        if is_move_valid(new_x, new_y, pacman_radius):
            # Handle teleportation
            if new_x < -1.0:
                new_x = 0.99 - pacman_radius
            elif new_x > 0.95:
                new_x = -1.0 + pacman_radius
            pacman_x, pacman_y = new_x, new_y
            mouth_open = not mouth_open  # Toggle mouth state
            if eat_food(pacman_x, pacman_y):
                if check_all_food_eaten():
                    trigger_game_state("won")

def move_ghost(ghost):
    global ghost_speed

    if ghost['color'] == (1.0, 0.0, 0.0) or ghost['color'] == (1.0, 0.65, 0.0) or ghost['color'] == (0.0, 1.0, 1.0) or ghost['color'] == (1.0, 0.5, 0.5) and not special_food_active:  # Ghost chases Pac-Man
        directions = [
            (ghost_speed, 0),   # Right
            (-ghost_speed, 0),  # Left
            (0, ghost_speed),   # Up
            (0, -ghost_speed)   # Down
        ]

        best_direction = None
        min_distance = float('inf')

        current_x = ghost['x']
        current_y = ghost['y']

        for dx, dy in directions:
            new_x = current_x + dx
            new_y = current_y + dy

            if is_move_valid(new_x, new_y, ghost_radius) and not will_collide_with_other_ghost(new_x, new_y, ghost):
                distance = math.sqrt((new_x - pacman_x) ** 2 + (new_y - pacman_y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    best_direction = (dx, dy)

        if best_direction:
            ghost['x'] += best_direction[0]
            ghost['y'] += best_direction[1]

    elif special_food_active:  # Ghosts run away from Pac-Man
        dx = ghost['x'] - pacman_x
        dy = ghost['y'] - pacman_y
        length = math.sqrt(dx * dx + dy * dy)

        if length > 0:
            dx /= length
            dy /= length

        new_x = ghost['x'] + dx * ghost_speed
        new_y = ghost['y'] + dy * ghost_speed

        if is_move_valid(new_x, new_y, ghost_radius) and not will_collide_with_other_ghost(new_x, new_y, ghost):
            ghost['x'] = new_x
            ghost['y'] = new_y

def will_collide_with_other_ghost(new_x, new_y, current_ghost):
    for ghost in ghosts:
        if ghost is not current_ghost:
            distance = math.sqrt((new_x - ghost['x']) ** 2 + (new_y - ghost['y']) ** 2)
            if distance < (ghost_radius * 2):
                return True
    return False

def check_collision_with_ghosts():
    for ghost in ghosts:
        distance = math.sqrt((ghost['x'] - pacman_x) ** 2 + (ghost['y'] - pacman_y) ** 2)
        if distance < (pacman_radius + ghost_radius):
            if special_food_active:
                # Respawn the ghost
                index = ghosts.index(ghost)
                initial_position = [(-0.15, -0.1), (0.15, 0.0), (0.15, -0.1), (-0.15, 0.0)]
                ghost['x'], ghost['y'] = initial_position[index]
            else:
                trigger_game_state("lost")
                return True
    return False

def trigger_game_state(state):
    global game_state, state_start_time
    game_state = state
    state_start_time = glfw.get_time()

def difficulty_selection():
    difficulty_selection_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
]
    # draw difficulty selection grid
    for row in range(len(difficulty_selection_grid)):
        for col in range(len(difficulty_selection_grid[row])):
            if difficulty_selection_grid[row][col] == 1:
                x = -1.0 + col * cell_size + cell_size / 2
                y = 1.0 - row * cell_size - cell_size / 2
                gl.glColor3f(1.0, 1.0, 1.0)
                draw_rectangle(x, y, cell_size, cell_size)

def won_state():
    won_state_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
]
    # draw difficulty selection grid
    for row in range(len(won_state_grid)):
        for col in range(len(won_state_grid[row])):
            if won_state_grid[row][col] == 1:
                x = -1.0 + col * cell_size + cell_size / 2
                y = 1.0 - row * cell_size - cell_size / 2
                gl.glColor3f(0.0, 1.0, 0.0)
                draw_rectangle(x, y, cell_size, cell_size)

def lose_state():
    lose_state_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
]
    # draw difficulty selection grid
    for row in range(len(lose_state_grid)):
        for col in range(len(lose_state_grid[row])):
            if lose_state_grid[row][col] == 1:
                x = -1.0 + col * cell_size + cell_size / 2
                y = 1.0 - row * cell_size - cell_size / 2
                gl.glColor3f(1.0, 0.0, 0.0)
                draw_rectangle(x, y, cell_size, cell_size)

def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glLoadIdentity()
    
    if game_state == "won":
        won_state()
    elif game_state == "lost":
        lose_state()
    else:
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)  # Black screen for playing
        # Draw map
        draw_map()
        
        # Draw Pac-Man
        gl.glColor3f(1.0, 1.0, 0.0)  # Yellow color
        draw_pacman(pacman_x, pacman_y, pacman_radius, pacman_direction, mouth_open)

        # Draw Ghosts
        for ghost in ghosts:
            gl.glColor3f(*ghost['color'])  # Ghost color
            draw_ghost(ghost['x'], ghost['y'], ghost_radius, 100)

    glfw.swap_buffers(window)

def main():
    global window, ghost_speed

    if not glfw.init():
        return

    # Resizability
    glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)

    # Create window for difficulty selection
    difficulty_window = glfw.create_window(800, 800, "Press a key to select difficulty (Easy: 1, Normal: 2, Hard: 3)", None, None)
    if not difficulty_window:
        glfw.terminate()
        return

    glfw.make_context_current(difficulty_window)

    # Difficulty selection loop
    while not glfw.window_should_close(difficulty_window):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()

        # Draw difficulty selection text
        difficulty_selection()


        glfw.swap_buffers(difficulty_window)
        glfw.poll_events()

        # Check for difficulty selection
        if glfw.get_key(difficulty_window, glfw.KEY_1) == glfw.PRESS:
            ghost_speed = ghost_speed_easy
            break
        elif glfw.get_key(difficulty_window, glfw.KEY_2) == glfw.PRESS:
            ghost_speed = ghost_speed_normal
            break
        elif glfw.get_key(difficulty_window, glfw.KEY_3) == glfw.PRESS:
            ghost_speed = ghost_speed_hard
            break

    glfw.destroy_window(difficulty_window)

    # Proceed to create main game window
    window = glfw.create_window(window_width, window_height, "Pac-Man | Score: 0", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()

    # Define clip space
    gl.glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)

    gl.glMatrixMode(gl.GL_MODELVIEW)

    while not glfw.window_should_close(window):
        if special_food_active:
            update_special_food()
        current_time = glfw.get_time()
        if game_state in ["won", "lost"] and current_time - state_start_time >= state_duration:
            restart_game()
        display()
        for ghost in ghosts:
            move_ghost(ghost)
        if game_state == "playing" and check_collision_with_ghosts():
            trigger_game_state("lost")
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
