import sys
import re

class Token:
    def __init__(self, _type, _value):
        self.type = _type
        self.value = _value

class Tokenizer:
    def __init__(self, _origin):
        self.origin = str(_origin)
        self.position = 0
        self.actual = Token("INT", ' ')
        self.selectNext()

    def selectNext(self):
        while self.position < len(self.origin) and self.origin[self.position] == ' ':
            self.position += 1

        if self.position == len(self.origin):
            self.actual = Token('EOF', 'EOF')

        elif self.origin[self.position].isnumeric():
            num = ''
            while self.position < len(self.origin) and self.origin[self.position].isnumeric():
                num = num + self.origin[self.position]
                self.position += 1
            self.actual = Token('INT', int(num))

        elif self.origin[self.position] == "+":
            self.position += 1
            self.actual = Token('PLUS','+')
        
        elif self.origin[self.position] == '-':
            self.position += 1
            self.actual = Token('MINUS','-')
        
        elif self.origin[self.position] == '*':
            self.position += 1
            self.actual = Token('MULT','*')
        
        elif self.origin[self.position] == '/':
            self.position += 1
            self.actual = Token('DIV','/')

        elif self.origin[self.position] == '(':
            self.position += 1
            self.actual = Token('OPEN','(')
        
        elif self.origin[self.position] == ')':
            self.position += 1
            self.actual = Token('CLOSE',')')
        
        else:
            raise ValueError('Erro')
        return self.actual
    
class Parser:
    @staticmethod
    def factor():
        if Parser.tokens.actual.type == "INT":
            result = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            
            if Parser.tokens.actual.type == "INT":
                raise ValueError('Erro')
            return result
        
        elif Parser.tokens.actual.type == "OPEN":
            
            Parser.tokens.selectNext()
            result = Parser.parseExpression()
            if Parser.tokens.actual.type == "CLOSE":
                Parser.tokens.selectNext()
                return result
            else:
                raise ValueError("Erro")
        
        elif Parser.tokens.actual.type == "PLUS":
            Parser.tokens.selectNext()
            return Parser.factor()

        elif Parser.tokens.actual.type == "MINUS":
            Parser.tokens.selectNext()
            return -Parser.factor()

        # print(Parser.tokens.actual.type)
        else:
            raise ValueError('Erro')
        
        return result

    @staticmethod
    def term():
        result = Parser.factor()
        while Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV":
            if Parser.tokens.actual.value == "*":
                Parser.tokens.selectNext()
                result *= Parser.factor()

            if Parser.tokens.actual.value == "/":
                Parser.tokens.selectNext()
                result //= Parser.factor()
        return result

    @staticmethod
    def parseExpression():
        
        result = Parser.term()
        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
            if Parser.tokens.actual.value == "+":
                Parser.tokens.selectNext()
                result += Parser.term()

            if Parser.tokens.actual.value == "-":
                Parser.tokens.selectNext()
                result -= Parser.term()
        return result

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        result = Parser.parseExpression()

        if Parser.tokens.actual.type == "CLOSE": 
            raise ValueError('Erro')
        
        Parser.tokens.selectNext()
        if Parser.tokens.actual.type != "EOF": 
            raise ValueError('Erro')
        return result

class PrePro:
    @staticmethod
    def filter(code):
        return re.sub(r'/\*.*?\*/',"", code)

def main(code):
    code = PrePro.filter(code)
    return Parser.run(code)

if __name__ == "__main__":
   print(main(sys.argv[1:][0]))
