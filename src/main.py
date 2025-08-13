from textnode import TextNode, TextType

def main():

    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    print(node)

    #test = "`code` bla `code`"
    #print(test.split("`"))

    #extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")

main()