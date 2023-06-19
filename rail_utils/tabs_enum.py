from dataclasses import dataclass
from enum import Enum


@dataclass
class Tab:
    name: str
    prefix: str
    precision_icon: float
    precision_header: float
    needs_be_on_world_map: bool


class Tabs(Enum):
    ENGINES = Tab(
        name="Engines",
        prefix="engine_",
        precision_icon=0.95,
        precision_header=0.95,
        needs_be_on_world_map=True
    )
    ASSOCIATION = Tab(
        name="Association",
        prefix="association_",
        precision_icon=0.80,
        precision_header=0.95,
        needs_be_on_world_map=True
    )
    LICENCES = Tab(
        name="Licences",
        prefix="licence_",
        precision_icon=0.70,
        precision_header=0.90,
        needs_be_on_world_map=True
    )
    RANKINGS = Tab(
        name="Rankings",
        prefix="ranking_",
        precision_icon=0.85,
        precision_header=0.80,
        needs_be_on_world_map=False
    )
    MEDALS = Tab(
        name="Medals",
        prefix="medals_",
        precision_icon=0.85,
        precision_header=0.95,
        needs_be_on_world_map=True
    )
    WORLD_MAP = Tab(
        name="World_map",
        prefix="world_map_",
        precision_icon=0.85,
        precision_header=0.80,
        needs_be_on_world_map=False
    )
