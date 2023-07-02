import datetime
from abc import ABC, abstractmethod
from typing import Optional


class RailRunnable(ABC):

    @abstractmethod
    def run(self) -> Optional[datetime]:
        pass
