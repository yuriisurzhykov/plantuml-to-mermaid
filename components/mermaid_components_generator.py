# mermaid_generator.py
from core.diagram_model import ComponentDiagram
from core.base_mermaid_generator import BaseMermaidGenerator

class MermaidGenerator(BaseMermaidGenerator):
    def generate(self, diagram: ComponentDiagram) -> str:
        lines = ["flowchart LR"]
        # Определения компонентов: экранируем метку через BaseMermaidGenerator.escape_text
        for comp in diagram.components:
            safe_label = self.escape_text(comp.label)
            lines.append(f'{comp.id}["{safe_label}"]')
        # Определения связей: экранируем метки через BaseMermaidGenerator.escape_text
        for edge in diagram.edges:
            if edge.label:
                safe_edge_label = self.escape_text(edge.label)
                lines.append(f'{edge.source} -->|{safe_edge_label}| {edge.target}')
            else:
                lines.append(f'{edge.source} --> {edge.target}')
        return "\n".join(lines)
