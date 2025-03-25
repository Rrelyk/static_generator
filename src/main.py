from textnode import *

def main():
    test_one = TextNode("test1","text","www.www.com")
    test_two = TextNode("test1","text","www.www.com")
    test_three = TextNode("test3","link","www.333.com")
    print (test_one)
    print (test_two)
    print (test_three)
    print (test_one == test_two)
    print (test_one == test_three)
    print (test_three == test_two)

if __name__ == main():
    main()