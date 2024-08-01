COMPREHENSIVE USER ACTIVITY LOGGER

OVERVIEW:
This Python script is designed to monitor and log various aspects of user activity on a Windows machine. The tool provides detailed insights by capturing keystrokes, mouse movements, and clicks, taking periodic screenshots, logging application activity, and capturing user images via webcam. It is particularly useful for creating detailed activity logs for security, analysis, or debugging purposes.

FEATURES:
->Keystroke Logging: Captures and logs all typed characters. It can trigger actions, such as locking the workstation, based on predefined strings.
->Mouse Tracking: Logs mouse movements and click events with timestamps.
->Periodic Screenshots: Takes screenshots of the entire screen at regular intervals to monitor visual activity.
->Application Activity Logging: Records active application windows and their titles every few seconds.
->User Image Capture: Periodically takes pictures using the webcam to capture the user's presence.

REQUIREMENTS:
Python 3.x
Libraries: pynput, Pillow (PIL), psutil, pygetwindow, opencv-python, ctypes
