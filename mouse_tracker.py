import logging
import time

import pyautogui

logging.basicConfig(level=logging.INFO)


def main():
    while True:
        mouse_position = pyautogui.position()
        logging.info(f"Mouse position: X={mouse_position[0]}, Y={mouse_position[1]}")
        time.sleep(1)


if __name__ == "__main__":
    main()
