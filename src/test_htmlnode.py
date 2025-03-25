import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()