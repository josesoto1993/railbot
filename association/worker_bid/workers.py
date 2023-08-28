import os

from association.worker_bid.worker_price_data import get_worker_preferences
from rail_utils.rail_utils import get_folder_paths_from_folder

WORKER_ACCELERATION = "worker_acceleration"
WORKER_BUILD_DISCOUNT = "worker_build_discount"
WORKER_CITY_CONNECTOR = "worker_city_connector"
WORKER_COMPETITION = "worker_competition"
WORKER_FASTER_BONUS = "worker_faster_bonus"
WORKER_FASTER_CONSTRUCTION = "worker_faster_construction"
WORKER_GOLD_DISCOUNT = "worker_gold_discount"
WORKER_PAX = "worker_pax"
WORKER_PRESIDENT = "worker_president"
WORKER_PRESTIGE_HOURLY = "worker_prestige_hourly"
WORKER_PRESTIGE_INDUSTRY = "worker_prestige_industry"
WORKER_REDUCE_WT = "worker_reduce_wt"
WORKER_SCIENCE = "worker_science"
WORKER_SERVICE_DISCOUNT = "worker_service_discount"
WORKER_SPEED = "worker_speed"
WORKER_TRACK_DISCOUNT = "worker_track_discount"
WORKER_WAGGONS_DISCOUNT = "worker_waggons_discount"

WORKER_MAIN_FOLDER = "data/workers"


def get_worker_data() -> list[tuple[str, int]]:
    folders = get_folder_paths_from_folder(WORKER_MAIN_FOLDER)

    preferences = get_worker_preferences()

    print("Preferences:", preferences)

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
