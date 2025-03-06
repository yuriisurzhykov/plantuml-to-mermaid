import streamlit as st
from mermaid_viewer import render_mermaid
from plantuml_parser import PlantUMLComponentParser
from mermaid_generator import MermaidGenerator
from plantuml_class_parser import PlantUMLClassParser
from mermaid_class_generator import MermaidClassGenerator

def main():
    st.set_page_config(page_title="PlantUML to Mermaid Converter", layout="wide")
    st.title("PlantUML to Mermaid Converter")
    
    # Меню выбора типа диаграммы
    diagram_type = st.selectbox("Select Diagram Type", ["Components", "Class"], index=0)
    
    placeholder_text = ""
    if diagram_type == "Components":
        placeholder_text = (
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
    elif diagram_type == "Class":
        placeholder_text = (
            '@startuml\n'
            'class Animal {\n'
            '    +int age\n'
            '    +String gender\n'
            '    +isMammal()\n'
            '    +mate()\n'
            '}\n'
            'class Duck {\n'
            '    +String beakColor\n'
            '    +swim()\n'
            '    +quack()\n'
            '}\n'
            'Animal <|-- Duck\n'
            '@enduml'
        )
        
    plantuml_code = st.text_area("Paste your PlantUML code here:", height=400, placeholder=placeholder_text)
    convert_button = st.button("Convert to Mermaid")
    
    if convert_button and plantuml_code.strip():
        if diagram_type == "Components":
            parser = PlantUMLComponentParser()
            diagram = parser.parse(plantuml_code)
            generator = MermaidGenerator()
            mermaid_code = generator.generate(diagram)
        elif diagram_type == "Class":
            parser = PlantUMLClassParser()
            diagram = parser.parse(plantuml_code)
            generator = MermaidClassGenerator()
            mermaid_code = generator.generate(diagram)
            
        st.markdown("### Generated Mermaid Code")
        st.code(mermaid_code, language="mermaid")
        st.markdown("### Diagram Preview")
        render_mermaid(mermaid_code, height=500)
    else:
        st.write("Converted Mermaid code and diagram preview will appear here after clicking **Convert**.")

if __name__ == "__main__":
    main()
