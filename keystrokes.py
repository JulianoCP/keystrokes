import ctypes, time, random, keyboard

LPINPUT  = ctypes.POINTER(ctypes.c_ulong)

class KEYBDINPUT(ctypes.Structure): 
    _fields_ = [
                ("wVk", ctypes.c_ushort), 
                ("wScan", ctypes.c_ushort), 
                ("dwFlags", ctypes.c_ulong), 
                ("time", ctypes.c_ulong), 
                ("dwExtraInfo", LPINPUT)
            ]

class HARDWAREINPUT(ctypes.Structure): 
    _fields_ = [
                ("uMsg", ctypes.c_ulong), 
                ("wParamL", ctypes.c_short), 
                ("wParamH", ctypes.c_ushort)
            ]

class MOUSEINPUT(ctypes.Structure): 
    _fields_ = [
                ("dx", ctypes.c_long), 
                ("dy", ctypes.c_long), 
                ("mouseData", ctypes.c_ulong), 
                ("dwFlags", ctypes.c_ulong), 
                ("time", ctypes.c_ulong), 
                ("dwExtraInfo", LPINPUT)
            ]

class INPUT_I(ctypes.Union): 
    _fields_ = [
                ("ki", KEYBDINPUT), 
                ("mi", MOUSEINPUT), 
                ("hi", HARDWAREINPUT)
            ]

class INPUT(ctypes.Structure): 
    _fields_ = [
                ("type", ctypes.c_ulong), 
                ("ii", INPUT_I)
            ]

class Game:
    def __init__ (self):
        self._handle = None
        self.map_keys = {
            'q': 0x10, 'w': 0x11, 'e': 0x12, 'r': 0x13, 't': 0x14, 'z': 0x15, 'u': 0x16, 'i': 0x17, 'o': 0x18,
            'a': 0x1E, 's': 0x1F, 'd': 0x20, 'f': 0x21, 'g': 0x22, 'h': 0x23, 'j': 0x24, 'k': 0x25, 'l': 0x26,
            'y': 0x2C, 'x': 0x2D, 'c': 0x2E, 'v': 0x2F, 'b': 0x30, 'n': 0x31, 'm': 0x32, 'p':0x19 , 
        }

    def press_key(self, key):
        input_int = ctypes.c_ulong(0); ii_ = INPUT_I(); flags = 0x0008
        ii_.ki = KEYBDINPUT(0, self.map_keys[key], flags, 0, ctypes.pointer(input_int))
        input_type = INPUT(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(input_type), ctypes.sizeof(input_type))

    def release_key(self, key):
        input_int = ctypes.c_ulong(0); ii_ = INPUT_I(); flags = 0x0008 | 0x0002
        ii_.ki = KEYBDINPUT(0, self.map_keys[key], flags, 0, ctypes.pointer(input_int))
        input_type = INPUT(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(input_type), ctypes.sizeof(input_type))

def main():

    GAME = Game()
    start_attack = False

    print("All set to start repeating a key\n")
    option = input("Which key would you like to repeat: ")

    while(option not in GAME.map_keys):
        print("\nWhoops this key is invalid, try again")
        option = input("Which key would you like to repeat: ")

    print("\n+------------------------------------------------------------------+")
    print(" All set, turn on / off keep the KEY_ENTER pressed inside the game. ")
    print("+------------------------------------------------------------------+")
    
    while(True):
        if keyboard.is_pressed("ENTER"):
            if start_attack: start_attack = False
            else: start_attack = True

        if start_attack:
           GAME.press_key(option.lower()); 
           time.sleep(random.uniform(0.05, 0.1))
           GAME.release_key(option.lower())
           time.sleep(random.uniform(0.1, 0.2))
        else: time.sleep(1)

if __name__ == '__main__': 
    main() 