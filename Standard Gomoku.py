import tkinter as tk
from tkinter import messagebox  

WIDTH = 750
HEIGHT = 750
MARGIN = 60
GRID_SIZE = 19
CELL_SIZE = (WIDTH - 2 * MARGIN) // (GRID_SIZE - 1)

current_turn = "black"  
board_state = {}        
game_over = False       


def get_pixel_coord(grid_x, grid_y):
    px = MARGIN + (grid_x - 1) * CELL_SIZE
    py = MARGIN + (grid_y - 1) * CELL_SIZE
    return px, py

def draw_stone(canvas, grid_x, grid_y, color):
    px, py = get_pixel_coord(grid_x, grid_y)
    r = CELL_SIZE // 2 - 2  
    outline_color = "gray" if color == "white" else "black"
    canvas.create_oval(px - r, py - r, px + r, py + r, fill=color, outline=outline_color)


def check_win(x, y, color):
    directions = [
        [(1, 0), (-1, 0)],   
        [(0, 1), (0, -1)],   
        [(1, 1), (-1, -1)],  
        [(1, -1), (-1, 1)]   
    ]

    for axis in directions:
        count = 1  
        for dx, dy in axis:
            step = 1
            while True:
                nx, ny = x + dx * step, y + dy * step
                if board_state.get((nx, ny)) == color:
                    count += 1
                    step += 1
                else:
                    break  
        if count >= 5:
            return True      
    return False


def handle_click(event):
    global current_turn, game_over
    
    if game_over:
        return

    grid_x = round((event.x - MARGIN) / CELL_SIZE) + 1
    grid_y = round((event.y - MARGIN) / CELL_SIZE) + 1
    
    if not (1 <= grid_x <= 19 and 1 <= grid_y <= 19):
        return  
        
    if (grid_x, grid_y) in board_state:
        return
        

    draw_stone(canvas, grid_x, grid_y, current_turn)
    board_state[(grid_x, grid_y)] = current_turn  
    
    if check_win(grid_x, grid_y, current_turn):
        game_over = True
        winner_text = "黑子" if current_turn == "black" else "白子"

        messagebox.showinfo("gameover！", f"{winner_text} 獲勝！")
        return

    current_turn = "white" if current_turn == "black" else "black"


root = tk.Tk()
root.title("19x19 五子棋")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#FFFFFF")
canvas.pack()
canvas.bind("<Button-1>", handle_click)

board_x1, board_y1 = MARGIN - 20, MARGIN - 20
board_x2 = MARGIN + (GRID_SIZE - 1) * CELL_SIZE + 20
board_y2 = MARGIN + (GRID_SIZE - 1) * CELL_SIZE + 20
canvas.create_rectangle(board_x1, board_y1, board_x2, board_y2, fill="#F3CB78", outline="black", width=2)

for i in range(GRID_SIZE):
    x = MARGIN + i * CELL_SIZE
    canvas.create_line(x, MARGIN, x, HEIGHT - MARGIN, fill="black")
    y = MARGIN + i * CELL_SIZE
    canvas.create_line(MARGIN, y, WIDTH - MARGIN, y, fill="black")


star_coords = [4, 10, 16]
for i in star_coords:
    for j in star_coords:
        px, py = get_pixel_coord(i, j)
        canvas.create_oval(px - 4, py - 4, px + 4, py + 4, fill="black")

root.mainloop()