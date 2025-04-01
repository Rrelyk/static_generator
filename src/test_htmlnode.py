import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        # Test with no props (None)
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "", "Empty props should return empty strings")
    def test_props_to_html_single_prop(self):
        # Test with a single property
        node = HTMLNode(props={"href": "www.test.com"})
        self.assertEqual(node.props_to_html(),' href="www.test.com"', "Single prop should be formatted correctly")

    def test_props_to_html_multiple_props(self):
        # Test with multiple properties
        node = HTMLNode(props={"href": "www.test.com", "target": "test"})
        # Note: Order might not be guaranteed in dictionaries, so this might need adjustment
        self.assertTrue(' href="www.test.com"' in node.props_to_html(), "Multiple props should include href")
        self.assertTrue(' target="test"' in node.props_to_html(), "Multiple props should include target")

    def test_props_with_empty_values(self):
        node = HTMLNode(props={"data-id": "", "aria-hidden": ""})
        self.assertTrue(' data-id=""' in node.props_to_html(), "Props with empty values should be included")

    def test_props_with_numeric_values(self):
        node = HTMLNode(props={"rows": 5, "cols": 10})
        self.assertTrue(' rows="5"' in node.props_to_html(), "Numeric props should be converted to strings")
    
    def test_props_with_boolean_values(self):
        node = HTMLNode(props={"disabled": True, "readonly": False})
        self.assertTrue(' disabled="True"' in node.props_to_html(), "Boolean props should be included")

    def test_empty_props_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "", "Empty props dict should return empty string")

    # Test leafNode
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>", "LeafNode 'p' tag should be rendered correctly")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>', "LeafNode 'a' tag should be rendered correctly")
    
    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", {"src":"url/of/image.jpg"})
        self.assertEqual(node.to_html(), '<img src="url/of/image.jpg" />', "LeafNode 'img' tag should be rendered correctly")

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text", "LeafNode with no tag should return just the value")

    def test_leaf_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("div", None).to_html()

    def test_leaf_with_multiple_props(self):
        node = LeafNode("input", "", {"type": "text", "name": "username", "placeholder": "Enter username"})
        # Adjust expected output based on your implementation
        # For non-self-closing tags:
        # self.assertEqual(node.to_html(), '<input type="text" name="username" placeholder="Enter username"></input>')
        # For self-closing tags:
        self.assertEqual(node.to_html(), '<input type="text" name="username" placeholder="Enter username" />')

    # Test parentNode
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>", "ParentNode should return child correctly")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
            "ParentNode should return grandchildren correctly"
        )
    
    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_with_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("b", "bold")
        child2 = LeafNode("i", "italic")
        parent = ParentNode("p", [child1, child2])
        self.assertEqual(parent.to_html(), "<p><b>bold</b><i>italic</i></p>", "ParentNode with multiple children should return correctly")

    def test_to_html_with_props(self):
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(parent.to_html(), "<div class=\"container\"><span>text</span></div>", "ParentNode with props should return correctly")   
    
    def test_to_html_with_empty_children_list(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>", "ParentNode with empty children list should return correctly")

if __name__ == "__main__":
    unittest.main()