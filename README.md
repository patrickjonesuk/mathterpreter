# mathterpreter

#### A lightweight and basic maths interpreter

## Example usage

Basic usage

```python
from mathterpreter import interpret

print(interpret("54-3*(2+1)-3", use_decimals=False))
```

Step by step
```python
from mathterpreter import Lexer, Parser

lexer = Lexer("54-3*(2+1)-3", use_decimals=False)
tokens = lexer.tokenize()
parser = Parser(tokens)
tree = parser.parse()
result = tree.evaluate()
print(result)
```
`use_decimals` determines whether numbers should be handled as `decimal.Decimal` rather than `float` for more accurate but slower calculations. 
Defaults to `True`

Command line
```shell script
python3 -m mathterpreter 54-3*(2+1)-3
# or
echo 54-3*(2+1)-3 | python3 -m mathterpreter
```

### Syntax:
| Operation         | Syntax                            |
| ----------------- | --------------------------------- |
| Addition          | `a+b`                             |
| Subtraction       | `a-b`                             |
| Multiplication    | `a*b`                             |
| Division          | `a/b`                             |
| Exponentiation    | `a^b`                             |
| `a`th root        | `a√b` or `asqrtb`                 |
| Standard Form:    | `aE+b` (shorthand for `a*10^b`)   |


### Constants:
| Symbol(s)         | Value             |
| ----------------- | ---------         |
| π/pi              | 3.141592653589793 |
| e                  | 2.718281828459045 |
##### All constants are just replaced with their value, wrapped in brackets.

