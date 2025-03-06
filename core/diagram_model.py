from dataclasses import dataclass
from typing import List, Optional

# Модель для components diagram (оставляем без изменений)
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

# Модель для классовой диаграммы
@dataclass
class ClassRelationship:
    source: str
    target: str
    relation: str  # "extends", "implements", "association", "dependency", etc.
    label: Optional[str] = ""
    source_cardinality: Optional[str] = ""
    target_cardinality: Optional[str] = ""
    arrow: Optional[str] = ""  # Новый параметр для хранения типа стрелки (например, "-->" или "o--")

@dataclass
class ClassEntity:
    name: str
    type: str  # "class" или "interface"
    body: str = ""

@dataclass
class ClassDiagram:
    entities: List[ClassEntity]
    relationships: List[ClassRelationship]
