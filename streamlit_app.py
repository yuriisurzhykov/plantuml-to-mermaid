import streamlit as st
import re

def plantuml_to_mermaid(plantuml_code: str) -> str:
    """
    Наивный конвертер из PlantUML кода (только sequence-диаграммы)
    в упрощённый Mermaid.
    """
    # 1. Удаляем служебные теги PlantUML
    lines = plantuml_code.splitlines()
    filtered_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith('@startuml'):
            continue
        if line.startswith('@enduml'):
            continue
        if not line:
            continue
        filtered_lines.append(line)
    
    # 2. Подготавливаем результат под Mermaid sequenceDiagram
    mermaid_lines = ["sequenceDiagram"]

    # 3. Наивно обрабатываем стрелки
    # Пример PlantUML: Alice -> Bob : Hello
    # Переведём в Mermaid: Alice->>Bob: Hello
    # Также учтём вариант ->> (с «двойной стрелкой»)
    arrow_pattern = re.compile(r'^(\S+)\s*([-\>]+)\s*(\S+)\s*:\s*(.*)$')

    for line in filtered_lines:
        match = arrow_pattern.match(line)
        if match:
            source, arrow, target, message = match.groups()
            # PlantUML может иметь -> или ->>
            # Mermaid чаще использует ->> в sequenceDiagram
            # Сведём к единому варианту ->> :
            mermaid_arrow = "->>" if ">>" in arrow else "->>"
            converted_line = f"{source}{mermaid_arrow}{target}: {message}"
            mermaid_lines.append(converted_line)
        else:
            # Здесь можно добавить дополнительный парсинг, 
            # например, для 'participant' или заметок (note)
            # Пока просто добавим строку "как есть"
            mermaid_lines.append(f"%% {line}")  # закомментируем, чтобы не ломать синтаксис
    
    # Объединяем результат
    mermaid_result = "\n".join(mermaid_lines)
    return mermaid_result

def main():
    st.title("Конвертер PlantUML → Mermaid (sequenceDiagram)")

    st.write(
        "Данное демо-приложение наивно конвертирует sequence-диаграммы из PlantUML "
        "в упрощённый Mermaid-код. Учтите, что поддерживаются только очень базовые конструкции."
    )

    plantuml_code = st.text_area(
        "Вставьте ваш PlantUML-код (sequence-диаграмма)", 
        height=200,
        value="""@startuml
Alice -> Bob : Hello
Bob -> Alice : Hi
@enduml"""
    )

    if st.button("Конвертировать"):
        mermaid_code = plantuml_to_mermaid(plantuml_code)
        st.subheader("Результирующий Mermaid-код")
        st.code(mermaid_code, language="markdown")  # указываем markdown, чтобы не ломать Mermaid синтаксис
        st.write("Скопируйте этот результат и проверьте в онлайн-редакторе Mermaid или в других поддерживающих инструментах.")

if __name__ == "__main__":
    main()
