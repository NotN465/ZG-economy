import time
import keyboard
import pyautogui
import os
import threading
head = "👾"
tail = "🟩"
apple = "🍎"
whitespace = "⬜"
direction = "right"
matrix = [[whitespace for i in range(10)] for j in range(10)]
def direction_check():
    direction = "right"

    while True:
        if keyboard.is_pressed("w"):
            direction = "up"
        elif keyboard.is_pressed("s"):
            direction = "down"
        elif keyboard.is_pressed("d"):
            direction = "right"
        elif keyboard.is_pressed("a"):
            direction = "left"
        time.sleep(0.01)
def clear_terminal():
    os.system('cls')
def game_printing():
    while True:
        for i in range(10):
            print(matrix[i])
        time.sleep(0.2)
        clear_terminal()
direction_thread = threading.Thread(target=direction_check)
game_printing_thread = threading.Thread(target=game_printing)
game_printing_thread.start()
direction_thread.start()
direction_thread.join()
game_printing_thread.join()
