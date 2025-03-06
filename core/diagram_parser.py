# diagram_parser.py
from abc import ABC, abstractmethod

class DiagramParser(ABC):
    @abstractmethod
    def parse(self, plantuml: str):
        pass
