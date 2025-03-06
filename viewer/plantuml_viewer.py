import streamlit.components.v1 as components
from viewer.renderer import DiagramRenderer
from viewer.zoomable import zoomable_plantuml_html

class PlantUMLRenderer(DiagramRenderer):
    def render(self, plantuml_code: str, height: int):
        html = zoomable_plantuml_html(plantuml_code, "plantuml-container", height)
        components.html(html, height=height, scrolling=True)
