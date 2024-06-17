from utils.models import AST, BinOp, Num
from utils.lexer import TokenType


class ParsingError(Exception):
    pass


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise ParsingError("Помилка синтаксичного аналізу")

    def advance(self, token_type):
        """
        Порівнюємо поточний токен з очікуваним токеном і, якщо вони збігаються,
        переходимо до наступного токена.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def term(self):
        # term: множення та ділення factors
        node = self.factor()

        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.advance(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.advance(TokenType.DIV)
            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        # factor: числа та expr в дужках
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.advance(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.advance(TokenType.LPAREN)
            node = self.expr()
            self.advance(TokenType.RPAREN)
            return node
        else:
            self.error()

    def expr(self):
        # expr: додавання та віднімання terms
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.advance(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.advance(TokenType.MINUS)
            node = BinOp(left=node, op=token, right=self.term())

        return node


def print_ast(node, level=0):
    indent = "  " * level
    if isinstance(node, Num):
        print(f"{indent}Num({node.value})")
    elif isinstance(node, BinOp):
        print(f"{indent}BinOp:")
        print(f"{indent}  left: ")
        print_ast(node.left, level + 2)
        print(f"{indent}  op: {node.op.type}")
        print(f"{indent}  right: ")
        print_ast(node.right, level + 2)
    else:
        print(f"{indent}Unknown node type: {type(node)}")
