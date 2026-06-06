import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys


def run_script(script_name):
    
    if not os.path.exists(script_name):
        messagebox.showerror("錯誤", f"找不到檔案：{script_name}\n請確認它和啟動器放在同一個資料夾！")
        return

    try:
        subprocess.Popen([sys.executable, script_name])
        status_label.config(text=f"✅ 成功啟動：{script_name}", fg="green")
    except Exception as e:
        messagebox.showerror("執行錯誤", f"無法執行 {script_name}\n錯誤訊息：{e}")

root = tk.Tk()
root.title("遊戲目錄")
root.geometry("300x350")
root.resizable(False, False)

title_label = tk.Label(root, text="🎮 請選擇要執行的程式", font=("Arial", 16, "bold"), pady=20)
title_label.pack()


btn_game1 = tk.Button(root, text="五字棋", font=("Arial", 12), width=25, pady=5,
                      command=lambda: run_script("Standard Gomoku.py"))
btn_game1.pack(pady=10)

btn_game2 = tk.Button(root, text="一色棋", font=("Arial", 12), width=25, pady=5,
                      command=lambda: run_script("One-color chess.py"))
btn_game2.pack(pady=10)

btn_game3 = tk.Button(root, text="盲棋", font=("Arial", 12), width=25, pady=5,
                      command=lambda: run_script("Blindfold Chess.py"))
btn_game3.pack(pady=10)


status_label = tk.Label(root, text="等待選擇...", font=("Arial", 10), fg="gray", pady=20)
status_label.pack(side=tk.BOTTOM)

root.mainloop()