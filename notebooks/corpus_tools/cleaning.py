import re

from typing import Final, Tuple

__all__ = (
    'strip_headers_footers',
    'join_broken_lines',
    'collapse_whitespace',
    'split_paragraphs',
    'clean_and_paragraphize',
)

NEW_PAGE_REG: Final[re.Pattern] = re.compile(r'\s*(\d+|[ivxlcdm]+)\s*')
WHITESPACES_REG: Final[re.Pattern] = re.compile(r'[ \t]+')
PARAGRAPHS_REG: Final[re.Pattern] = re.compile(r'\n{2,}')
LINE_ENDING: Final[Tuple] = ('.', '?', '!', '"', ':', ';')
KEYWORDS: Final[Tuple] = (
    "Cambridge University Press",
    "Cambridge Histories Online",
    "https",
    ""
    "GDZ",
    "RGASPI"
)


def check_keywords(text, *, keywords=KEYWORDS) -> bool:
    for keyword in keywords:
        if keyword in text:
            return True
    return False


def strip_headers_footers(text):
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        if check_keywords(line):
            continue
        if NEW_PAGE_REG.fullmatch(line.strip().lower()):
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


def join_broken_lines(text):
    lines = text.splitlines()
    out_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 < len(lines):
            nxt = lines[i + 1]
            if line and not line.endswith(LINE_ENDING) and nxt and nxt[0].islower():
                line += ' ' + nxt.lstrip()
                i += 1
        out_lines.append(line)
        i += 1
    return "\n".join(out_lines)


def collapse_whitespace(text):
    return WHITESPACES_REG.sub(' ', text)


def split_paragraphs(text):
    return [p.strip() for p in PARAGRAPHS_REG.split(text) if len(p.strip()) > 40]


def clean_and_paragraphize(text):
    text = strip_headers_footers(text)
    text = join_broken_lines(text)
    text = collapse_whitespace(text)
    return split_paragraphs(text)
