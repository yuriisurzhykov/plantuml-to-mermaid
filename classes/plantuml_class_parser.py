import re
from core.diagram_model import ClassDiagram, ClassEntity, ClassRelationship
from core.diagram_parser import DiagramParser

class PlantUMLClassParser(DiagramParser):
    def parse(self, plantuml: str) -> ClassDiagram:
        # Убираем директивы @startuml и @enduml, а также пустые строки
        lines = [
            line.strip()
            for line in plantuml.splitlines()
            if line.strip() and not line.strip().startswith('@')
        ]
        entities = {}
        relationships = []
        i = 0

        # Регулярное выражение для отношений с карточными метками,
        # например: Customer "1" --> "0..*" Order : places
        card_assoc_re = re.compile(
            r'^(\w+)(?:\s+"([^"]+)")?\s+([o*\-\>]+)\s+(?:"([^"]+)"\s+)?(\w+)(?:\s*:\s*(.+))?$',
            re.IGNORECASE
        )
        # Регулярное выражение для реализации через стрелку, например:
        # Discountable <|.. PremiumCustomer
        impl_arrow_re = re.compile(
            r'^(\w+)\s+<\|..\s+(\w+)(?:\s*:\s*(.+))?$',
            re.IGNORECASE
        )
        
        while i < len(lines):
            line = lines[i]
            matched = False

            # 1. Блочное определение класса или интерфейса: "class MyClass {"
            m_block = re.match(r'^(class|interface)\s+(\w+)\s*\{$', line, re.IGNORECASE)
            if m_block:
                typ, name = m_block.groups()
                body_lines = []
                i += 1
                while i < len(lines) and lines[i] != '}':
                    body_lines.append(lines[i])
                    i += 1
                body = "\n".join(body_lines)
                entities[name] = ClassEntity(name=name, type=typ.lower(), body=body)
                matched = True
                i += 1  # пропускаем "}"
                continue

            # 2. Inline-объявление класса или интерфейса: "class MyClass"
            m_inline = re.match(r'^(class|interface)\s+(\w+)$', line, re.IGNORECASE)
            if m_inline:
                typ, name = m_inline.groups()
                entities[name] = ClassEntity(name=name, type=typ.lower(), body="")
                matched = True
                i += 1
                continue

            # 3. Отношения с карточными метками (если есть)
            m_card = card_assoc_re.match(line)
            if m_card:
                # Группы: 1: source, 2: source_cardinality (опционально),
                # 3: arrow, 4: target_cardinality (опционально),
                # 5: target, 6: label (опционально)
                source, source_card, arrow, target_card, target, label = m_card.groups()
                relationships.append(
                    ClassRelationship(
                        source=source,
                        target=target,
                        relation="association",
                        label=label or "",
                        source_cardinality=source_card or "",
                        target_cardinality=target_card or "",
                        arrow=arrow or ""
                    )
                )
                if source not in entities:
                    entities[source] = ClassEntity(name=source, type="class", body="")
                if target not in entities:
                    entities[target] = ClassEntity(name=target, type="class", body="")
                matched = True
                i += 1
                continue

            # 4. Наследование в формате стрелки: "Animal <|-- Duck"
            m_inh = re.match(r'^(\w+)\s+<\|--\s+(\w+)(?:\s*:\s*(.+))?$', line)
            if m_inh:
                parent, child, label = m_inh.groups()
                relationships.append(
                    ClassRelationship(
                        source=child,
                        target=parent,
                        relation="extends",
                        label=label or ""
                    )
                )
                if child not in entities:
                    entities[child] = ClassEntity(name=child, type="class", body="")
                if parent not in entities:
                    entities[parent] = ClassEntity(name=parent, type="class", body="")
                matched = True
                i += 1
                continue

            # 5. Реализация через стрелку: "Discountable <|.. PremiumCustomer"
            m_impl_arrow = impl_arrow_re.match(line)
            if m_impl_arrow:
                interface, impl_class, label = m_impl_arrow.groups()
                # В реализации интерфейса, класс реализует интерфейс,
                # поэтому source = impl_class, target = interface.
                relationships.append(
                    ClassRelationship(
                        source=impl_class,
                        target=interface,
                        relation="implements",
                        label=label or ""
                    )
                )
                if impl_class not in entities:
                    entities[impl_class] = ClassEntity(name=impl_class, type="class", body="")
                if interface not in entities:
                    entities[interface] = ClassEntity(name=interface, type="interface", body="")
                matched = True
                i += 1
                continue

            # 6. Отношения типа extends или implements (словесный формат),
            # например: "A extends B" или "A implements B"
            m_rel = re.match(r'^(\w+)\s+(extends|implements)\s+(\w+)(?:\s*:\s*(.+))?$', line, re.IGNORECASE)
            if m_rel:
                source, rel_type, target, label = m_rel.groups()
                relationships.append(
                    ClassRelationship(
                        source=source,
                        target=target,
                        relation=rel_type.lower(),
                        label=label or ""
                    )
                )
                if source not in entities:
                    entities[source] = ClassEntity(name=source, type="class", body="")
                if target not in entities:
                    entities[target] = ClassEntity(name=target, type="class", body="")
                matched = True
                i += 1
                continue

            # 7. Ассоциации без карточных меток: "A --> B : label"
            m_assoc = re.match(r'^(\w+)\s+-->\s+(\w+)(?:\s*:\s*(.+))?$', line)
            if m_assoc:
                source, target, label = m_assoc.groups()
                relationships.append(
                    ClassRelationship(
                        source=source,
                        target=target,
                        relation="association",
                        label=label or ""
                    )
                )
                if source not in entities:
                    entities[source] = ClassEntity(name=source, type="class", body="")
                if target not in entities:
                    entities[target] = ClassEntity(name=target, type="class", body="")
                matched = True
                i += 1
                continue

            # 8. Зависимости: "A ..> B : label"
            m_dep = re.match(r'^(\w+)\s+\.\.>\s+(\w+)(?:\s*:\s*(.+))?$', line)
            if m_dep:
                source, target, label = m_dep.groups()
                relationships.append(
                    ClassRelationship(
                        source=source,
                        target=target,
                        relation="dependency",
                        label=label or ""
                    )
                )
                if source not in entities:
                    entities[source] = ClassEntity(name=source, type="class", body="")
                if target not in entities:
                    entities[target] = ClassEntity(name=target, type="class", body="")
                matched = True
                i += 1
                continue

            if not matched:
                # Выводим для отладки строки, которые не распознаны
                print(f"Unparsed line: {line}")
            i += 1

        return ClassDiagram(entities=list(entities.values()), relationships=relationships)
