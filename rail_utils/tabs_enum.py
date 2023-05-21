from enum import Enum


class Tabs(Enum):
    ENGINES = {
        "tab_name": "Engines",
        "prefix": "engine_",
        "on_load_image_path": "data/tabs_status/engine_on_load.png",
        "precision_icon": 0.95,
        "precision_header": 0.95
    }
    ASSOCIATION = {
        "tab_name": "Association",
        "prefix": "association_",
        "on_load_image_path": "data/tabs_status/association_on_load.png",
        "precision_icon": 0.95,
        "precision_header": 0.95
    }
    LICENCES = {
        "tab_name": "Licences",
        "prefix": "licence_",
        "on_load_image_path": "data/tabs_status/licence_on_load.png",
        "precision_icon": 0.95,
        "precision_header": 0.95
    }

    @property
    def tab_name(self):
        return self.value["tab_name"]

    @property
    def prefix(self):
        return self.value["prefix"]

    @property
    def on_load_image_path(self):
        return self.value["on_load_image_path"]

    @property
    def precision_icon(self):
        return self.value["precision_icon"]

    @property
    def precision_header(self):
        return self.value["precision_header"]
