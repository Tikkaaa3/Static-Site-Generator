from page import copy_content, generate_pages_recursive


def main():
    copy_content()
    generate_pages_recursive("content/", "template.html", "public/")


main()
