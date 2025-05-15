import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_images(old_node.text)

        if not links:
            new_nodes.append(old_node)
            continue

        curr_text = old_node.text
        curr_nodes = []

        for image_alt, image_link in links:

            parts = curr_text.split(f"![{image_alt}]({image_link})", 1)

            if parts[0]:
                curr_nodes.append(TextNode(parts[0], TextType.TEXT))

            curr_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            if len(parts) > 1:
                curr_text = parts[1]
            else:
                curr_text = ""

        if curr_text:
            curr_nodes.append(TextNode(curr_text, TextType.TEXT))

        new_nodes.extend(curr_nodes)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)

        if not links:
            new_nodes.append(old_node)
            continue

        curr_text = old_node.text
        curr_nodes = []

        for link_text, link_url in links:

            parts = curr_text.split(f"[{link_text}]({link_url})", 1)

            if parts[0]:
                curr_nodes.append(TextNode(parts[0], TextType.TEXT))

            curr_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            if len(parts) > 1:
                curr_text = parts[1]
            else:
                curr_text = ""

        if curr_text:
            curr_nodes.append(TextNode(curr_text, TextType.TEXT))

        new_nodes.extend(curr_nodes)

    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_image([node])
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
