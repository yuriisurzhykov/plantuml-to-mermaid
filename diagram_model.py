# diagram_model.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Component:
    id: str
    label: str

@dataclass
class Edge:
    source: str
    target: str
    label: Optional[str] = None

@dataclass
class ComponentDiagram:
    components: List[Component]
    edges: List[Edge]