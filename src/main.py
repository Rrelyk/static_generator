from textnode import *
from htmlnode import *

def main():
    test_one = HTMLNode("test1","text","www.www.com", {
    "href": "https://www.google.com",
    "target": "_blank",
})
    test_two = HTMLNode("test1","text","www.www.com")
    test_three = HTMLNode("test3","link","www.333.com")
    print (test_one)
    print (test_two)
    print (test_three)
    print (test_one == test_two)
    print (test_one == test_three)
    print (test_three == test_two)
    print(test_one.props_to_html())

if __name__ == main():
    main()