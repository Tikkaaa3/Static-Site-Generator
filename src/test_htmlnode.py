import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        childNode = HTMLNode("a", "goUP", "", {"href": "https://www.google.com"})
        node1 = HTMLNode(
            "p",
            "This is is a paragraph.",
            childNode,
            {"class": "customParagraph"},
        )
        node2 = HTMLNode(
            "p",
            "This is is a paragraph.",
            childNode,
            {"class": "customParagraph"},
        )
        self.assertEqual(node1, node2)

    def test_eq_edge(self):
        node1 = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node1, node2)

    def test_noteq(self):
        childNode1 = HTMLNode("h1", "UP")
        childNode2 = HTMLNode("a", "goUP", {"href": "https://www.google.com"})
        node1 = HTMLNode(
            "p",
            "This is is a paragraph.",
            childNode1,
            {"class": "customParagraph"},
        )
        node2 = HTMLNode(
            "p",
            "This is is a paragraph.",
            childNode2,
            {"class": "customParagraph"},
        )
        self.assertNotEqual(node1, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Title")
        self.assertEqual(node.to_html(), "<h1>Title</h1>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_and_props(self):
        grandchild_node = LeafNode("b", "grandchild", {"class": "child"})
        child_node = ParentNode("span", [grandchild_node], {"class": "child"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span class="child"><b class="child">grandchild</b></span></div>',
        )
