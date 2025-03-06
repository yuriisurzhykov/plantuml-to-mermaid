import streamlit as st
from viewer.mermaid_viewer import render_mermaid
from components.plantuml_components_parser import PlantUMLComponentParser
from components.mermaid_components_generator import MermaidGenerator
from classes.plantuml_class_parser import PlantUMLClassParser
from classes.mermaid_class_generator import MermaidClassGenerator
from sequence.plantuml_sequence_parser import PlantUMLSequenceParser
from sequence.mermaid_sequence_generator import MermaidSequenceGenerator

def main():
    st.set_page_config(page_title="PlantUML to Mermaid Converter", layout="wide")
    st.title("PlantUML to Mermaid Converter")
    
    # Меню выбора типа диаграммы
    diagram_type = st.selectbox("Select Diagram Type", ["Components", "Class", "Sequence"], index=0)
    
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
            'class Customer {\n'
            '    +int id\n'
            '    +String name\n'
            '    +login()\n'
            '}\n'
            'class Order {\n'
            '    +int orderId\n'
            '    +date orderDate\n'
            '    +calculateTotal()\n'
            '}\n'
            'Customer "1" --> "0..*" Order : places\n'
            'Customer <|-- VIPCustomer\n'
            '@enduml'
        )
    elif diagram_type == "Sequence":
        placeholder_text = (
            '@startuml\n'
            'participant Alice\n'
            'participant Bob\n'
            'Alice -> Bob : Hello Bob, how are you?\n'
            'activate Bob\n'
            'Bob -> Alice : I\'m fine, thanks!\n'
            'deactivate Bob\n'
            'note over Alice: End of conversation\n'
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
        elif diagram_type == "Sequence":
            parser = PlantUMLSequenceParser()
            diagram = parser.parse(plantuml_code)
            generator = MermaidSequenceGenerator()
            mermaid_code = generator.generate(diagram)
            
        st.markdown("### Generated Mermaid Code")
        st.code(mermaid_code, language="mermaid")
        st.markdown("### Diagram Preview")
        render_mermaid(mermaid_code, height=500)
    else:
        st.write("Converted Mermaid code and diagram preview will appear here after clicking **Convert**.")

if __name__ == "__main__":
    main()
