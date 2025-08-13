import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_without_children(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("div", [])
            parent_node.to_html()

    def test_to_html_without_tag(self):
        with self.assertRaises(ValueError):
            child_node = LeafNode("span", "child")
            parent_node = ParentNode(None, [child_node])
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()