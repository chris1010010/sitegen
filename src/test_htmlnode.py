import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):

    def test_init(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
    
    def test_repr(self):
        node = HTMLNode("p", "Content")
        self.assertEqual(str(node), "HTMLNode(tag=p, value=Content, children=None, props=None)")

    def test_props_to_html(self):
        node = HTMLNode("p", "v", None, {"id": "id1"})
        self.assertEqual(node.props_to_html(), "id=\"id1\"")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Hello, world!")
        self.assertEqual(node.to_html(), "<div>Hello, world!</div>")

    def test_leaf_to_html_txt(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


if __name__ == "__main__":
    unittest.main()