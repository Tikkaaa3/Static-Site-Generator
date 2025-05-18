import os
import shutil

from markdown_to_html import markdown_to_html_node


def copy_content(src="static/", dest="public/", is_root=True):
    if os.path.exists(dest) and is_root:
        shutil.rmtree(dest)

    if not os.path.exists(dest):
        os.mkdir(dest)
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            os.mkdir(dest_path)
            copy_content(src_path, dest_path, False)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#") and line[1] == " ":
            return line[2:].strip()
    raise Exception(f"No title found in {markdown}")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template_path")

    f = open(from_path)
    markdown_file = f.read()
    f.close()

    f = open(template_path)
    template_file = f.read()
    f.close()

    node = markdown_to_html_node(markdown_file)
    node = node.to_html()
    title = extract_title(markdown_file)

    result = template_file.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", node)
