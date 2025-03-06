# mermaid_generator.py
from diagram_model import ComponentDiagram
from diagram_generator import DiagramGenerator

class MermaidGenerator(DiagramGenerator):
    def generate(self, diagram: ComponentDiagram) -> str:
        lines = ["flowchart LR"]
        # Определения компонентов: заменяем последовательности "\n" и реальные переводы строк на <br>
        for comp in diagram.components:
            safe_label = comp.label.replace("\\n", "<br>").replace("\n", "<br>")
            lines.append(f'{comp.id}["{safe_label}"]')
        # Определения связей: экранируем скобки в метках
        for edge in diagram.edges:
            if edge.label:
                safe_edge_label = edge.label.replace("\\n", "<br>").replace("\n", "<br>")
                safe_edge_label = safe_edge_label.replace("(", "#40;").replace(")", "#41;")
                lines.append(f'{edge.source} -->|{safe_edge_label}| {edge.target}')
            else:
                lines.append(f'{edge.source} --> {edge.target}')
        return "\n".join(lines)
