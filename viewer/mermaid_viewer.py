import streamlit.components.v1 as components
from viewer.renderer import DiagramRenderer
from viewer.zoomable import zoomable_mermaid_html

class MermaidRenderer(DiagramRenderer):
    def render(self, mermaid_code: str, height: int):
        html = zoomable_mermaid_html(mermaid_code, "mermaid-container", height)
        components.html(html, height=height, scrolling=True)
