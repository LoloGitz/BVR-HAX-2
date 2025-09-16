import random
import math
import os
import time
import termios
import sys
import tty
import select
import threading

from typing import Optional

if os.name == "nt":
    import msvcrt

load_iterations = 4
load_x = 500
load_y = 500
camera_range_x = 81
camera_range_y = 46

tiles_loaded = 0
tiles_to_load = load_x * load_y * load_iterations

validSpawnTiles = "🟩🟨"

random.seed()

def update_terminal(message: str = None) -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    
    if (message != None):
        print(message)

def get_key() -> Optional[str]:
    if os.name == "nt":  # If the operating system is Windows
        if msvcrt.kbhit():  # Checks if a keypress is available
            return msvcrt.getch().decode("utf-8")  # Reads the keypress
    else:  # If the operating system is macOS or Linux
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char
    
def updateLoading():
    global tiles_loaded
    global tiles_to_load

    ratio = round(tiles_loaded / tiles_to_load * 100) / 100
    ratio_bar = math.floor(ratio * 10)  

    update_terminal(
        "loading map... " 
        + str(round(ratio * 100))
        + "%\n-[ " + ("■" * ratio_bar)
        + ("□" * (10 - ratio_bar))
        + " ]-"
    )
    
#update_terminal()

mult = 1.3

def generateNoise(x: int, y: int, iterations: int, batch: dict = None) -> dict:
    global tiles_loaded
    result = {}
    lowest, highest = 1, 0

    for y_i in range(y):
        result[y_i] = {}
        for x_i in range(x):
            weight = 0

            if (batch == None):
                weight = random.uniform(0, 1)
            else:
                new_value = 0
                neighbors = 0

                for i in range(9):
                    xx = x_i + ((i % 3) - 1)
                    yy = y_i + (math.floor(i / 3) - 1)
                    
                    if (xx >= 0 and xx <= (x - 1) and yy >= 0 and yy <= (y - 1)):
                        new_value += batch[yy][xx]
                        neighbors += 1
                    
                weight = (0.5 + (new_value / neighbors)) * mult - 0.5

            lowest, highest = min(lowest, weight), max(highest, weight)
            result[y_i][x_i] = weight

            tiles_loaded += 1
            if (tiles_loaded % math.floor(tiles_to_load / 100) == 0):
                updateLoading()
                    
    if (iterations > 1):
        return generateNoise(x, y, iterations - 1, result)
    else:
        filt = {}

        for y_i in range(y):
            filt[y_i] = {}
            for x_i in range(x):
                weight = (result[y_i][x_i] - lowest) / (highest - lowest)

                rand = random.randint(0, 100)
                if weight >= 0.8 and rand <= 20:
                    if rand == 1:
                        weight = "🎄"
                    else:
                        weight = "🌲"
                elif weight >= 0.65:
                    weight = "🟩"
                elif weight >= 0.55:
                    weight = "🟨"
                else:
                    weight = "🟦"

                filt[y_i][x_i] = weight

        return filt
    

def findSpawn() -> tuple[int, int]:
    global load_x
    global load_y
     
    validSpawn = False
    while not validSpawn:
        p_x = random.randint(0, load_x)
        p_y = random.randint(0, load_y)
        if noise[p_y][p_x] in validSpawnTiles:
            validSpawn = True

    return p_x, p_y
    
tick_load = time.time()
noise = generateNoise(load_x, load_y, load_iterations)
tick_load_end = time.time()
print("loadtime: " + str(tick_load_end - tick_load))

p_x, p_y = findSpawn()
p_lx, p_lx = p_x, p_y
moveBuffer = []
inventory = []

base_inventoryRows = 4
base_inventoryColumns = 4

for i in base_inventoryRows * base_inventoryColumns:
    inventory.append([None, 0])

camera_pos_x = p_x
camera_pos_y = p_y

while time.time() - tick_load_end <= 1:
    pass

def display():
    global camera_range_x
    global camera_range_y
    global camera_pos_x
    global camera_pos_y
    global moveBuffer
    global p_x
    global p_y
    global p_lx
    global p_ly

    while True:
        for key in moveBuffer:
            if key == "w":
                p_y += 1
            elif key == "a":
                p_x -= 1
            elif key == "s":
                p_y -= 1
            elif key == "d":
                p_x += 1

            if not noise[p_y][p_x] in validSpawnTiles:
                p_x, p_y = p_lx, p_ly
            else:
                p_lx, p_ly = p_x, p_y
        moveBuffer = []

        camera_pos_x = round(p_x)
        camera_pos_y = round(p_y)


        display = ""

        for cam_iy in range(camera_range_y):
            for cam_ix in range(camera_range_x):
                xx = camera_pos_x + (cam_ix % camera_range_x) - math.floor(camera_range_x / 2)
                yy = camera_pos_y - cam_iy + math.floor(camera_range_y / 2)

                if xx == p_x and yy == p_y:
                    weight = "😄"
                elif xx >= 0 and xx <= (load_x - 1) and yy >= 0 and yy <= (load_y - 1):
                    weight = noise[yy][xx]
                else:
                    weight = "⬛"

                display += weight
                
            display += "\n"
        
        update_terminal(display)
        
        time.sleep(1/30)

def inputs():
    global camera_pos_x
    global camera_pos_y
    global p_x
    global p_y
    global moveBuffer

    while True:
        key = get_key()
        if key in "wasd":
            moveBuffer.append(key)

thread1 = threading.Thread(target=display)
thread2 = threading.Thread(target=inputs)

thread1.start()
thread2.start()
