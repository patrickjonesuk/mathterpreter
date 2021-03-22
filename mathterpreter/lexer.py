from decimal import Decimal

from mathterpreter.tokens import Token, TokenType
from mathterpreter.exceptions import MathSyntaxError
from typing import List


class Lexer:
    def __init__(self, string: str = "", use_decimals: bool = True):
        self.string = string
        self.use_decimals = use_decimals
        self.tokens: List[Token] = []

        self._string_iterator = iter(string)
        self._character = None
        self._iterate_string()

    def _iterate_string(self):
        try:
            self._character = next(self._string_iterator)
        except StopIteration:
            self._character = None

    def _get_number(self):
        has_decimal_point = False
        has_exponent = False
        string = self._character
        self._iterate_string()
        while self._character is not None \
                and (self._character.isdigit() or self._character in (".", "e", "+", "-",)):
            if self._character == ".":
                if has_decimal_point:
                    raise MathSyntaxError("Second decimal point in the number",
                                          f"{self.string}\n"
                                          f"{'^'.rjust(self.string.index(self._character) + 1)}")
                else:
                    has_decimal_point = True

            if self._character == "e":
                if has_exponent:
                    raise MathSyntaxError("Second exponent in the number",
                                          f"{self.string}\n"
                                          f"{'^'.rjust(self.string.index(self._character) + 1)}")
                else:
                    has_exponent = True

            if self._character == "+" or self._character == "-":
                if string[-1] != "e":  # exponent is not a previous symbol
                    break

            string += self._character
            self._iterate_string()

        if string.startswith("."):
            string = "0" + string
        if string.endswith(".") or string.endswith("+") or string.endswith("-"):
            string += "0"

        if self.use_decimals:
            return Token(TokenType.NUMBER, Decimal(string))
        else:
            return Token(TokenType.NUMBER, float(string))

    def generate_tokens(self):
        while self._character is not None:
            if self._character in (" ", "\t", "\n"):
                self._iterate_string()
                continue
            elif self._character == "+":
                yield Token(TokenType.ADDITION_OPERATOR)
            elif self._character == "-":
                yield Token(TokenType.SUBTRACTION_OPERATOR)
            elif self._character == "*":
                yield Token(TokenType.MULTIPLICATION_OPERATOR)
            elif self._character == "/":
                yield Token(TokenType.DIVISION_OPERATOR)
            elif self._character in ("**", "^"):
                yield Token(TokenType.POWER_OPERATOR)
            elif self._character in ("sqrt", "√"):
                yield Token(TokenType.SQRT_OPERATOR)
            elif self._character == "(":
                yield Token(TokenType.OPENING_BRACKET)
            elif self._character == ")":
                yield Token(TokenType.CLOSING_BRACKET)
            if self._character in ("-", "+", "*", "/", "**", "^", "sqrt", "√", "(", ")"):
                self._iterate_string()
            elif self._character == "." or self._character.isdigit():
                yield self._get_number()
            else:
                raise MathSyntaxError("Unsupported token",
                                      f"{self.string}\n"
                                      f"{'^'.rjust(self.string.index(self._character) + 1)}")

    def tokenize(self):
        for token in self.generate_tokens():
            self.tokens.append(token)
        return self.tokens

    def __str__(self):
        return "\n".join([z.__str__() for z in self.tokens])
