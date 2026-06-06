import tkinter as tk
from tkinter import messagebox

WIDTH = 550
HEIGHT = 550
MARGIN = 50
GRID_SIZE = 19
CELL_SIZE = (WIDTH - 2 * MARGIN) // (GRID_SIZE - 1)

LETTERS = "ABCDEFGHIJKLMNOPQRS"
LETTER_TO_NUM = {letter: index + 1 for index, letter in enumerate(LETTERS)}

board_state = {}
current_turn = "black"  
game_over = False

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

def parse_input(user_input):
    
    user_input = user_input.strip().upper()
    if not user_input: return None
    
    if user_input[0] in LETTERS:
        try:
            x = LETTER_TO_NUM[user_input[0]]
            y = int(user_input[1:])
            return x, y
        except ValueError:
            pass
            
    parts = user_input.replace(',', ' ').split()
    if len(parts) == 2:
        try:
            return int(parts[0]), int(parts[1])
        except ValueError:
            pass
    return None

def get_pixel_coord(grid_x, grid_y):
    px = MARGIN + (grid_x - 1) * CELL_SIZE
    py = MARGIN + (grid_y - 1) * CELL_SIZE
    return px, py

def draw_stone(grid_x, grid_y, color):
    px, py = get_pixel_coord(grid_x, grid_y)
    r = CELL_SIZE // 2 - 2  
    outline_color = "gray" if color == "white" else "black"
    canvas.create_oval(px - r, py - r, px + r, py + r, fill=color, outline=outline_color)

def reveal_board():
    for (x, y), color in board_state.items():
        draw_stone(x, y, color)

def handle_submit(event=None):
    global current_turn, game_over
    
    if game_over:
        return
        
    user_input = entry.get()
    entry.delete(0, tk.END)  
    
    coords = parse_input(user_input)
    
    if not coords:
        status_label.config(text=f"格式錯誤！請重新輸入 (例: 10，10)\n目前輪到：{'黑子' if current_turn == 'black' else '白子'}", fg="red")
        return
        
    grid_x, grid_y = coords
    
    if not (1 <= grid_x <= 19 and 1 <= grid_y <= 19):
        status_label.config(text=f"座標超出邊界！\n目前輪到：{'黑子' if current_turn == 'black' else '白子'}", fg="red")
        return
        
    if (grid_x, grid_y) in board_state:
        occupier = "黑子" if board_state[(grid_x, grid_y)] == "black" else "白子"
        status_label.config(text=f"該位置已有 {occupier}\n目前輪到：{'黑子' if current_turn == 'black' else '白子'}", fg="red")
        return
        
    board_state[(grid_x, grid_y)] = current_turn
    
    if check_win(grid_x, grid_y, current_turn):
        game_over = True
        winner_text = "黑子" if current_turn == "black" else "白子"
        status_label.config(text=f"🎉 gameover！{winner_text} 獲勝！", fg="blue")
        
        reveal_board()
        
        messagebox.showinfo("gameover！", f"{winner_text} 獲勝！")
        entry.config(state="disabled") 
        btn_submit.config(state="disabled")
        return
        
    current_turn = "white" if current_turn == "black" else "black"
    player_text = "黑子" if current_turn == "black" else "白子"
    status_label.config(text=f"成功落子！\n👉 現在輪到：{player_text} (請輸入座標)", fg="black")


root = tk.Tk()
root.title("盲棋五子棋")
root.resizable(False, False)


status_label = tk.Label(root, text="請在下方輸入座標。\n👉 現在輪到：黑子", font=("Arial", 12, "bold"), pady=10)
status_label.pack()


canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#FFFFFF")
canvas.pack()


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



input_frame = tk.Frame(root, pady=10)
input_frame.pack()

tk.Label(input_frame, text="輸入座標: ", font=("Arial", 12)).pack(side=tk.LEFT)
entry = tk.Entry(input_frame, font=("Arial", 12), width=10)
entry.pack(side=tk.LEFT, padx=5)
entry.bind("<Return>", handle_submit)  

btn_submit = tk.Button(input_frame, text="確認落子", font=("Arial", 12), command=handle_submit)
btn_submit.pack(side=tk.LEFT)

root.mainloop()