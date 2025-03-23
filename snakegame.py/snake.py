import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

class tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Game window
window = tkinter.Tk()
window.title("snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

# Center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Initialize game
snake = tile(5 * TILE_SIZE, 5 * TILE_SIZE)
food = tile(10 * TILE_SIZE, 10 * TILE_SIZE)
snake_body = []
velocityx = 0
velocityy = 0
game_over = False
score = 0

def change_direction(e):
    global velocityx, velocityy, game_over
    if game_over:
        if e.keysym == "space":
            reset_game()
        return
    if e.keysym == "Up" and velocityy != 1:
        velocityx = 0
        velocityy = -1
    elif e.keysym == "Down" and velocityy != -1:
        velocityx = 0
        velocityy = 1
    elif e.keysym == "Left" and velocityx != 1:
        velocityx = -1
        velocityy = 0
    elif e.keysym == "Right" and velocityx != -1:
        velocityx = 1
        velocityy = 0

def move():
    global snake, food, snake_body, game_over, score

    if game_over:
        return

    # Predict next position
    next_x = snake.x + velocityx * TILE_SIZE
    next_y = snake.y + velocityy * TILE_SIZE

    # Wall collision BEFORE moving
    if next_x < 0 or next_x >= WINDOW_WIDTH or next_y < 0 or next_y >= WINDOW_HEIGHT:
        game_over = True
        return

    # Self collision BEFORE moving
    for segment in snake_body:
        if next_x == segment.x and next_y == segment.y:
            game_over = True
            return

    # Food collision
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(tile(food.x, food.y))
        score += 1
        while True:
            food.x = random.randint(0, COLS - 1) * TILE_SIZE
            food.y = random.randint(0, ROWS - 1) * TILE_SIZE
            collision = False
            if food.x == snake.x and food.y == snake.y:
                collision = True
            for segment in snake_body:
                if segment.x == food.x and segment.y == food.y:
                    collision = True
                    break
            if not collision:
                break

    # Move body
    for i in range(len(snake_body) - 1, -1, -1):
        Tile = snake_body[i]
        if i == 0:
            Tile.x = snake.x
            Tile.y = snake.y
        else:
            prev_Tile = snake_body[i - 1]
            Tile.x = prev_Tile.x
            Tile.y = prev_Tile.y

    # Move snake head
    snake.x = next_x
    snake.y = next_y

def draw_snake_face(x, y):
    eye_size = TILE_SIZE // 5
    offset = TILE_SIZE // 4
    canvas.create_oval(x + offset, y + offset, x + offset + eye_size, y + offset + eye_size, fill="white")
    canvas.create_oval(x + TILE_SIZE - offset - eye_size, y + offset, x + TILE_SIZE - offset, y + offset + eye_size, fill="white")
    canvas.create_arc(x + offset, y + offset, x + TILE_SIZE - offset, y + TILE_SIZE - offset,
                      start=200, extent=140, style=tkinter.ARC, outline="white", width=2)

def draw_dead_face(x, y):
    offset = TILE_SIZE // 4
    eye_spacing = TILE_SIZE // 6

    # Draw x x eyes using lines
    canvas.create_line(x + offset, y + offset, x + offset + eye_spacing, y + offset + eye_spacing, fill="white", width=2)
    canvas.create_line(x + offset + eye_spacing, y + offset, x + offset, y + offset + eye_spacing, fill="white", width=2)

    canvas.create_line(x + TILE_SIZE - offset - eye_spacing, y + offset,
                       x + TILE_SIZE - offset, y + offset + eye_spacing, fill="white", width=2)
    canvas.create_line(x + TILE_SIZE - offset, y + offset,
                       x + TILE_SIZE - offset - eye_spacing, y + offset + eye_spacing, fill="white", width=2)

    # Draw :( mouth (sad arc)
    canvas.create_arc(x + offset, y + offset + eye_spacing, x + TILE_SIZE - offset, y + TILE_SIZE - offset,
                      start=20, extent=140, style=tkinter.ARC, outline="white", width=2)

def draw():
    global snake, food, game_over, snake_body, score
    move()
    canvas.delete("all")

    # Food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="lime green")

    # Snake body
    for Tile in snake_body:
        canvas.create_rectangle(Tile.x, Tile.y, Tile.x + TILE_SIZE, Tile.y + TILE_SIZE, fill="purple")

    # Snake head
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="purple")

    if not game_over:
        draw_snake_face(snake.x, snake.y)
    else:
        draw_dead_face(snake.x, snake.y)

    # Score
    canvas.create_text(80, 20, font=("Comic Sans MS", 20), text=f"Score: {score}", fill="white")

    if game_over:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font=("Comic Sans MS", 20),
                           text=f"Game Over: {score}", fill="white")
        canvas.create_text(WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) + 30, font=("Comic Sans MS", 15),
                           text=f"Press SPACE to reset", fill="white")

    window.after(100, draw)  # 10fps

def reset_game():
    global snake, food, snake_body, velocityx, velocityy, game_over, score
    snake = tile(5 * TILE_SIZE, 5 * TILE_SIZE)
    food = tile(10 * TILE_SIZE, 10 * TILE_SIZE)
    snake_body = []
    velocityx = 0
    velocityy = 0
    game_over = False
    score = 0

draw()
window.bind("<KeyRelease>", change_direction)
window.mainloop()
