from convert import markdown_to_html_node
import os
from os.path import realpath
from os.path import dirname


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]
    raise Exception("No h1 found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    os.makedirs(realpath(dirname(dest_path)), mode=0o777, exist_ok=True)
    with open(from_path) as f, open(template_path) as t, open(dest_path, "w") as d:
        markdown = f.read()
        template = t.read()
        
        html_node = markdown_to_html_node(markdown)
        html = html_node.to_html()

        title = extract_title(markdown)

        template = template.replace("{{ Title }}", title)
        template = template.replace("{{ Content }}", html)

        template = template.replace('href="/', f"href=\"{basepath}")
        template = template.replace('src="/', f"src=\"{basepath}")

        d.write(template)


