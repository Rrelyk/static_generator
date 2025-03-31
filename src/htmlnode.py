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
        return f"HTMLNode(tag='{self.tag}', value='{self.value}', children='{self.children}', props='{self.props}')"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        
        # List of self-closing tags
        self_closing_tags = ["img", "input", "br", "hr", "meta", "link"]

        #open front tag
        front_tag = "<" + self.tag
        #add props if existing
        if self.props:
            for key, value in self.props.items():
                front_tag += f' {key}="{value}"'
    
        # Handle self-closing tags differently
        if self.tag.lower() in self_closing_tags:
            front_tag += " />"
            return front_tag
        else:
            # Close front tag normally for regular tags
            front_tag += ">"
            back_tag = "</" + self.tag + ">"
            return front_tag + self.value + back_tag
    

    

