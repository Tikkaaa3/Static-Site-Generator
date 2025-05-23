import os
import shutil

from markdown_to_html import markdown_to_html_node


def copy_content(src="./static", dest="./docs", is_root=True):
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


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown_file = f.read()

    with open(template_path) as f:
        template = f.read()

    node = markdown_to_html_node(markdown_file)
    html = node.to_html()
    title = extract_title(markdown_file)

    # Inject basepath into static asset links and internal URLs
    html = html.replace('href="/', f'href="{basepath}/')
    html = html.replace('src="/', f'src="{basepath}/')

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace(
        "{{ BasePath }}", basepath if basepath.endswith("/") else basepath + "/"
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(content_path) and content_path.endswith(".md"):
            dest_path = dest_path.replace(".md", ".html")
            generate_page(content_path, template_path, dest_path, basepath)
        elif os.path.isfile(content_path):
            continue
        else:
            generate_pages_recursive(content_path, template_path, dest_path, basepath)
