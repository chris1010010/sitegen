from textnode import TextNode, TextType
import os
import shutil
from create_html import generate_page

def main():
    print("main:")

    copy_files("static", "public")

    generate_page("content/index.md", "template.html", "public/index.html")


def copy_files(source, target):
    try:
        working_dir = os.getcwd()
        source_path = os.path.join(working_dir, source)
        target_path = os.path.join(working_dir, target)

        print("Clearing " + target_path)
        shutil.rmtree(target_path)

        print("Copying from " + source_path + " to " + target_path)
        shutil.copytree(source_path, target_path)
        print("Done")
    except Exception as e:
        print(e)

main()