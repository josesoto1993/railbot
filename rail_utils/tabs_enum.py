from dataclasses import dataclass
from enum import Enum


@dataclass
class Tab:
    name: str
    prefix: str
    needs_be_on_world_map: bool


class Tabs(Enum):
    ENGINES = Tab(
        name="Engines",
        prefix="engine_",
        needs_be_on_world_map=True
    )
    ASSOCIATION = Tab(
        name="Association",
        prefix="association_",
        needs_be_on_world_map=True
    )
    LICENCES = Tab(
        name="Licences",
        prefix="licence_",
        needs_be_on_world_map=True
    )
    RANKINGS = Tab(
        name="Rankings",
        prefix="ranking_",
        needs_be_on_world_map=False
    )
    MEDALS = Tab(
        name="Medals",
        prefix="medals_",
        needs_be_on_world_map=True
    )
    WORLD_MAP = Tab(
        name="World_map",
        prefix="world_map_",
        needs_be_on_world_map=False
    )
