from utils.lexer import Lexer
from utils.parser import Parser, print_ast
from utils.interpreter import Interpreter


def main():
    while True:
        try:
            text = input('Введіть вираз (або "exit" для виходу): ')
            if text.lower() == "exit":
                print("Вихід із програми.")
                break
            lexer = Lexer(text)
            parser = Parser(lexer)

            # tree = parser.expr()
            # print_ast(tree)

            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print("Result:", result)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
