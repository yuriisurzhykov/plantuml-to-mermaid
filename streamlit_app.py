import streamlit as st
from viewer.mermaid_viewer import render_mermaid
from components.plantuml_components_parser import PlantUMLComponentParser
from components.mermaid_components_generator import MermaidGenerator
from classes.plantuml_class_parser import PlantUMLClassParser
from classes.mermaid_class_generator import MermaidClassGenerator
from sequence.plantuml_sequence_parser import PlantUMLSequenceParser
from sequence.mermaid_sequence_generator import MermaidSequenceGenerator
from resources.image import get_base64_image


def main():
    st.set_page_config(page_title="PlantUML to Mermaid Converter", layout="wide")
    
    # Загружаем логотип из ресурсов и отображаем его через Base64
    try:
        logo_b64 = get_base64_image("resources/project_logo.png")
        html_logo = f'<div style="text-align: center;"><img src="data:image/png;base64,{logo_b64}" alt="Logo" width="350"></div>'
        st.markdown(html_logo, unsafe_allow_html=True)
    except Exception as e:
        st.error("Ошибка при загрузке логотипа: " + str(e))
    
    st.title("PlantUML to Mermaid Converter")
    st.markdown("Переведите ваш PlantUML код в удобочитаемый Mermaid синтаксис.")

    # Сайдбар с настройками и инструкциями
    st.sidebar.header("Настройки диаграммы")
    diagram_type = st.sidebar.selectbox(
        "Выберите тип диаграммы",
        ["🧩 Components", "📚 Class", "🔄 Sequence"],
        index=0
    )
    st.sidebar.markdown(
        """
        **Инструкция:**
        1. Вставьте ваш PlantUML код в текстовое поле.
        2. Нажмите кнопку **Convert to Mermaid**.
        3. Слева будет показан сгенерированный Mermaid код, справа – предварительный просмотр диаграммы.
        """
    )

    # Placeholder-текст зависит от выбранного типа диаграммы
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

    st.subheader("Введите ваш PlantUML код")
    plantuml_code = st.text_area("PlantUML Code", height=400, placeholder=placeholder_text)

    convert_button = st.button("Convert to Mermaid")

    if convert_button and plantuml_code.strip():
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
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Generated Mermaid Code")
            st.code(mermaid_code, language="mermaid")
        with col2:
            st.markdown("### Diagram Preview")
            render_mermaid(mermaid_code, height=500)
    else:
        st.info("Введите ваш PlantUML код и нажмите **Convert to Mermaid**.")

if __name__ == "__main__":
    main()
