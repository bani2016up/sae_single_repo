import textwrap

from backend.AI_services.ai_services.corpus_tools.cleaning import (
    strip_headers_footers,
    join_broken_lines,
    clean_and_paragraphize,
)


def test_strip_headers_and_page_numbers():
    raw = textwrap.dedent(
        """
                Cambridge University Press
                123
                
                CONTENT
            """
    ).lstrip()
    assert strip_headers_footers(raw).strip() == "CONTENT"


def test_join_broken_lines_simple():
    raw = "Это строка оборвана\nв середине."
    assert join_broken_lines(raw) == "Это строка оборвана в середине."


def test_clean_and_paragraphize_end_to_end():
    raw = textwrap.dedent(
        """
                Cambridge University Press
                
                Первый абзац. 
                
                Второй абзац
                продолжается на следующей строке.
            """
    ).lstrip()
    paras = clean_and_paragraphize(raw)
    assert paras == [
        "Первый абзац.",
        "Второй абзац продолжается на следующей строке."
    ]

