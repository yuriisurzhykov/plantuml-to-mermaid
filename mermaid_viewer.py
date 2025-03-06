import streamlit.components.v1 as components

def render_mermaid(mermaid_code: str, height: int = 500):
    """
    Отображает Mermaid диаграмму, используя mermaid.js через встроенный HTML.
    """
    html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <!-- Подключаем Mermaid из CDN -->
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <script>
          mermaid.initialize({{startOnLoad:true, securityLevel:'loose'}});
        </script>
        <style>
          body {{
            margin: 0;
            padding: 0;
          }}
        </style>
      </head>
      <body>
        <div class="mermaid">
{mermaid_code}
        </div>
      </body>
    </html>
    """
    components.html(html, height=height, scrolling=True)
