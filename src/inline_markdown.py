import re
from enum import Enum

from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"


def block_to_block_type(block: str) -> BlockType:
    if re.fullmatch(r"#{1,6} .+", block):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.splitlines()
    if lines and all(re.fullmatch(r"> ?.*", line) for line in lines):
        return BlockType.QUOTE

    if lines and all(re.fullmatch(r"- .+", line) for line in lines):
        return BlockType.UNORDERED_LIST

    if lines and all(
        re.fullmatch(rf"{index}\. .+", line)
        for index, line in enumerate(lines, start=1)
    ):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_markdown(old_nodes, extract_markdown_images, TextType.IMAGE)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_markdown(old_nodes, extract_markdown_links, TextType.LINK)


def _split_nodes_markdown(
    old_nodes: list[TextNode],
    extractor,
    text_type: TextType,
) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        matches = extractor(text)
        if not matches:
            new_nodes.append(old_node)
            continue

        remaining = text
        for alt_text, url in matches:
            markdown = (
                f"![{alt_text}]({url})"
                if text_type == TextType.IMAGE
                else f"[{alt_text}]({url})"
            )
            before, _, after = remaining.partition(markdown)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt_text, text_type, url))
            remaining = after

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    cleaned = []
    for block in blocks:
        stripped = block.strip()
        if stripped:
            cleaned.append(stripped)
    return cleaned


def text_to_children(text: str) -> list[ParentNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def markdown_to_html_node(markdown: str) -> ParentNode:
    root = ParentNode("div", [])
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            level = len(block) - len(block.lstrip("#"))
            text = block[level + 1 :].strip()
            root.children.append(ParentNode(f"h{level}", text_to_children(text)))
        elif block_type == BlockType.CODE:
            code_text = block[4:-3]
            code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
            root.children.append(ParentNode("pre", [code_node]))
        elif block_type == BlockType.QUOTE:
            quote_text = " ".join(
                line.lstrip().lstrip("> ").lstrip(">").strip()
                for line in block.splitlines()
            )
            root.children.append(ParentNode("blockquote", text_to_children(quote_text)))
        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in block.splitlines():
                item_text = line[2:]
                items.append(ParentNode("li", text_to_children(item_text)))
            root.children.append(ParentNode("ul", items))
        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in block.splitlines():
                item_text = re.sub(r"^\d+\. ", "", line)
                items.append(ParentNode("li", text_to_children(item_text)))
            root.children.append(ParentNode("ol", items))
        else:
            paragraph_text = block.replace("\n", " ")
            root.children.append(ParentNode("p", text_to_children(paragraph_text)))

    return root


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """Split text nodes on a delimiter and preserve surrounding text."""
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(
                f"Invalid markdown syntax: matching closing delimiter '{delimiter}' not found"
            )

        for i, section in enumerate(sections):
            if section == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(section, TextType.TEXT))
            else:
                new_nodes.append(TextNode(section, text_type))

    return new_nodes
