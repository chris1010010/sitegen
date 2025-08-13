from textnode import TextNode, TextType
from convert import text_to_textnodes

def main():
    print("main:")
    #node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    #print(node)

    #test = "`code` bla `code`"
    #print(test.split("`"))

    #extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")

    nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    for node in nodes:
        print(str(node))

main()