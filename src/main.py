from page import copy_content
from textnode import TextNode, TextType


def main():
    text_node = TextNode("Here we go again...", TextType.TEXT)
    print(text_node)
    copy_content()


main()
