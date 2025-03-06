from dataclasses import dataclass
from typing import List, Optional, Union

@dataclass
class Participant:
    name: str

@dataclass
class Actor:
    name: str

@dataclass
class Message:
    sender: str
    receiver: str
    message: str

@dataclass
class Activate:
    participant: str

@dataclass
class Deactivate:
    participant: str

@dataclass
class Note:
    participant: Optional[str]  # если None – глобальная заметка
    message: str

# Контрольные блоки:
@dataclass
class AltBlock:
    # Список альтернатив: каждая альтернатива – кортеж (condition, events)
    alternatives: List[tuple]

@dataclass
class LoopBlock:
    condition: str
    events: List[Union['Message', 'Activate', 'Deactivate', 'Note', 'AltBlock', 'LoopBlock', 'ParBlock']]

@dataclass
class ParBlock:
    # Каждая ветка – кортеж (branch_label, events)
    branches: List[tuple]

# Общая модель диаграммы:
@dataclass
class SequenceDiagram:
    actors: List[Actor]
    participants: List[Participant]
    events: List[Union[Message, Activate, Deactivate, Note, AltBlock, LoopBlock, ParBlock]]
