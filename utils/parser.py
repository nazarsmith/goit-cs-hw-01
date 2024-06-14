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
        """Парсер для 'term' правил граматики. У нашому випадку - це цілі числа."""
        token = self.current_token
        self.advance(TokenType.INTEGER)
        return Num(token)

    def factor(self, token):
        self.advance(token.type)  # перейти до наступного токену після дужок
        node = (
            self.term()
        )  # вважатимемо, що токен - це інт і використаймо його як наступний лівий символ в ноді BinOp
        token = self.current_token
        if token.type == TokenType.LPAREN:
            node = self.factor(token)
        elif token.type in (
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.MUL,
            TokenType.DIV,
        ):
            self.advance(token.type)
        node = BinOp(left=node, op=token, right=self.term())
        return node

    def expr(self):
        """Парсер для арифметичних виразів."""
        if self.current_token.type == TokenType.LPAREN:
            node = self.factor(
                self.current_token
            )  # повертає нод який буде використаний як лівий нод в BinOp
        elif self.current_token.type == TokenType.RPAREN:
            self.error()
        else:
            node = self.term()
        while self.current_token.type in (
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.MUL,
            TokenType.DIV,
            TokenType.LPAREN,
            TokenType.RPAREN,
        ):
            token = self.current_token
            print(token.type)
            if token.type == TokenType.PLUS:
                self.advance(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.advance(TokenType.MINUS)
            elif token.type == TokenType.MUL:
                self.advance(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.advance(TokenType.DIV)
            elif token.type == TokenType.LPAREN:
                node = self.factor(token)
            elif token.type == TokenType.RPAREN:
                self.advance(token.type)
                if self.current_token.type != TokenType.EOF:
                    continue
                else:
                    return node
            try:
                right = self.term()
            except:
                right = self.factor(self.current_token)
            node = BinOp(left=node, op=token, right=right)

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
