import glob
import logging
import os

from rail_utils.rail_utils import image_on_screen, wait_rail_response, get_screenshot, click_on_rect_area, \
    get_image_size, move_mouse_close_to_top_right, any_image_on_screen, close_all_pop_ups, ERROR_FOLDER
from rail_utils.tabs_enum import Tab, Tabs

BASE_REGEX = "_base"

SELECTED_REGEX = "_selected"

DEFAULT_IMG_SUFFIX = '.png'

TAB_STATUS_DIR = 'data/tabs_status'

logging.basicConfig(level=logging.INFO)

RETRIES_TO_LOAD_TAB = 5


def open_tab(tab_enum: Tab):
    logging.debug(f"try oppen tab: {tab_enum.name}")
    _prepare_screen(tab_enum)

    tabs_state = _find_tab_state(tab_enum)
    on_screen_tabs = [tab_state for tab_state in tabs_state if tab_state[1]]

    if not on_screen_tabs:
        get_screenshot(save=True, filename=f"{ERROR_FOLDER}/{tab_enum.name}_not_found")
        raise TabNotFoundException(f"{tab_enum.name} tab not found.")
    else:
        _open_or_reopen_tab(on_screen_tabs=on_screen_tabs, tab_enum=tab_enum)
        _check_if_tab_open(tab_enum)


def _prepare_screen(tab_enum: Tab):
    logging.debug("_prepare_screen")
    _open_world_map_if_needed(tab_enum)
    close_all_pop_ups()
    move_mouse_close_to_top_right()
    wait_rail_response()


def _open_world_map_if_needed(tab_enum: Tab):
    logging.debug("_open_world_map_if_needed")
    logging.debug(f"needs_be_on_world_map? {tab_enum.needs_be_on_world_map}")
    if tab_enum.needs_be_on_world_map:
        is_on_world_map = _is_tab_selected(Tabs.WORLD_MAP.value)
        logging.debug(f"is_on_world_map? {is_on_world_map}")
        if not is_on_world_map:
            open_tab(Tabs.WORLD_MAP.value)


def _is_tab_selected(tab_enum: Tab):
    logging.debug(f"_is_tab_selected? {tab_enum.name}")
    screenshot = get_screenshot()
    for file_name in os.listdir(TAB_STATUS_DIR):
        if file_name.startswith(tab_enum.prefix) and (SELECTED_REGEX in file_name):
            file_path = os.path.join(TAB_STATUS_DIR, file_name)
            is_on_screen, _, _ = image_on_screen(
                file_path,
                screenshot=screenshot)
            if is_on_screen:
                logging.debug(f"_is_tab_selected ({tab_enum.name})? {True}")
                return True
    logging.debug(f"_is_tab_selected ({tab_enum.name})? {False}")
    return False


def _open_or_reopen_tab(on_screen_tabs, tab_enum: Tab):
    logging.debug(f"_open_or_reopen_tab: {tab_enum.name}")
    base_images = [tab for tab in on_screen_tabs if BASE_REGEX in tab[0]]
    if base_images:
        _click_on_tab(base_images[0])
    else:
        _reopen_tab(on_screen_tabs, tab_enum)


def _reopen_tab(on_screen_tabs, tab_enum: Tab):
    logging.debug("_reopen_tab")
    if tab_enum != Tabs.WORLD_MAP.value:
        logging.debug(f"{tab_enum.name} tab is already opened, open another then open.")
        _open_another(tab_enum)
        selected_images = [item for item in on_screen_tabs if SELECTED_REGEX in item[0]]
        _click_on_tab(selected_images[0])


def _click_on_tab(image_on_screen_data):
    logging.debug("_click_on_tab")
    start_position = image_on_screen_data[2]
    image_path = image_on_screen_data[0]
    click_on_rect_area(top_left_corner=start_position, size=get_image_size(image_path))


def _open_another(tab_enum: Tab):
    if tab_enum != Tabs.LICENCES.value:
        open_tab(Tabs.LICENCES.value)
    else:
        open_tab(Tabs.ENGINES.value)


def _find_tab_state(tab_enum: Tab) -> list[list[str | bool | tuple[int, int] | None]]:
    logging.debug(f"_find_tab_state for: {tab_enum.name}")
    tabs_state = []
    screenshot = get_screenshot()
    for file_name in os.listdir(TAB_STATUS_DIR):
        if file_name.startswith(tab_enum.prefix) and (BASE_REGEX in file_name or SELECTED_REGEX in file_name):
            file_path = os.path.join(TAB_STATUS_DIR, file_name)
            is_on_screen, position, _ = image_on_screen(file_path,
                                                        screenshot=screenshot)
            _log_find_tab_state(file_name, is_on_screen, position)
            tabs_state.append([file_path, is_on_screen, position])
    return tabs_state


def _log_find_tab_state(file_name, is_on_screen, position):
    log_msg = f"Image: {file_name} | Is on screen? {is_on_screen}"
    if is_on_screen:
        log_msg += f" | Position: {position}"
    logging.debug(log_msg)


def _check_if_tab_open(tab_enum: Tab):
    logging.debug(f"_check_if_tab_open: {tab_enum.name}")
    for _ in range(RETRIES_TO_LOAD_TAB):
        wait_rail_response()

        partial_path = os.path.join(TAB_STATUS_DIR, tab_enum.prefix + "on_load")
        tab_on_load_files = glob.glob(partial_path + "*.png")

        on_screen, _, _, _ = any_image_on_screen(tab_on_load_files)
        if on_screen:
            logging.debug(f"Tab {tab_enum.name} opened")
            return

    get_screenshot(save=True, filename=f"{ERROR_FOLDER}/{tab_enum.name}_not_found")
    raise TabNotFoundException(f"{tab_enum.name} tab not opened.")


class TabNotFoundException(Exception):
    pass
