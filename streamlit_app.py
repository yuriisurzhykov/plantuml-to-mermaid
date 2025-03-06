import streamlit as st
from components.plantuml_components_parser import PlantUMLComponentParser
from components.mermaid_components_generator import MermaidGenerator
from classes.plantuml_class_parser import PlantUMLClassParser
from classes.mermaid_class_generator import MermaidClassGenerator
from sequence.plantuml_sequence_parser import PlantUMLSequenceParser
from sequence.mermaid_sequence_generator import MermaidSequenceGenerator
from resources.image import get_base64_image
from viewer.plantuml_viewer import PlantUMLRenderer
from viewer.mermaid_viewer import MermaidRenderer

def main():
    st.set_page_config(page_title="PlantUML to Mermaid Converter", layout="wide")
    
    # Display logo
    try:
        logo_b64 = get_base64_image("resources/project_logo.png")
        html_logo = (
            f'<div style="text-align: center;">'
            f'<img src="data:image/png;base64,{logo_b64}" alt="Logo" width="350">'
            f'</div>'
        )
        st.markdown(html_logo, unsafe_allow_html=True)
    except Exception as e:
        st.error("Error loading logo: " + str(e))
    
    st.title("PlantUML to Mermaid Converter")
    st.markdown("Convert your PlantUML code to a readable Mermaid syntax.")

    # Sidebar settings and instructions
    st.sidebar.header("Diagram Settings")
    diagram_type = st.sidebar.selectbox(
        "Select diagram type",
        ["🧩 Components", "📚 Class", "🔄 Sequence"],
        index=0
    )
    st.sidebar.markdown(
        """
        **Instructions:**
        1. Paste your PlantUML code in the text area.
        2. Click **Convert to Mermaid**.
        3. The top row shows the PlantUML code and its preview, while the bottom row displays
           the generated Mermaid code and its preview.
        """
    )
    
    # Define placeholder text based on the selected diagram type
    if "Components" in diagram_type:
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
    elif "Class" in diagram_type:
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
    elif "Sequence" in diagram_type:
        placeholder_text = (
            '@startuml\n'
            'actor User\n'
            'participant "Mobile App" as App\n'
            'participant "Auth Service" as Auth\n'
            'participant "Payment Gateway" as Payment\n'
            'participant "Order Service" as Order\n\n'
            'User -> App: Login\n'
            'activate App\n'
            'App -> Auth: Validate Credentials\n'
            'alt Valid Credentials\n'
            '    Auth -> App: Success\n'
            '    deactivate Auth\n'
            '    App -> Payment: Initiate Payment\n'
            '    activate Payment\n'
            '    alt Payment Approved\n'
            '         Payment -> Order: Create Order\n'
            '         activate Order\n'
            '         Order -> Payment: Confirm Order\n'
            '         deactivate Order\n'
            '         Payment -> App: Payment Successful\n'
            '    else Payment Declined\n'
            '         Payment -> App: Payment Failed\n'
            '    end\n'
            '    deactivate Payment\n'
            'else Invalid Credentials\n'
            '    Auth -> App: Failure\n'
            '    deactivate Auth\n'
            'end\n'
            'App -> User: Show Result\n'
            'deactivate App\n'
            '@enduml'
        )
    else:
        placeholder_text = ""
    
    # ------------------------------------------------------------------
    # Top Row: PlantUML Input and Preview
    # ------------------------------------------------------------------
    with st.container():
        top_cols = st.columns(2)
        with top_cols[0]:
            st.subheader("PlantUML Code")
            plantuml_code = st.text_area(
                "Enter your PlantUML code", 
                height=400, 
                placeholder=placeholder_text
            )
            convert_button = st.button("Convert to Mermaid")
        with top_cols[1]:
            st.subheader("PlantUML Diagram Preview")
            plantuml_renderer = PlantUMLRenderer()
            if plantuml_code.strip():
                plantuml_renderer.render(plantuml_code, 400)
            else:
                st.info("Enter your PlantUML code to preview the diagram.")
    
    # ------------------------------------------------------------------
    # Bottom Row: Mermaid Code and Preview
    # ------------------------------------------------------------------
    with st.container():
        bottom_cols = st.columns(2)
        if convert_button and plantuml_code.strip():
            # Choose the appropriate parser and generator based on diagram type
            if "Components" in diagram_type:
                parser = PlantUMLComponentParser()
                diagram = parser.parse(plantuml_code)
                generator = MermaidGenerator()
                mermaid_code = generator.generate(diagram)
            elif "Class" in diagram_type:
                parser = PlantUMLClassParser()
                diagram = parser.parse(plantuml_code)
                generator = MermaidClassGenerator()
                mermaid_code = generator.generate(diagram)
            elif "Sequence" in diagram_type:
                parser = PlantUMLSequenceParser()
                diagram = parser.parse(plantuml_code)
                generator = MermaidSequenceGenerator()
                mermaid_code = generator.generate(diagram)
            else:
                mermaid_code = ""
            
            with bottom_cols[0]:
                st.subheader("Generated Mermaid Code")
                st.code(mermaid_code, language="mermaid")
            with bottom_cols[1]:
                st.subheader("Mermaid Diagram Preview")
                mermaid_renderer = MermaidRenderer()
                mermaid_renderer.render(mermaid_code, 500)
        else:
            with bottom_cols[0]:
                st.info("Click **Convert to Mermaid** to convert your PlantUML code.")
            with bottom_cols[1]:
                st.info("Mermaid diagram preview will appear after conversion.")

if __name__ == "__main__":
    main()
