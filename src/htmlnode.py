class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""
        if self.props:
            for key, val in self.props.items():
                result += f' {key}="{val}"'
        return result

    def __repr__(self):
        return f"[tag:{self.tag}\nvalue:{self.value}\nchildren:{self.children}\nprops:{self.props}]"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value == None:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if tag == None:
            raise ValueError("ParentNode must have a tag")
        if children == None:
            raise ValueError("ParentNode must have children")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        if self.children == None or self.children == []:
            raise ValueError("ParentNode must have children")
        return f"<{self.tag}{super().props_to_html()}>{"".join(map(lambda child: child.to_html(), self.children))}</{self.tag}>"
