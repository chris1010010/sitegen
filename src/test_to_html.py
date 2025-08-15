import unittest
from convert import markdown_to_html_node


class TestToHtml(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        #print("///////////////////////////")
        #print(html)
        #print("///////////////////////////")

        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_ul(self):
        md = """
- List item 1
- List **item 2**
- List item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>List item 1</li><li>List <b>item 2</b></li><li>List item 3</li></ul></div>",
        )


    def test_ol(self):
        md = """
Ordered list:

1. List item 1
2. List _item 2_
3. List item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Ordered list:</p><ol><li>List item 1</li><li>List <i>item 2</i></li><li>List item 3</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()