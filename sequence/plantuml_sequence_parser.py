import re
from core.sequence_model import (
    SequenceDiagram, Participant, Actor, Message,
    Activate, Deactivate, Note, AltBlock, LoopBlock, ParBlock
)
from core.diagram_parser import DiagramParser

class PlantUMLSequenceParser(DiagramParser):
    def parse(self, plantuml: str) -> SequenceDiagram:
        # Сначала собираем все строки, удаляя @startuml, @enduml и пустые строки
        all_lines = [line.strip() for line in plantuml.splitlines() 
                     if line.strip() and not line.strip().startswith('@')]
        
        # Сбор актёров и участников из объявлений
        actors = {}
        participants = {}
        for line in all_lines:
            m_actor_alias = re.match(r'^(actor)\s+"([^"]+)"\s+as\s+(\w+)$', line, re.IGNORECASE)
            if m_actor_alias:
                _, _, alias = m_actor_alias.groups()
                actors[alias] = Actor(name=alias)
                continue
            m_actor = re.match(r'^(actor)\s+(\w+)$', line, re.IGNORECASE)
            if m_actor:
                name = m_actor.group(2)
                actors[name] = Actor(name=name)
                continue
            m_part_alias = re.match(r'^(participant)\s+"([^"]+)"\s+as\s+(\w+)$', line, re.IGNORECASE)
            if m_part_alias:
                _, _, alias = m_part_alias.groups()
                participants[alias] = Participant(name=alias)
                continue
            m_part = re.match(r'^(participant)\s+(\w+)$', line, re.IGNORECASE)
            if m_part:
                name = m_part.group(2)
                participants[name] = Participant(name=name)
                continue
        
        # Формируем список строк для событий, исключая объявления
        event_lines = [line for line in all_lines if not re.match(r'^(actor|participant)\s+', line, re.IGNORECASE)]
        
        events, _ = self._parse_events(event_lines, 0)
        
        # Собираем имена участников из событий (если не добавлены явно)
        def collect_names(ev_list):
            for ev in ev_list:
                if isinstance(ev, Message):
                    if ev.sender not in actors and ev.sender not in participants:
                        participants[ev.sender] = Participant(name=ev.sender)
                    if ev.receiver not in actors and ev.receiver not in participants:
                        participants[ev.receiver] = Participant(name=ev.receiver)
                elif isinstance(ev, (Activate, Deactivate)):
                    if ev.participant not in actors and ev.participant not in participants:
                        participants[ev.participant] = Participant(name=ev.participant)
                elif isinstance(ev, Note):
                    if ev.participant and (ev.participant not in actors and ev.participant not in participants):
                        participants[ev.participant] = Participant(name=ev.participant)
                elif isinstance(ev, AltBlock):
                    for cond, subev in ev.alternatives:
                        collect_names(subev)
                elif isinstance(ev, LoopBlock):
                    collect_names(ev.events)
                elif isinstance(ev, ParBlock):
                    for label, branch in ev.branches:
                        collect_names(branch)
        collect_names(events)
        
        return SequenceDiagram(
            actors=list(actors.values()),
            participants=list(participants.values()),
            events=events
        )
    
    def _parse_events(self, lines, i):
        events = []
        while i < len(lines):
            line = lines[i]
            # Завершаем блок, если встречаем "end"
            if line.lower().startswith("end"):
                return events, i + 1
            # Завершаем блок alt/par, если встречаем "else" или "and"
            if line.lower().startswith("else") or line.lower().startswith("and"):
                return events, i
            # Alt-блок
            if line.lower().startswith("alt"):
                condition = line[3:].strip()
                i += 1
                alternatives = []
                alt_events, i = self._parse_events(lines, i)
                alternatives.append((condition, alt_events))
                while i < len(lines) and lines[i].lower().startswith("else"):
                    condition = lines[i][4:].strip()
                    i += 1
                    sub_events, i = self._parse_events(lines, i)
                    alternatives.append((condition, sub_events))
                if i < len(lines) and lines[i].lower().startswith("end"):
                    i += 1
                events.append(AltBlock(alternatives=alternatives))
                continue
            # Loop-блок
            if line.lower().startswith("loop"):
                condition = line[4:].strip()
                i += 1
                loop_events, i = self._parse_events(lines, i)
                events.append(LoopBlock(condition=condition, events=loop_events))
                continue
            # Par-блок
            if line.lower().startswith("par"):
                branch_label = line[3:].strip()
                i += 1
                branch_events, i = self._parse_events(lines, i)
                branches = [(branch_label, branch_events)]
                while i < len(lines) and lines[i].lower().startswith("and"):
                    branch_label = lines[i][3:].strip()
                    i += 1
                    branch_events, i = self._parse_events(lines, i)
                    branches.append((branch_label, branch_events))
                if i < len(lines) and lines[i].lower().startswith("end"):
                    i += 1
                events.append(ParBlock(branches=branches))
                continue
            # Сообщения: поддерживаем как "->" так и "->>"
            m_msg = re.match(r'^(\w+)\s*->>?\s*(\w+)\s*:\s*(.+)$', line)
            if m_msg:
                sender, receiver, msg = m_msg.groups()
                events.append(Message(sender=sender, receiver=receiver, message=msg.strip()))
                i += 1
                continue
            # Активация
            m_act = re.match(r'^activate\s+(\w+)$', line, re.IGNORECASE)
            if m_act:
                participant = m_act.group(1)
                events.append(Activate(participant=participant))
                i += 1
                continue
            # Деактивация
            m_deact = re.match(r'^deactivate\s+(\w+)$', line, re.IGNORECASE)
            if m_deact:
                participant = m_deact.group(1)
                events.append(Deactivate(participant=participant))
                i += 1
                continue
            # Заметка (note)
            m_note = re.match(r'^note(?:\s+(?:over|left of|right of))?\s*(\w+)?\s*:\s*(.+)$', line, re.IGNORECASE)
            if m_note:
                participant = m_note.group(1)
                note_text = m_note.group(2).strip()
                events.append(Note(participant=participant, message=note_text))
                i += 1
                continue
            i += 1
        return events, i
