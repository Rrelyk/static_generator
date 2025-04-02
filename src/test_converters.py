import unittest

from htmlnode import *
from textnode import *
from converters import *

class TestHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None, "TextNode conversion should return no tag")
        self.assertEqual(html_node.value, "This is a text node", "TextNode conversion should properly return html_node.value")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b", "TextNode conversion should return 'b' tag")
        self.assertEqual(html_node.value, "This is a text node", "TextNode conversion should properly return html_node.value")
    
    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i", "TextNode conversion should return 'i' tag")
        self.assertEqual(html_node.value, "This is a text node", "TextNode conversion should properly return html_node.value")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code", "TextNode conversion should return 'code' tag")
        self.assertEqual(html_node.value, "This is a text node", "TextNode conversion should properly return html_node.value")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a", "TextNode conversion should return 'a' tag")
        self.assertEqual(html_node.value, "This is a text node", "TextNode conversion should properly return html_node.value as anchor text")
        self.assertEqual(html_node.props, {"href":"https://www.google.com"}, "TextNode conversion should properly return html_node.properties")

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img", "TextNode conversion should return 'img' tag")
        self.assertEqual(html_node.value, "", "TextNode conversion should properly return html_node.value")
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "This is a text node"}, "TextNode conversion should properly return html_node.properties")

if __name__ == "__main__":
    unittest.main()