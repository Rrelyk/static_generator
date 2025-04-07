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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    output_nodes = []

    def delimiter_text_search(node, delimiter):
        opening_index = node.text.find(delimiter)
        if opening_index == -1:
            if node.text:
                output_nodes.append(node)
            return
        if opening_index != -1:
            #print(f"opening_index found: {opening_index}")
            #print(f"remaining node to search: {node.text[opening_index + 1:]}")
            #find closing delimiter after opening is found
            closing_substring_index = node.text[opening_index + len(delimiter):].find(delimiter)
            if closing_substring_index == -1:
                raise Exception ("No closing Delimiter Found")
            #print(f"closing_index found: {closing_substring_index}")

            #calc actual indices
            closing_index = opening_index + len(delimiter) + closing_substring_index

            #split into 3 parts
            text_before = node.text[:opening_index]
            if text_before != "":
                node_before = TextNode(text_before, node.text_type)
                output_nodes.append(node_before)
            #print(f"before: {text_before}")
            text_between = node.text[opening_index + len(delimiter):closing_index]
            if text_between != "":
                node_between = TextNode(text_between, text_type)
                output_nodes.append(node_between)
            #print(f"between: {text_between}")
            text_after = node.text[closing_index + len(delimiter):]
            #print(f"after: {text_after}")
            #output_nodes.extend([node_before, node_between])
            return delimiter_text_search(TextNode(text_after, node.text_type), delimiter)

    
    for node in old_nodes:
        #print(f"node: {node}")
        match node.text_type:
            case TextType.TEXT:
                #print(f"TextType.TEXT matched, calling delimiter_text_search({node}, {delimiter})")          
                delimiter_text_search(node, delimiter)
            case _:
                output_nodes.append(node)   
    
    #print(f"output_nodes: {output_nodes}")
    return output_nodes

def extract_markdown_images(text):
    #matches = re.findall(r"\!\[(.*?)\]\((.*?)\)",text)
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    #matches = re.findall(r"\[(.*?)\]\((.*?)\)",text)
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
