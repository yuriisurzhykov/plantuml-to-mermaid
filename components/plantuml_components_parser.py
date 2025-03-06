# plantuml_parser.py
import re
from core.diagram_model import Component, Edge, ComponentDiagram
from core.diagram_parser import DiagramParser

class PlantUMLComponentParser(DiagramParser):
    def parse(self, plantuml: str) -> ComponentDiagram:
        # Удаляем директивы @startuml/@enduml и пустые строки
        lines = [
            line.strip()
            for line in plantuml.splitlines()
            if line.strip() and not line.strip().startswith('@')
        ]
        
        components = {}
        edges = []
        
        # Шаблоны для парсинга
        comp_quoted_pattern = re.compile(r'^component\s+"([^"]+)"\s+as\s+(\w+)', re.IGNORECASE)
        comp_simple_pattern = re.compile(r'^component\s+(\w+)', re.IGNORECASE)
        # Поддержка стрелок --> и <--
        edge_pattern = re.compile(r'^(\w+)\s+((?:-->|<--))\s+(\w+)(?:\s*:\s*(.+))?$', re.IGNORECASE)
        
        for line in lines:
            # Парсим компонент с кавычками
            match = comp_quoted_pattern.match(line)
            if match:
                label, comp_id = match.groups()
                components[comp_id] = Component(id=comp_id, label=label)
                continue
            
            # Парсим простой компонент
            match = comp_simple_pattern.match(line)
            if match:
                comp_id = match.group(1)
                if comp_id not in components:
                    components[comp_id] = Component(id=comp_id, label=comp_id)
                continue
            
            # Парсим связь (edge)
            match = edge_pattern.match(line)
            if match:
                source, arrow, target, label = match.groups()
                # Если стрелка начинается с "<", меняем направление
                if arrow.startswith("<"):
                    source, target = target, source
                # Если компонент не объявлен, добавляем его с именем по умолчанию
                if source not in components:
                    components[source] = Component(id=source, label=source)
                if target not in components:
                    components[target] = Component(id=target, label=target)
                edges.append(Edge(source=source, target=target, label=label.strip() if label else None))
                continue
            
            # Остальные строки игнорируем
        return ComponentDiagram(components=list(components.values()), edges=edges)
