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

    #Test Regex Extractions
    #Extract Images
    def test_extract_markdown_images_base(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(matches,
                        [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
                        ,"Markdown image extractions should generate text correctly")
        
    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual(matches,
                        [],
                        "Markdown image extractions with no images should extract no list")
        
    def test_extract_markdown_images_with_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_images(text)
        self.assertListEqual(matches,
                        [],
                        "Markdown image extractions with no images should extract no list")
        
    def test_extract_markdown_images_with_images_and_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_images(text)
        self.assertListEqual(matches,
                        [("rick roll", "https://i.imgur.com/aKaOqIh.gif")],
                        "Markdown image extractions should generate text correctly")
    #Extract Links
    def test_extract_markdown_links_base(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches,
                        [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
                        "Markdown link extractions should generate text correctly")
        
    def test_extract_markdown_links_no_links(self):
        text = "This is text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches,
                        [],
                        "Markdown link extractions with no links should extract no list")
        
    def test_extract_markdown_links_with_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches,
                        [],
                        "Markdown link extractions with no links should extract no list")
        
    def test_extract_markdown_images_with_links_and_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches,
                        [("to youtube", "https://www.youtube.com/@bootdotdev")],
                        "Markdown link extractions should generate text correctly")
        
    #Test Split Nodes Link

    def test_split_links(self):
        node = TextNode(
            "This is text with links to [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with links to ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_empty_node(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([], new_nodes)

    def test_split_links_only_link(self):
        node = TextNode("[link text](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link text", TextType.LINK, "https://example.com")],
            new_nodes
        )
    
    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("First node with [a link](https://example.com)", TextType.TEXT),
            TextNode("Second node", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("First node with ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://example.com"),
                TextNode("Second node", TextType.TEXT)
            ],
            new_nodes
        )
    
    def test_split_links_non_text_node(self):
        node = TextNode("Some text", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
        
    #Test split nodes image    

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_no_links(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    #test text to textnodes
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_double(self):
        nodes = text_to_textnodes(
            "This is **text** and **text** with an _italic_ word and _italic_ word and a `code block` and another `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and a [to boot dev](https://www.boot.dev) and one more [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and another ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and one more ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            nodes,
        )

    def test_empty_string(self):
        nodes = text_to_textnodes("")
        self.assertListEqual([], nodes)
    
    def test_plain_text(self):
        nodes = text_to_textnodes("Just some plain text with no formatting.")
        self.assertListEqual(
            [TextNode("Just some plain text with no formatting.", TextType.TEXT)],
            nodes
        )

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ['This is **bolded** paragraph', 'This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line', '- This is a list\n- with items'],
        )
    
    def test_markdown_to_blocks_empty_blocks(self):
        md = """



    This is **bolded** paragraph

    
    
    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    

    - This is a list
    - with items



    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ['This is **bolded** paragraph', 'This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line', '- This is a list\n- with items'],
        )

    def test_markdown_to_blocks_single_block(self):
        md = """

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line
    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line
    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line
    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line
    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line
    

    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ['This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line']
        )

    def test_markdown_to_blocks_empty_input(self):
        md = """






    

    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

    def test_markdown_to_blocks_complex_multiline(self):
        md = """# Heading

A paragraph with
multiple lines
but still one block.

```python
def code_example():
    print("This is a code block")

    # With a blank line
    return True
```

- List item 1
    - Nested item
    - Another nested item
- List item 2
  With a continuation"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ['# Heading', 'A paragraph with\nmultiple lines\nbut still one block.', '```python\ndef code_example():\nprint("This is a code block")', '# With a blank line\nreturn True\n```', '- List item 1\n- Nested item\n- Another nested item\n- List item 2\nWith a continuation'],
        )

    
    
class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_code_block(self):
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "```\nprint('hi')\nprint('bye')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "```\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "> quote\nnot quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "- item 1\n- item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "- item 1\nnot a list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "1. item 1\n2. item 2\n3. item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "1. item 1\n3. item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1. item 1\n2. item 2\n4. item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "Just a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "not a list\nstill not a list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()