from textnode import TextType, TextNode
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Text node type not supported")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT or not old_node.text or delimiter not in old_node.text:
            new_nodes.append(old_node)
        else:
            split_res = old_node.text.split(delimiter)
            if len(split_res) % 2 != 1:
                raise Exception("No matching closing delimiter")
            inside = False
            for i in range(len(split_res)):
                if split_res[i]:
                    if not inside:
                        new_nodes.append(TextNode(split_res[i], TextType.TEXT))
                    else: # inside
                        new_nodes.append(TextNode(split_res[i], text_type))
                inside = not inside


    return new_nodes