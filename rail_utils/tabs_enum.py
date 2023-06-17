from enum import Enum


class Tabs(Enum):
    ENGINES = {
        "tab_name": "Engines",
        "prefix": "engine_",
        "precision_icon": 0.95,
        "precision_header": 0.95
    }
    ASSOCIATION = {
        "tab_name": "Association",
        "prefix": "association_",
        "precision_icon": 0.85,
        "precision_header": 0.95
    }
    LICENCES = {
        "tab_name": "Licences",
        "prefix": "licence_",
        "precision_icon": 0.70,
        "precision_header": 0.95
    }
    RANKINGS = {
        "tab_name": "Rankings",
        "prefix": "ranking_",
        "precision_icon": 0.85,
        "precision_header": 0.80
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
