import unittest
from textnode import TextNode, TextType
from convert import text_node_to_html_node, split_nodes_delimiter

class TestConvert(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_img(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://u.rl")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://u.rl")
        self.assertEqual(html_node.props["alt"], "Alt text")

    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")

    def test_split_nodes_code2(self):
        node = TextNode("This is text with two `code blocks` word `code block B` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is text with two ")
        self.assertEqual(new_nodes[1].text, "code blocks")
        self.assertEqual(new_nodes[2].text, " word ")
        self.assertEqual(new_nodes[3].text, "code block B")
        self.assertEqual(new_nodes[4].text, " word")
    
    def test_split_nodes_not_found(self):
        node = TextNode("This is text with no tag", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text with no tag")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_split_nodes_invalid(self):
        with self.assertRaises(Exception):
            node = TextNode("This is text with invalid `code block", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)


if __name__ == "__main__":
    unittest.main()