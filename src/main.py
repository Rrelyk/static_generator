from textnode import *
from htmlnode import *

def main():
    test_one = HTMLNode("test1","text","www.www.com", {
    "href": "https://www.google.com",
    "target": "_blank",
})
    test_two = HTMLNode("test1","text","www.www.com")
    test_three = HTMLNode("test3","link","www.333.com")
    leaf_test_one = LeafNode("p", "Hello, world!")
    leaf_test_two = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    leaf_test_three = LeafNode("img", "", {"src":"image.jpg"})
    leaf_test_four = LeafNode(None, "random value",None)
    print (test_one)
    print (test_two)
    print (test_three)
    print (test_one == test_two)
    print (test_one == test_three)
    print (test_three == test_two)
    print(test_one.props_to_html())
    print(leaf_test_one)
    print(leaf_test_one.to_html())
    print(leaf_test_two)
    print(leaf_test_two.to_html())
    print(leaf_test_three)
    print(leaf_test_three.to_html())
    print(leaf_test_four)
    print(leaf_test_four.to_html())

if __name__ == main():
    main()