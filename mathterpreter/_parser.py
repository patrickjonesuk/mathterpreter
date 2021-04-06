from mathterpreter.nodes import *
from mathterpreter.tokens import TokenType, Token
from mathterpreter.exceptions import MathSyntaxError
from typing import List


class Parser:
    def __init__(self, tokens: List[Token]):
        self._tokens = iter(tokens)
        self.token_list = tokens
        self._token = None
        self._index = -1
        self._iterate_token()

    def _iterate_token(self):
        try:
            self._token = next(self._tokens)
            self._index += 1
        except StopIteration:
            self._token = None

    def parse(self):
        if self._token is None:
            return None

        result = self._addition_subtraction_base()

        return result

    def _addition_subtraction_base(self):
        if self._token is None:
            output = ''.join([z.__str__() for z in self.token_list])
            raise MathSyntaxError("Expression expected", f"{output}\n{'^^^'.rjust(len(output) + 3)}")
        result = self._multiplication_division()
        while self._token is not None:
            if self._token.type == TokenType.ADDITION_OPERATOR:
                self._iterate_token()
                result = AdditionNode(result, self._multiplication_division())
            elif self._token.type == TokenType.SUBTRACTION_OPERATOR:
                self._iterate_token()
                result = SubtractionNode(result, self._multiplication_division())
            else:
                break

        return result

    def _multiplication_division_modulo(self):
        result = self._exponentiation_root()

        while self._token is not None:
            if self._token.type == TokenType.MULTIPLICATION_OPERATOR:
                self._iterate_token()
                result = MultiplicationNode(result, self._exponentiation_root())
            elif self._token.type == TokenType.DIVISION_OPERATOR:
                self._iterate_token()
                result = DivisionNode(result, self._exponentiation_root())
            elif self._token.type() == TokenType.MODULO_OPERATOR:
                self._iterate_token()
                result = ModuloNode(result, self._exponentiation_root())
            elif self._token.type == TokenType.OPENING_BRACKET:
                result = MultiplicationNode(result, self._literal_polarity())
            else:
                break

        return result

    def _exponentiation_root_factorial(self):
        result = self._literal_polarity()
        while self._token is not None:
            if self._token.type == TokenType.POWER_OPERATOR:
                self._iterate_token()
                result = ExponentiationNode(result, self._literal_polarity())
            elif self._token.type == TokenType.SQRT_OPERATOR:
                self._iterate_token()
                result = RootNode(result, self._literal_polarity())
            elif self._token.type == TokenType.FACTORIAL_OPERATOR:
                self._iterate_token()
                result = RootNode(result, self._literal_polarity)
            else:
                break
        return result

    def _literal_polarity(self):
        token = self._token
        if token.type == TokenType.OPENING_BRACKET:
            self._iterate_token()
            result = self._addition_subtraction_base()
            self._iterate_token()
            return result

        else:
            self._iterate_token()
            if token.type == TokenType.NUMBER:
                return NumberNode(token.value)

            elif token.type == TokenType.ADDITION_OPERATOR:
                return PositiveNode(self._literal_polarity())

            elif token.type == TokenType.SUBTRACTION_OPERATOR:
                return NegativeNode(self._literal_polarity())
            else:
                output = [z.__str__() for z in self.token_list]
                raise MathSyntaxError("Unexpected token",
                                      f"{''.join(output)}\n"
                                      f"{'^'.rjust(sum([len(z) for z in output[:self._index]]))}")
