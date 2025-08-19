# nns_parser.py
import webbrowser
import os

class NNS:
    def __init__(self):
        self.html = []
        self.css = []
        self.js = []
        self.section = None

    def parse_line(self, line):
        line = line.strip()
        if not line or line.startswith("#"):
            return

        # Changement de section
        if line.lower() == "html":
            self.section = "html"
            return
        elif line.lower() == "css":
            self.section = "css"
            return
        elif line.lower() == "js":
            self.section = "js"
            return

        # Parsing selon la section
        if self.section == "html":
            if "=" in line:
                key, value = line.split("=", 1)
                key, value = key.strip(), value.strip()
                if key.lower() == "titre":
                    self.html.insert(0, f"<title>{value}</title>")
                elif key.lower() == "h1":
                    self.html.append(f"<h1>{value}</h1>")
                elif key.lower() == "h2":
                    self.html.append(f"<h2>{value}</h2>")
                elif key.lower() == "paragraphe":
                    self.html.append(f"<p>{value}</p>")
                elif key.lower() == "bouton" and "->" in value:
                    text, link = value.split("->")
                    text, link = text.strip(), link.strip()
                    self.html.append(f'<a href="{link}"><button>{text}</button></a>')
        elif self.section == "css":
            if "=" in line:
                key, value = line.split("=", 1)
                key, value = key.strip(), value.strip()
                if key.lower() == "couleur":
                    self.css.append(f"body {{ color: {value}; }}")
                elif key.lower() == "fond":
                    self.css.append(f"body {{ background-color: {value}; }}")
                elif key.lower() == "police":
                    self.css.append(f"body {{ font-family: {value}; }}")
                elif key.lower() == "police-taille":
                    self.css.append(f"body {{ font-size: {value}; }}")
        elif self.section == "js":
            self.js.append(line)  # Pour l'instant on met juste les lignes dans le script

    def parse_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                self.parse_line(line)

    def generate_html(self, output_file="output.html"):
        content = "<!DOCTYPE html>\n<html>\n<head>\n"
        content += "\n".join(self.html) + "\n"
        if self.css:
            content += "<style>\n" + "\n".join(self.css) + "\n</style>\n"
        content += "</head>\n<body>\n"
        content += "\n".join([line for line in self.html if not line.startswith("<title>")]) + "\n"
        if self.js:
            content += "<script>\n" + "\n".join(self.js) + "\n</script>\n"
        content += "</body>\n</html>"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Page générée: {output_file}")
        webbrowser.open('file://' + os.path.realpath(output_file))  # ouvre automatiquement dans le navigateur


if __name__ == "__main__":
    nns = NNS()
    nns.parse_file("mon_site.nns")  # Remplacez par votre fichier NNS
    nns.generate_html()
