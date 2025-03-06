from abc import ABC, abstractmethod

class DiagramGenerator(ABC):
    @abstractmethod
    def generate(self, diagram) -> str:
        pass
