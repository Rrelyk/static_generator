class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        # First check if 'other' is also a HTMLNode
        if not isinstance(other, HTMLNode):
            return False
        # Then check if all properties are equal
        return (self.tag == other.tag and 
                self.value == other.value and 
                self.children == other.children and
                self.props == other.props) 
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"