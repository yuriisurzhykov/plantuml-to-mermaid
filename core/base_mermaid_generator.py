class BaseMermaidGenerator:
    @staticmethod
    def escape_text(text: str, support_lucid: bool = False) -> str:
        """
        Экранирует специальные символы для Mermaid:
          - &  -> &amp;
          - ;  -> #59;
          - последовательности "\n" и реальные переводы строк -> <br>
          - (  -> #40;
          - )  -> #41;
        """
        if support_lucid:
            return text
        safe = text.replace("&", "&amp;")
        safe = safe.replace(";", "#59;")
        safe = safe.replace("\\n", "<br>").replace("\n", "<br>")
        safe = safe.replace("(", "#40;").replace(")", "#41;")
        return safe

    @staticmethod
    def format_name(name: str) -> str:
        """
        Форматирует имя участника (actor/participant) для Mermaid:
         – сначала экранирует спецсимволы,
         – затем заменяет внутренние кавычки на экранированные,
         – если в результате обнаружены пробелы, оборачивает имя в кавычки.
        """
        escaped = BaseMermaidGenerator.escape_text(name)
        escaped = escaped.replace('"', '\\"')
        if any(c.isspace() for c in escaped):
            return f'"{escaped}"'
        return escaped

    @staticmethod
    def format_condition(text: str) -> str:
        """
        Форматирует текст для условий в блоках (alt, loop, par).
        Просто экранирует текст без оборачивания в кавычки.
        """
        return BaseMermaidGenerator.escape_text(text)
