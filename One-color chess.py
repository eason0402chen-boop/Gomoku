import tkinter as tk
from tkinter import messagebox

WIDTH = 750
HEIGHT = 750
MARGIN = 60
GRID_SIZE = 19
CELL_SIZE = (WIDTH - 2 * MARGIN) // (GRID_SIZE - 1)

current_player = "玩家 1"  
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


def check_win(x, y, player):
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
                if board_state.get((nx, ny)) == player:
                    count += 1
                    step += 1
                else:
                    break  
        if count >= 5:
            return True
    return False

def reveal_board():
    for (x, y), player in board_state.items():
        real_color = "black" if player == "玩家 1" else "white"
        draw_stone(canvas, x, y, real_color)


def handle_click(event):
    global current_player, game_over
    
    if game_over:
        return

    grid_x = round((event.x - MARGIN) / CELL_SIZE) + 1
    grid_y = round((event.y - MARGIN) / CELL_SIZE) + 1
    
    if not (1 <= grid_x <= 19 and 1 <= grid_y <= 19):
        return  
        
    if (grid_x, grid_y) in board_state:
        return
        

    draw_stone(canvas, grid_x, grid_y, "white")
    
    board_state[(grid_x, grid_y)] = current_player  
    
    if check_win(grid_x, grid_y, current_player):
        game_over = True
        root.title(f"19x19 一色五子棋 - 遊戲結束！")
        
        reveal_board()
        
        messagebox.showinfo("遊戲結束！", f"恭喜 {current_player} 獲勝！")
        return
    
    current_player = "玩家 2" if current_player == "玩家 1" else "玩家 1"
    root.title(f"19x19 一色五子棋 - 輪到：{current_player}")


root = tk.Tk()
root.title(f"19x19 一色五子棋 - 輪到：{current_player}")
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