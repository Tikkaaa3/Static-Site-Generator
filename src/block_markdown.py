from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    # Heading check (only first line)
    first_line = lines[0]
    if first_line.startswith("#"):
        # count number of '#' at the start before a space
        count = 0
        for ch in first_line:
            if ch == "#":
                count += 1
            else:
                break
        if 1 <= count <= 6 and first_line[count : count + 1] == " ":
            return BlockType.HEADING

    # Code block: starts and ends with ```
    if len(lines) >= 2 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE

    # Quote: every line starts with '>'
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with '- '
    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST

    # Ordered list: lines start with 1., 2., 3. etc.
    expected_num = 1
    for line in lines:
        prefix = f"{expected_num}."
        if not line.startswith(prefix + " "):
            break
        expected_num += 1
    else:
        # all lines matched the sequence
        return BlockType.OLIST

    # fallback to paragraph
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda s: s.strip(), blocks))
    blocks = [block for block in blocks if block]
    return blocks
