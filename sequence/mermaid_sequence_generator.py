# sequence/mermaid_sequence_generator.py

from core.sequence_model import (
    SequenceDiagram, Message, Activate, Deactivate, Note,
    AltBlock, LoopBlock, ParBlock
)
from core.diagram_generator import DiagramGenerator
from core.base_mermaid_generator import BaseMermaidGenerator

def escape_sequence_text(text: str) -> str:
    return BaseMermaidGenerator.escape_text(text)

def format_mermaid_name(name: str) -> str:
    return BaseMermaidGenerator.format_name(name)

def format_condition(text: str) -> str:
    return BaseMermaidGenerator.format_condition(text)

class MermaidSequenceGenerator(DiagramGenerator):
    def generate(self, diagram: SequenceDiagram) -> str:
        lines = ["sequenceDiagram"]

        # Выводим актёров
        for actor in diagram.actors:
            lines.append(f"actor {format_mermaid_name(actor.name)}")
        # Выводим участников
        for part in diagram.participants:
            lines.append(f"participant {format_mermaid_name(part.name)}")

        def process_events(events):
            out = []
            for ev in events:
                if isinstance(ev, Message):
                    msg = escape_sequence_text(ev.message)
                    out.append(f"{format_mermaid_name(ev.sender)}->>{format_mermaid_name(ev.receiver)}: {msg}")
                elif isinstance(ev, Activate):
                    out.append(f"activate {format_mermaid_name(ev.participant)}")
                elif isinstance(ev, Deactivate):
                    out.append(f"deactivate {format_mermaid_name(ev.participant)}")
                elif isinstance(ev, Note):
                    note_text = escape_sequence_text(ev.message)
                    if ev.participant:
                        out.append(f"Note over {format_mermaid_name(ev.participant)}: {note_text}")
                    else:
                        out.append(f"Note: {note_text}")
                elif isinstance(ev, AltBlock):
                    out.extend(process_alt_block(ev))
                elif isinstance(ev, LoopBlock):
                    out.append("loop " + format_condition(ev.condition))
                    out.extend(process_events(ev.events))
                    out.append("end")
                elif isinstance(ev, ParBlock):
                    first_label, first_branch = ev.branches[0]
                    out.append("par " + format_condition(first_label))
                    out.extend(process_events(first_branch))
                    for label, branch in ev.branches[1:]:
                        out.append("and " + format_condition(label))
                        out.extend(process_events(branch))
                    out.append("end")
            return out

        def process_alt_block(alt_block: AltBlock):
            out_alt = []
            first_cond, first_branch = alt_block.alternatives[0]
            out_alt.append("alt " + format_condition(first_cond))
            out_alt.extend(process_events(first_branch))
            for cond, branch in alt_block.alternatives[1:]:
                out_alt.append("else " + format_condition(cond))
                out_alt.extend(process_events(branch))
            out_alt.append("end")
            return out_alt

        raw_lines = process_events(diagram.events)
        filtered_lines = self.filter_deactivations(raw_lines)
        lines.extend(filtered_lines)
        return "\n".join(lines)

    def filter_deactivations(self, lines):
        active = {}
        result = []
        for line in lines:
            if line.startswith("activate "):
                part = line.split(" ", 1)[1]
                active[part] = True
                result.append(line)
            elif line.startswith("deactivate "):
                part = line.split(" ", 1)[1]
                if active.get(part, False):
                    result.append(line)
                    active[part] = False
                else:
                    continue
            else:
                result.append(line)
        return result
