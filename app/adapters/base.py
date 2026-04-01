from abc import ABC, abstractmethod


class PlanningAdapter(ABC):
    source_name: str

    @abstractmethod
    def fetch(self) -> list[dict]:
        raise NotImplementedError


class RailAdapter(ABC):
    source_name: str

    @abstractmethod
    def fetch(self) -> list[dict]:
        raise NotImplementedError
