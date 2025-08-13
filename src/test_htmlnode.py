import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()