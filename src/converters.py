from htmlnode import *
from textnode import *
import re


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b",text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text, None)
        case TextType.CODE:
            return LeafNode("code",text_node.text, None)
        case TextType.LINK:
            return LeafNode("a",text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img","", {"src":text_node.url,"alt":text_node.text})
        case _:
            raise Exception("TextNode is not a valid TextType")

def text_to_textnodes(text):
    nodes = [TextNode(text,TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**',TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_',TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`',TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    output_nodes = []

    def delimiter_text_search(node, delimiter):
        opening_index = node.text.find(delimiter)
        if opening_index == -1:
            if node.text:
                output_nodes.append(node)
            return
        
        if opening_index != -1:
            closing_substring_index = node.text[opening_index + len(delimiter):].find(delimiter)
            if closing_substring_index == -1:
                raise Exception ("No closing Delimiter Found")

            #calc actual indices
            closing_index = opening_index + len(delimiter) + closing_substring_index

            #split into 3 parts
            text_before = node.text[:opening_index]
            if text_before != "":
                node_before = TextNode(text_before, node.text_type)
                output_nodes.append(node_before)
            
            text_between = node.text[opening_index + len(delimiter):closing_index]
            if text_between != "":
                node_between = TextNode(text_between, text_type)
                output_nodes.append(node_between)
            
            text_after = node.text[closing_index + len(delimiter):]
            return delimiter_text_search(TextNode(text_after, node.text_type), delimiter)

    
    for node in old_nodes:
        match node.text_type:
            case TextType.TEXT:          
                delimiter_text_search(node, delimiter)
            case _:
                output_nodes.append(node)   
    
    return output_nodes

def split_nodes_link(old_nodes):
    output_nodes = []

    def link_text_search(node):
        matches = extract_markdown_links(node.text)
        if not matches:
            if node.text:  # Only add nodes with non-empty text
                output_nodes.append(node)
            return

        first_match_text, first_match_url = matches[0]
        original_pattern = f"[{first_match_text}]({first_match_url})"
        sections = node.text.split(original_pattern, 1)
        
        # Only add text before the link if it's not empty
        if sections[0]:
            output_nodes.append(TextNode(sections[0], node.text_type))
        
        # Add the image node
        output_nodes.append(TextNode(first_match_text, TextType.LINK, first_match_url))
        
        text_after = sections[1] if len(sections) > 1 else ""
        if text_after:
            link_text_search(TextNode(text_after, node.text_type))

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            link_text_search(node)
        else:
            output_nodes.append(node)

    return output_nodes

def split_nodes_image(old_nodes):
    output_nodes = []

    def image_text_search(node):
        matches = extract_markdown_images(node.text)
        if not matches:
            if node.text:  # Only add nodes with non-empty text
                output_nodes.append(node)
            return

        first_match_text, first_match_url = matches[0]
        original_pattern = f"![{first_match_text}]({first_match_url})"
        sections = node.text.split(original_pattern, 1)
        
        # Only add text before the image if it's not empty
        if sections[0]:
            output_nodes.append(TextNode(sections[0], node.text_type))
        
        # Add the image node
        output_nodes.append(TextNode(first_match_text, TextType.IMAGE, first_match_url))
        
        text_after = sections[1] if len(sections) > 1 else ""
        if text_after:
            image_text_search(TextNode(text_after, node.text_type))

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            image_text_search(node)
        else:
            output_nodes.append(node)

    return output_nodes

def extract_markdown_images(text):
    #matches = re.findall(r"\!\[(.*?)\]\((.*?)\)",text)
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    #matches = re.findall(r"\[(.*?)\]\((.*?)\)",text)
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
