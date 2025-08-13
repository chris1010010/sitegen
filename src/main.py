from textnode import TextNode, TextType

def main():

    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    print(node)

    #test = "`code` bla `code`"
    #print(test.split("`"))

main()