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
    ")": lambda: TokenType.CLOSING_BRACKET
}


class Lexer:

    def __init__(self, string: str = ""):
        self.string = string
        self.__string = iter(string)
        self.tokens: List[Token] = []
        self.__expanded_tokens = expand(TOKENS)
        self.__character = None
        self.__iterate_string__()

    def __iterate_string__(self, append=False):
        try:
            next_char = next(self.__string)
            self.__character = self.__character + next_char if append else next_char
        except StopIteration:
            self.__character = None


    def generate_tokens(self):
        while self.__character is not None:
            found = False
            if self.__character in (" ", "\t", "\n"):
                self.__iterate_string__()
                continue
            if self.__character in self.__expanded_tokens:
                yield Token(self.__expanded_tokens[self.__character]())
                self.__iterate_string__()
                found = True
            elif self.__character == "." or self.__character.isdigit():
                yield self.__get_number__()
                found = True
            else:
                for token in self.__expanded_tokens:
                    if token.startswith(self.__character):
                        self.__iterate_string__(True)
                        found = True
            if not found:
                raise MathSyntaxError("Unsupported token",
                                      f"{self.string}\n{'^'.rjust(self.string.index(self.__character) + 1)}")

    def tokenize(self):
        for token in self.generate_tokens():
            self.tokens.append(token)
        return self.tokens

    def __get_number__(self):
        decimal = 0
        string = self.__character
        self.__iterate_string__()
        while self.__character is not None and (self.__character.isdigit() or self.__character == ".") and decimal < 2:
            if self.__character == ".":
                decimal += 1

            string += self.__character
            self.__iterate_string__()

        if string.startswith('.'):
            string = '0' + string
        if string.endswith('.'):
            string += '0'

        return Token(TokenType.NUMBER, float(string))

    def __str__(self):
        return "\n".join([z.__str__() for z in self.tokens])
