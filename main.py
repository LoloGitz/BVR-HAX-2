import logic
import utils._display as _display

import time
import threading

overworld = logic.Game("overworld", 250, 250, 4)

tick_load = time.time()
overworld.generate_map()
s_x, s_y, _ = overworld.findSpawn()
player = logic.Entity("😏", s_x, s_y, overworld)
logic.camera_pos_x = s_x
logic.camera_pos_y = s_y
tick_load_end = time.time()
print("loadtime: " + str(tick_load_end - tick_load))

# player.destroy()

while time.time() - tick_load_end <= 1:
    pass

def runDisplay():
    while True:
        display = overworld.display()
        _display.update_terminal(display)
        
        time.sleep(1/30)

runDisplay_thread = threading.Thread(target=runDisplay)

runDisplay_thread.start()

# keyBuffer = []

# def initalizeInventory(i):
#     if not i in inventory:
#         inventory[i] = ["🚫", 0]

# def getInventoryDisplay(i: int) -> Optional[str]:
#     if not i in inventory:
#         return None
    
#     if gameState == "game":
#         select_i = hotbar_i
#     else:
#         select_i = inv_i
    
#     slot = inventory[i]
#     slot_display = ""
                
#     item = slot[0]
#     amount = slot[1]
#     if item == None:
#         item = ""
#     if amount <= 9:
#         amount = f"0{amount}"
    
#     slot_display = f"[{item} x{amount}]"
#     if select_i == i:
#         slot_display = f"{GREEN}{slot_display}{RESET}"
#     elif i < inventory_rows:
#         slot_display = f"{MAGENTA}{slot_display}{RESET}"

#     return slot_display

# inventory = {}
# inventory_slots = 15
# inventory_rows = 5
# for i in range(inventory_slots):
#     initalizeInventory(i)



# def runLogic():
#     global keyBuffer
#     global gameState
#     global inventory
#     global inventory_rows
#     global inventory_slots
#     global p_x
#     global p_y
#     global p_lx
#     global p_ly
#     global inv_i
#     global hotbar_i

#     newBuffer = []
#     for key in keyBuffer:
#         key_num = tonumber(key)

#         if key == "w":
#             if gameState == "game":
#                 p_y += 1
#             elif gameState == "inventory":
#                 inv_i -= inventory_rows
#         elif key == "a":
#             if gameState == "game":
#                 p_x -= 1
#             elif gameState == "inventory":
#         elif key == "s":
#             p_y -= 1
#         elif key == "d":
#             p_x += 1
#         elif key_num and key_num <= inventory_rows and key_num >= 1:
#             hotbar_i = key_num - 1
#         elif key == "e":
#             gameState = "inventory"
#         else:
#             newBuffer.append(key)

#         if not overworld[p_y][p_x] in validSpawnTiles:
#             p_x, p_y = p_lx, p_ly
#         else:
#             p_lx, p_ly = p_x, p_y

#     camera_pos_x = round(p_x)
#     camera_pos_y = round(p_y)

#     keyBuffer = newBuffer

#      for key in keyBuffer:
#         inv_mod = inv_i % inventory_rows
#         if key == "w":
#             inv_i -= inventory_rows
#         elif key == "s":
#             inv_i += inventory_rows
#         elif key == "a" and inv_mod > 0:
#             inv_i -= 1
#             keyBuffer.pop()
#         elif key == "d" and inv_mod < 3:
#             inv_i += 1
#         else:
#             newBuffer.append(key)
#     inv_i = max(0, min(inv_i, inventory_slots - 1))

# def runInputs():
#     global keyBuffer
#     while True:
#         key = get_key()
#         keyBuffer.append(key)


# thread2 = threading.Thread(target=runInputs)


# thread2.start()
