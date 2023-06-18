from enum import Enum


class Tabs(Enum):
    ENGINES = {
        "tab_name": "Engines",
        "prefix": "engine_",
        "precision_icon": 0.95,
        "precision_header": 0.95,
        "needs_be_on_world_map": True
    }
    ASSOCIATION = {
        "tab_name": "Association",
        "prefix": "association_",
        "precision_icon": 0.85,
        "precision_header": 0.95,
        "needs_be_on_world_map": True
    }
    LICENCES = {
        "tab_name": "Licences",
        "prefix": "licence_",
        "precision_icon": 0.70,
        "precision_header": 0.90,
        "needs_be_on_world_map": True
    }
    RANKINGS = {
        "tab_name": "Rankings",
        "prefix": "ranking_",
        "precision_icon": 0.85,
        "precision_header": 0.80,
        "needs_be_on_world_map": False
    }
    WORLD_MAP = {
        "tab_name": "World_map",
        "prefix": "world_map_",
        "precision_icon": 0.85,
        "precision_header": 0.80,
        "needs_be_on_world_map": False
    }

    @property
    def tab_name(self):
        return self.value["tab_name"]

    @property
    def prefix(self):
        return self.value["prefix"]

    @property
    def precision_icon(self):
        return self.value["precision_icon"]

    @property
    def precision_header(self):
        return self.value["precision_header"]

    @property
    def needs_be_on_world_map(self):
        return self.value["needs_be_on_world_map"]
