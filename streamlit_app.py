import streamlit as st
from plantuml_parser import PlantUMLComponentParser
from mermaid_generator import MermaidGenerator
from mermaid_viewer import render_mermaid

def main():
    st.set_page_config(page_title="PlantUML to Mermaid Converter", layout="wide")
    st.title("PlantUML to Mermaid Converter (Components Diagram)")

    plantuml_code = st.text_area(
        "Paste your PlantUML code here:",
        height=400,
        placeholder=(
            '@startuml\n'
            'component "UI (Compose Screen)" as UI\n'
            'component "ViewModel\\n(State Holder)" as VM\n'
            'component "Domain/Repository\\n(Business Logic)" as BL\n\n'
            'UI --> VM : User events (intent calls)\n'
            'VM --> BL : Requests data or actions\n'
            'VM <-- BL : New data/result\n'
            'UI <-- VM : Updated UI State\n'
            '@enduml'
        )
    )
    convert_button = st.button("Convert to Mermaid")

    if convert_button and plantuml_code.strip():
        # Парсим PlantUML в промежуточное представление диаграммы
        parser = PlantUMLComponentParser()
        diagram = parser.parse(plantuml_code)

        # Генерируем Mermaid-код из промежуточной структуры
        generator = MermaidGenerator()
        mermaid_code = generator.generate(diagram)

        st.markdown("### Generated Mermaid Code")
        st.code(mermaid_code, language="mermaid")

        st.markdown("### Diagram Preview")
        render_mermaid(mermaid_code, height=500)
    else:
        st.write("Converted Mermaid code and diagram preview will appear here after clicking **Convert**.")

if __name__ == "__main__":
    main()
