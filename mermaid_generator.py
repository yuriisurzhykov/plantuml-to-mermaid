# mermaid_generator.py
from diagram_model import ComponentDiagram

class MermaidGenerator:
    def generate(self, diagram: ComponentDiagram) -> str:
        lines = ["flowchart LR"]
        # Добавляем определения компонентов (узлов)
        for comp in diagram.components:
            # Заменяем последовательность "\n" и реальные переводы строк на <br>
            safe_label = comp.label.replace("\\n", "<br>").replace("\n", "<br>")
            lines.append(f'{comp.id}["{safe_label}"]')
        # Добавляем связи между компонентами
        for edge in diagram.edges:
            if edge.label:
                safe_edge_label = edge.label.replace("\\n", "<br>").replace("\n", "<br>")
                # Экранируем круглые скобки
                safe_edge_label = safe_edge_label.replace("(", "&#40;").replace(")", "&#41;")
                lines.append(f'{edge.source} -->|{safe_edge_label}| {edge.target}')
            else:
                lines.append(f'{edge.source} --> {edge.target}')
        return "\n".join(lines)
