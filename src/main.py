from textnode import TextNode, TextType
import os
import shutil
from create_html import generate_page
import sys

def main():
    print("main:")

    basepath = "/"
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    print("Basepath: " + basepath)

    copy_files("static", "public")

    generate_pages_recursive("content", "template.html", "docs", basepath)
    #generate_page("content/index.md", "template.html", "public/index.html")
    #generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    #generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    #generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    #generate_page("content/contact/index.md", "template.html", "public/contact/index.html")


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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):

    files = os.listdir(dir_path_content)
    for name in files:
        path = os.path.join(dir_path_content, name)
        if os.path.isdir(path):
            generate_pages_recursive(path, template_path, os.path.join(dest_dir_path, name), basepath)
        else:
            generate_page(path, template_path, os.path.join(dest_dir_path, name).replace(".md", ".html"), basepath)
            

main()