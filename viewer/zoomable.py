import zlib

def encode_plantuml(plantuml_text: str) -> str:
    """
    Encodes PlantUML text into a format suitable for building a URL
    to a public PlantUML server.
    """
    compressed = zlib.compress(plantuml_text.encode("utf-8"))
    compressed = compressed[2:-4]
    return encode64(compressed)

def encode64(data: bytes) -> str:
    """
    Custom Base64 encoding for PlantUML using the alphabet:
    "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    """
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    
    def encode6bit(b: int) -> str:
        if b < 10:
            return chr(48 + b)
        b -= 10
        if b < 26:
            return chr(65 + b)
        b -= 26
        if b < 26:
            return chr(97 + b)
        b -= 26
        if b == 0:
            return '-'
        elif b == 1:
            return '_'
        else:
            raise Exception("Invalid value for 6-bit encoding")
    
    res = []
    i = 0
    length = len(data)
    while i < length:
        if i + 3 <= length:
            b1, b2, b3 = data[i], data[i+1], data[i+2]
            i += 3
        elif i + 2 == length:
            b1, b2 = data[i], data[i+1]
            b3 = 0
            i += 2
        else:
            b1 = data[i]
            b2 = 0
            b3 = 0
            i += 1
        
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F
        
        res.append(alphabet[c1])
        res.append(alphabet[c2])
        res.append(alphabet[c3])
        res.append(alphabet[c4])
    return "".join(res)

def zoomable_plantuml_html(plantuml_code: str, container_id: str, height: int) -> str:
    """
    Returns an HTML document that displays a PlantUML diagram (rendered as an image)
    wrapped in a container with pan and zoom functionality.
    """
    encoded = encode_plantuml(plantuml_code)
    plantuml_url = f"http://www.plantuml.com/plantuml/svg/{encoded}"
    img_tag = (
        f'<img src="{plantuml_url}" alt="PlantUML Diagram" '
        f'style="width: auto; display: block; margin: auto;" />'
    )
    return f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <!-- Load Panzoom library -->
        <script src="https://unpkg.com/@panzoom/panzoom/dist/panzoom.min.js"></script>
        <style>
          #{container_id} {{
            width: 100%;
            height: {height}px;
            overflow: hidden;
            position: relative;
            border: 1px solid #ddd;
          }}
        </style>
      </head>
      <body>
        <div id="{container_id}">
          {img_tag}
        </div>
        <script>
          const elem = document.getElementById("{container_id}");
          const panzoomInstance = panzoom(elem, {{
            maxZoom: 5,
            minZoom: 0.5
          }});
          // Привязываем метод zoomWithWheel к экземпляру panzoomInstance
          elem.parentElement.addEventListener("wheel", panzoomInstance.zoomWithWheel.bind(panzoomInstance));
        </script>
      </body>
    </html>
    """

def zoomable_mermaid_html(mermaid_code: str, container_id: str, height: int) -> str:
    """
    Returns an HTML document that displays a Mermaid diagram wrapped in a container
    with pan and zoom functionality.
    """
    return f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <!-- Load Mermaid and Panzoom libraries from CDN -->
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <script src="https://unpkg.com/@panzoom/panzoom/dist/panzoom.min.js"></script>
        <script>
          mermaid.initialize({{ startOnLoad: true, securityLevel: 'loose' }});
        </script>
        <style>
          #{container_id} {{
            width: 100%;
            height: {height}px;
            overflow: hidden;
            position: relative;
            border: 1px solid #ddd;
          }}
        </style>
      </head>
      <body>
        <div id="{container_id}">
          <div class="mermaid">
{mermaid_code}
          </div>
        </div>
        <script>
          const elem = document.getElementById("{container_id}");
          const panzoomInstance = panzoom(elem, {{
            maxZoom: 5,
            minZoom: 0.5
          }});
          // Привязываем метод zoomWithWheel к экземпляру panzoomInstance
          elem.parentElement.addEventListener("wheel", panzoomInstance.zoomWithWheel.bind(panzoomInstance));
        </script>
      </body>
    </html>
    """
