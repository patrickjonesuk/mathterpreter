from mathterpreter.lexer import Lexer
from mathterpreter._parser import Parser


def interpret(string: str, use_decimals: bool = True):
    return Parser(Lexer(string, use_decimals).tokenize()).parse().evaluate()
