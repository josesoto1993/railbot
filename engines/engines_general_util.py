import logging
import os
import random
import time

from rail_utils.rail_utils import image_on_screen, click_on_rect_area, get_image_size, wait_rail_response

logging.basicConfig(level=logging.INFO)

RETRIES_TO_LOAD = 5


def open_engines_tab():
    prefix = 'engine_'
    tab_state = find_tab_state(prefix, precision=0.95)

    on_screen_tabs = [item for item in tab_state if item[1]]
    if not on_screen_tabs:
        raise Exception("Engine Tab not found.")
    else:
        click_tab_if_needed(on_screen_tabs)
        wait_engine_tab_open()


def click_tab_if_needed(on_screen_tabs):
    base_images = [item for item in on_screen_tabs if "_base" in item[0]]
    if base_images:
        click_on_tab(base_images[0])
    else:
        logging.info("Engine Tab is already opened. Open another wait then open")
        # TODO: check the open another as its not checking, just click licence
        click_on_rect_area(top_left_corner=(880, 970), size=(40, 40))
        time.sleep(random.uniform(20, 30))
        selected_images = [item for item in on_screen_tabs if "_selected" in item[0]]
        click_on_tab(selected_images[0])
        # ENDTODO


def click_on_tab(base_image):
    start_position = base_image[2]
    image_path = base_image[0]
    image_width, image_height = get_image_size(image_path)
    size = (image_width, image_height)
    click_on_rect_area(top_left_corner=start_position, size=size)


def find_tab_state(prefix, precision=0.95):
    tab_dir = 'data/tabs_status'
    tab_state = []
    for file_name in os.listdir(tab_dir):
        if file_name.startswith(prefix) and file_name.endswith('.png'):
            file_path = os.path.join(tab_dir, file_name)
            is_on_screen, position = image_on_screen(file_path, precision=precision)
            tab_state.append([file_path, is_on_screen, position])
            log_find_tab_state(file_name, is_on_screen, position)

    on_screen_images = len([item for item in tab_state if item[1]])
    if on_screen_images > 1:
        logging.warning(f"Found {on_screen_images} engine images, expected 1 or 0.")

    return tab_state


def log_find_tab_state(file_name, is_on_screen, position):
    logmsg = f"Image: {file_name} | Is on screen? {is_on_screen}"
    if is_on_screen:
        logmsg += f"Position: {position}"
    logging.info(logmsg)


def wait_engine_tab_open():
    for _ in range(RETRIES_TO_LOAD):
        wait_rail_response()
        if check_finish_load_engine_tab():
            logging.info("Tab opened")
            return
    raise Exception("Engine Tab not opened.")


def check_finish_load_engine_tab():
    on_screen, _ = image_on_screen("data/tab_engine/tab_header_engine.png", precision=0.95)
    return on_screen
