import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD, "url")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_init(self):
        node = TextNode("Text", TextType.ITALIC, "url")
        self.assertEqual(node.text, "Text")
        self.assertEqual(node.text_type, TextType.ITALIC)
        self.assertEqual(node.url, "url")
    
    def test_repr(self):
        node = TextNode("Text", TextType.CODE, "url")
        self.assertEqual(str(node), "TextNode(Text, code, url)")


if __name__ == "__main__":
    unittest.main()