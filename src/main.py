import sys

from page import copy_content, generate_pages_recursive


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_content()
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)


main()
