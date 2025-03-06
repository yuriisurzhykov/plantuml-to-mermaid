# mermaid_class_generator.py
from core.diagram_model import ClassDiagram
from core.base_mermaid_generator import BaseMermaidGenerator
import re

def process_body_line(line: str) -> str:
    """
    Обрабатывает строку тела класса или интерфейса.
    Убирает ключевое слово 'fun' после модификатора видимости,
    а также удаляет лишнее двоеточие после закрывающей скобки, если оно присутствует.
    """
    line = line.strip()
    processed = re.sub(r'^([+-])\s*fun\s+', r'\1 ', line)
    processed = re.sub(r"\)\s*:", ")", processed)
    return processed

class MermaidClassGenerator(BaseMermaidGenerator):
    def generate(self, diagram: ClassDiagram) -> str:
        lines = ["classDiagram"]
        # Обрабатываем отношения между классами
        for rel in diagram.relationships:
            relation_type = rel.relation.lower().strip()
            safe_label = (self.escape_text(rel.label.strip())
                          if rel.label and rel.label.strip() else "")
            # Если заданы карточные метки – выводим строку с ними
            if rel.source_cardinality or rel.target_cardinality:
                if safe_label:
                    lines.append(f'{rel.source} "{rel.source_cardinality}" {rel.arrow} "{rel.target_cardinality}" {rel.target} : {safe_label}')
                else:
                    lines.append(f'{rel.source} "{rel.source_cardinality}" {rel.arrow} "{rel.target_cardinality}" {rel.target}')
            else:
                if relation_type == "extends":
                    lines.append(f"{rel.target} <|-- {rel.source}")
                elif relation_type == "implements":
                    lines.append(f"{rel.target} <|.. {rel.source}")
                elif relation_type == "aggregation":
                    if safe_label:
                        lines.append(f"{rel.source} o-- {rel.target} : {safe_label}")
                    else:
                        lines.append(f"{rel.source} o-- {rel.target}")
                elif relation_type == "composition":
                    if safe_label:
                        lines.append(f"{rel.source} *-- {rel.target} : {safe_label}")
                    else:
                        lines.append(f"{rel.source} *-- {rel.target}")
                elif relation_type == "dependency":
                    if safe_label:
                        lines.append(f"{rel.source} ..> {rel.target} : {safe_label}")
                    else:
                        lines.append(f"{rel.source} ..> {rel.target}")
                elif relation_type == "association":
                    if safe_label:
                        lines.append(f"{rel.source} --> {rel.target} : {safe_label}")
                    else:
                        lines.append(f"{rel.source} --> {rel.target}")
                else:
                    if safe_label:
                        lines.append(f"{rel.source} --> {rel.target} : {safe_label}")
                    else:
                        lines.append(f"{rel.source} --> {rel.target}")
        # Обрабатываем определения классов и интерфейсов
        for ent in diagram.entities:
            if ent.type.lower() == "interface":
                if ent.body:
                    lines.append(f"class {ent.name} {{")
                    lines.append("    <<interface>>")
                    for body_line in ent.body.splitlines():
                        processed_line = process_body_line(body_line)
                        lines.append(f"    {processed_line}")
                    lines.append("}")
                else:
                    lines.append(f"class {ent.name} <<interface>>")
            else:
                if ent.body:
                    lines.append(f"class {ent.name} {{")
                    for body_line in ent.body.splitlines():
                        processed_line = process_body_line(body_line)
                        lines.append(f"    {processed_line}")
                    lines.append("}")
                else:
                    lines.append(f"class {ent.name}")
        return "\n".join(lines)
