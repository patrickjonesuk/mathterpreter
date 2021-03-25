from decimal import Decimal
import math

from mathterpreter.tokens import Token, TokenType
from mathterpreter.exceptions import MathSyntaxError
from typing import List


def expand(compact_dict):
    result = {}
    for item in compact_dict:
        if isinstance(item, tuple):
            for key in item:
                result[key] = compact_dict[item]
        else:
            result[item] = compact_dict[item]
    return result


TOKENS = {
    "+": lambda: TokenType.ADDITION_OPERATOR,
    "-": lambda: TokenType.SUBTRACTION_OPERATOR,
    "*": lambda: TokenType.MULTIPLICATION_OPERATOR,
    "/": lambda: TokenType.DIVISION_OPERATOR,
    ("sqrt", "√"): lambda: TokenType.SQRT_OPERATOR,
    "^": lambda: TokenType.POWER_OPERATOR,
    "(": lambda: TokenType.OPENING_BRACKET,
    ")": lambda: TokenType.CLOSING_BRACKET,
}
CONSTANTS = {
    ("pi", "π"): lambda: math.pi,
    "e": lambda: math.e,
}

class Lexer:
    def __init__(self, string: str = "", use_decimals: bool = True):
        self.string = string
        self.use_decimals = use_decimals
        self.number_type = Decimal if use_decimals else float
        self.tokens: List[Token] = []
        self._expanded_tokens = expand(TOKENS)
        self._expanded_constants = expand(CONSTANTS)
        self._string_iterator = iter(string)
        self._character = None
        self._index = 0
        self._iterate_string()

    def _iterate_string(self, append=False):
        try:
            next_char = next(self._string_iterator)
            self._character = self._character + next_char if append else next_char
            self._index += 1
        except StopIteration:
            self._character = None

    def generate_tokens(self):
        while self._character is not None:
            found = False
            if self._character in (" ", "\t", "\n"):
                self._iterate_string()
                continue
            if self._character in self._expanded_tokens:
                token_types = self._expanded_tokens[self._character]()
                token_types = token_types if isinstance(token_types, list) else [token_types]
                for token_type in token_types:
                    yield token_type if isinstance(token_type, Token) else Token(token_type)
                self._iterate_string()
                found = True
            elif self._character in self._expanded_constants:
                constant = self._expanded_constants[self._character]()
                yield Token(TokenType.OPENING_BRACKET)
                yield Token(TokenType.NUMBER, self.number_type(constant))
                yield Token(TokenType.CLOSING_BRACKET)
                found = True
                self._iterate_string()
            elif self._character == "." or self._character.isdigit():
                yield self._get_number()
                found = True
            else:
                found = self._get_multichar(self._expanded_constants) or self._get_multichar(self._expanded_tokens)
            if not found:
                raise MathSyntaxError("Unsupported token",
                                      f"{self.string}\n{'^'.rjust(self.string.index(self._character) + 1)}")

    def _get_number(self):
        has_decimal_point = False
        has_exponent = False
        string = self._character
        self._iterate_string()
        while self._character is not None \
                and (self._character.isdigit() or self._character in (".", "E", "+", "-",)):
            if self._character == ".":
                if has_decimal_point:
                    raise MathSyntaxError("Second decimal point in the number",
                                          f"{self.string}\n"
                                          f"{'^'.rjust(self.string.index(self._character) + 1)}")
                else:
                    has_decimal_point = True

            if self._character == "E":
                if has_exponent:
                    raise MathSyntaxError("Second exponent in the number",
                                          f"{self.string}\n"
                                          f"{'^'.rjust(self.string.index(self._character) + 1)}")
                else:
                    has_exponent = True

            if self._character == "+" or self._character == "-":
                if string[-1] != "E":  # exponent is not a previous symbol
                    break

            string += self._character
            self._iterate_string()

        if string.startswith("."):
            string = "0" + string
        if string.endswith(".") or string.endswith("+") or string.endswith("-") or string.endswith("E"):
            string += "0"

        return Token(TokenType.NUMBER, self.number_type(string))

    def _get_multichar(self, tokens):
        complete = False
        found_complete = ""
        string_builder = ""
        string_iterator = iter(self.string[self._index-1:])
        while not complete:
            complete = True
            for token in tokens:
                if token.startswith(string_builder):
                    if token == string_builder and len(string_builder) > len(found_complete):
                        found_complete = string_builder
                    try:
                        string_builder += next(string_iterator)
                    except StopIteration:
                        complete = True
                        break
                    complete = False

        found = string_builder if string_builder in tokens else found_complete
        if found:
            for _ in range(len(found)-1):
                self._iterate_string(True)
        return bool(found)

    def tokenize(self):
        for token in self.generate_tokens():
            self.tokens.append(token)
        return self.tokens

    def __str__(self):
        return "\n".join([z.__str__() for z in self.tokens])
