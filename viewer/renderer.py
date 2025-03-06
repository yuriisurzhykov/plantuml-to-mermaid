from abc import ABC, abstractmethod

class DiagramRenderer(ABC):
    @abstractmethod
    def render(self, code: str, height: int):
        """Render a diagram using the provided code and height."""
        pass
