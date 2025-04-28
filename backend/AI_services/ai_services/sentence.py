from typing import List

__all__ = ("Token", "SentenceProposal")


class Token(object):
    """
    A class representing a token in the text.
    Each token has a text representation and a span indicating its start
    and end positions in the original text.
    """

    def __init__(self, text: str, start: int, end: int):
        """
        Initialize a Token instance.
        Args:
            text (str): The text of the token.
            start (int): The starting position of the token in the original text.
            end (int): The ending position of the token in the original text.
        """
        self.text = text
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Token(text={self.text}, span=({self.start}, {self.end}))"

    def __str__(self):
        return self.text


class SentenceProposal(str):
    """
    A class representing a sentence proposal.
    It inherits from str and contains additional attributes for
    the tokens that make up the sentence and its index.
    The sentence proposal is created by joining the tokens together,
    taking care to handle spaces and punctuation correctly.
    """

    def __new__(cls, tokens: List[Token], index: int):
        sentence_text = ""
        for i, token in enumerate(tokens):
            if i == 0:
                sentence_text += token.text
                continue
            if token.text and token.text[0].isalnum():
                sentence_text += ' ' + token.text
            else:
                sentence_text += token.text

        obj = super(SentenceProposal, cls).__new__(cls, sentence_text)
        obj.tokens = tokens
        obj.index = index
        return obj

    def __repr__(self) -> str:
        return f"SentenceProposal(index={self.index}, text={str(self)!r}, tokens={self.tokens})"

    def __str__(self):
        return super().__str__()
