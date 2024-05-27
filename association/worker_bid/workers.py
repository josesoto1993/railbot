import os

from association.worker_bid.worker_price_data import get_worker_preferences
from rail_utils.folders_paths import WORKER_MAIN_FOLDER
from rail_utils.rail_utils import get_folder_paths_from_folder


def get_worker_data() -> list[tuple[str, int]]:
    folders = get_folder_paths_from_folder(WORKER_MAIN_FOLDER)
    preferences = get_worker_preferences()

    return [(os.path.join(root, file), get_price(folder, preferences))
            for folder in folders
            for root, _, files in os.walk(folder)
            for file in files
            if file.lower().endswith('.png')
            ]


def get_all_worker_folders():
    _, folders, _ = next(os.walk(WORKER_MAIN_FOLDER))
    return folders


def get_price(folder: str, preferences: list[tuple[str, int]]) -> int:
    folder_name = os.path.basename(folder)
    matching_values = [value
                       for (name, value) in preferences
                       if name == folder_name]
    return matching_values[0] if matching_values else 0
