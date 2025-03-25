import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_text_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2, "TextNodes with same text should be equal.")

    def test_text_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2, "TextNodes with different text should not be equal.")

    def test_text_type_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2, "TextNodes with same type should be equal.")

    def test_text_type_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2, "TextNodes with different type should not be equal.")

    def test_urls_eq(self):
        node = TextNode("This is a text node", TextType.TEXT, "www.test.com")
        node2 = TextNode("This is a text node", TextType.TEXT, "www.test.com")
        self.assertEqual(node, node2, "TextNodes with the same URLS should be equal.")

    def test_urls_ne(self):
        node = TextNode("This is a text node", TextType.TEXT, "www.test.com")
        node2 = TextNode("This is a text node", TextType.TEXT, "www.testing.com")
        self.assertNotEqual(node, node2, "TextNodes with different URLS should not be equal.")

    def test_one_url_none(self):
        node = TextNode("This is a text node", TextType.TEXT, None)
        node2 = TextNode("This is a text node", TextType.TEXT, "www.test.com")
        self.assertNotEqual(node, node2, "TextNode with URL=None should not equal one with a URL value")

    def test_both_urls_none(self):
        node = TextNode("This is a text node", TextType.TEXT, None)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2, "TextNodes should be equal when both have None URLs")

    



if __name__ == "__main__":
    unittest.main()