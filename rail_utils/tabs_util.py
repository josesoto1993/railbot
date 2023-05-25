import logging
import os

from rail_utils.rail_utils import image_on_screen, wait_rail_response, get_screenshot, click_on_rect_area, \
    get_image_size, move_mouse_to_center
from rail_utils.tabs_enum import Tabs

BASE_REGEX = "_base"

SELECTED_REGEX = "_selected"

DEFAULT_IMG_SUFFIX = '.png'

TAB_STATUS_DIR = 'data/tabs_status'

logging.basicConfig(level=logging.INFO)

RETRIES_TO_LOAD = 5


def open_tab(tab_enum):
    _prepare_screen()

    tabs_state = _find_tab_state(tab_enum)
    on_screen_tabs = [tab_state for tab_state in tabs_state if tab_state[1]]

    if not on_screen_tabs:
        tab_name = tab_enum.tab_name
        raise Exception(f"{tab_name} tab not found.")
    else:
        _open_or_reopen_tab(on_screen_tabs=on_screen_tabs, tab_enum=tab_enum)
        _check_if_tab_open(tab_enum)


def _prepare_screen():
    move_mouse_to_center()
    wait_rail_response()


def _open_or_reopen_tab(on_screen_tabs, tab_enum):
    base_images = [tab for tab in on_screen_tabs if BASE_REGEX in tab[0]]
    if base_images:
        _click_on_tab(base_images[0])
    else:
        logging.info(f"{tab_enum.tab_name} tab is already opened, open another then open.")
        _open_another(tab_enum)
        selected_images = [item for item in on_screen_tabs if SELECTED_REGEX in item[0]]
        _click_on_tab(selected_images[0])


def _click_on_tab(image_on_screen_data):
    start_position = image_on_screen_data[2]
    image_path = image_on_screen_data[0]
    click_on_rect_area(top_left_corner=start_position, size=get_image_size(image_path))


def _open_another(tab_enum):
    if tab_enum != Tabs.LICENCES:
        open_tab(Tabs.LICENCES)
    else:
        open_tab(Tabs.ENGINES)


def _find_tab_state(tab_enum):
    tabs_state = []
    screenshot = get_screenshot()
    for file_name in os.listdir(TAB_STATUS_DIR):
        if file_name.startswith(tab_enum.prefix) and (BASE_REGEX in file_name or SELECTED_REGEX in file_name):
            file_path = os.path.join(TAB_STATUS_DIR, file_name)
            is_on_screen, position = image_on_screen(file_path, precision=tab_enum.precision_icon,
                                                     screenshot=screenshot)
            _log_find_tab_state(file_name, is_on_screen, position)
            tabs_state.append([file_path, is_on_screen, position])

    on_screen_images = len([tab_state for tab_state in tabs_state if tab_state[1]])
    if on_screen_images > 1:
        logging.warning(f"Found {on_screen_images} images, expected 1 or 0.")

    return tabs_state


def _log_find_tab_state(file_name, is_on_screen, position):
    log_msg = f"Image: {file_name} | Is on screen? {is_on_screen}"
    if is_on_screen:
        log_msg += f" | Position: {position}"
    logging.debug(log_msg)


def _check_if_tab_open(tab_enum):
    for _ in range(RETRIES_TO_LOAD):
        wait_rail_response()
        on_screen, _ = image_on_screen(tab_enum.on_load_image_path, precision=tab_enum.precision_header)
        if on_screen:
            logging.info(f"Tab {tab_enum.tab_name} opened")
            return
    raise Exception(f"{tab_enum.tab_name} tab not opened.")
