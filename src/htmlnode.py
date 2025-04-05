# python imports

# application imports


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # "p", "a", "h1", etc
        self.value = value  # text in tag
        self.children = children  # list of HTMLNode objects children of this node
        self.props = props  # dict attributes of HTML tag
        # For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        # for now just raise error instead of pass
        raise NotImplementedError

    def props_to_html(self):
        """
        return a string that represents the HTML of attributes of the node

        {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        returns (leading space before key):
         href="https://www.google.com" target="_blank"
        """
        if self.props is None:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        """print an HTMLNode object and see its tag, value, children, and props.
        This will be useful for your debugging.
        """
        return f"HTMLNode(tag={self.tag}, value={self.value}, " f"children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return f"{self.value}"
        # h1-h6, p, b, etc (no link) should not have props
        # with props (for our current stuff should be like href, a)
        if self.props:
            prop_string = super().props_to_html()
            return f"<{self.tag}{prop_string}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: missing tag")
        if self.children is None:
            raise ValueError("No children html elements")

        child_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"

    def __repr__(self):
        # Optional but helpful for debugging
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
