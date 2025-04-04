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

    #split_nodes_delimiter testing
    def test_split_nodes_delimiter_emptybefore(self):
        node = TextNode(" `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,
                         [
                            TextNode(" ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                        ], "TextNodes with empty values before delimiter should render correctly")
        
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,
                         [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                        ], "TextNodes split to code blocks should render correctly")
        
    def test_split_nodes_delimiter_multi_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node], "`", TextType.CODE)
        self.assertEqual(new_nodes,
                         [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                        ], "Multiple TextNodes should render correctly")
        
    def test_split_nodes_delimiter_mismatch(self):
        node = TextNode("This is text with a `code block** word", TextType.TEXT)
        with self.assertRaises(Exception): 
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_delimter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
                         [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("bold", TextType.BOLD),
                            TextNode(" word", TextType.TEXT),
                        ], "TextNodes should render correctly")
        
    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("This is plain text without delimiters!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
                         [
                            TextNode("This is plain text without delimiters!", TextType.TEXT)
                        ], "TextNodes with no delimiters should render correctly")



        


if __name__ == "__main__":
    unittest.main()