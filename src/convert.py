import re
from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode
from block import BlockType

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

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT or not old_node.text:
            new_nodes.append(old_node)
        else:
            image_tuples = extract_markdown_images(old_node.text)
            if len(image_tuples) == 0:
                new_nodes.append(old_node)
            else:
                remainin_text = old_node.text
                for tuple in image_tuples:
                    split_res = remainin_text.split(f"![{tuple[0]}]({tuple[1]})", 1)
                    if len(split_res) != 2:
                        raise Exception("Invalid image split")
                    if split_res[0]:
                        new_nodes.append(TextNode(split_res[0], TextType.TEXT))
                    new_nodes.append(TextNode(tuple[0], TextType.IMAGE, tuple[1]))
                    remainin_text = split_res[1]
                if remainin_text:
                    new_nodes.append(TextNode(remainin_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT or not old_node.text:
            new_nodes.append(old_node)
        else:
            link_tuples = extract_markdown_links(old_node.text)
            if len(link_tuples) == 0:
                new_nodes.append(old_node)
            else:
                remainin_text = old_node.text
                for tuple in link_tuples:
                    split_res = remainin_text.split(f"[{tuple[0]}]({tuple[1]})", 1)
                    if len(split_res) != 2:
                        raise Exception("Invalid link split")
                    if split_res[0]:
                        new_nodes.append(TextNode(split_res[0], TextType.TEXT))
                    new_nodes.append(TextNode(tuple[0], TextType.LINK, tuple[1]))
                    remainin_text = split_res[1]
                if remainin_text:
                    new_nodes.append(TextNode(remainin_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    all_nodes = [TextNode(text, TextType.TEXT)]

    all_nodes = split_nodes_delimiter(all_nodes, "**", TextType.BOLD)
    all_nodes = split_nodes_delimiter(all_nodes, "_", TextType.ITALIC)
    all_nodes = split_nodes_delimiter(all_nodes, "`", TextType.CODE)
    all_nodes = split_nodes_image(all_nodes)
    all_nodes = split_nodes_link(all_nodes)

    return all_nodes

def markdown_to_blocks(markdown):
    split_res = markdown.split("\n\n")
    trimmed = map(lambda s: s.strip(), split_res)
    filtered = list(filter(lambda s: s != "", trimmed))
    return filtered

def block_to_block_type(text):
    if re.match(r"#{1,5}\s\w", text):
        return BlockType.HEADING
    if text.startswith("```") and text.endswith("```"):
        return BlockType.CODE
    if text.startswith(">"):
        for line in text.split("\n"):
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if text.startswith("- "):
        for line in text.split("\n"):
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if text.startswith("1. "):
        num = 1
        for line in text.split("\n"):
            if not line.startswith(f"{num}. "):
                return BlockType.PARAGRAPH
            num += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = None

        if block_type == BlockType.PARAGRAPH:
            html_node = ParentNode("p", text_to_children(block.replace("\n", " ")))
        elif block_type == BlockType.HEADING:
            tag, remaining_text = get_heading_tag_and_text(block)
            html_node = ParentNode(tag, text_to_children(remaining_text))
        elif block_type == BlockType.QUOTE:
            html_node = ParentNode("blockquote", text_to_children(block.replace("> ", ""))) #TODO
        elif block_type == BlockType.CODE:
            code_node = ParentNode("code", [text_node_to_html_node(TextNode(block.replace("```\n", "").replace("```", ""), TextType.TEXT))])
            html_node = ParentNode("pre", [code_node])
        elif block_type == BlockType.UNORDERED_LIST:
            html_node = ParentNode("ul", get_unordered_list_items_blocks(block))
        elif block_type == BlockType.ORDERED_LIST:
            html_node = ParentNode("ol", get_ordered_list_items_blocks(block))

        if html_node:
            html_nodes.append(html_node)

    return ParentNode("div", html_nodes)

def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes


def get_heading_tag_and_text(block_text):
    if block_text.startswith("# "):
        return "h1", block_text[2:]
    if block_text.startswith("## "):
        return "h2", block_text[3:]
    if block_text.startswith("### "):
        return "h3", block_text[4:]
    if block_text.startswith("#### "):
        return "h4", block_text[5:]
    if block_text.startswith("##### "):
        return "h5", block_text[6:]
    raise Exception("Invalid heading")

def get_unordered_list_items_blocks(text):
    nodes = []
    for line in text.split("\n"):
        nodes.append(ParentNode("li", text_to_children(line[2:])))
    return nodes

def get_ordered_list_items_blocks(text):
    nodes = []
    for line in text.split("\n"):
        pos = line.index(". ")
        nodes.append(ParentNode("li", text_to_children(line[pos+2:])))
    return nodes
