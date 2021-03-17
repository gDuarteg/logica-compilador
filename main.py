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
        
        else:
            raise ValueError('Erro')
        return self.actual
    
class Parser:
    @staticmethod
    def term():
        if Parser.tokens.actual.type == "INT":
            result = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            
            if Parser.tokens.actual.type == "INT":
                raise ValueError('Erro')
        
            while Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV":
                if Parser.tokens.actual.value == "*":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "INT":
                        result *= Parser.tokens.actual.value
                    else:
                        raise ValueError('Erro')

                if Parser.tokens.actual.value == "/":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "INT":
                        result //= Parser.tokens.actual.value
                    else:
                        raise ValueError('Erro')
        else:
            raise ValueError('Erro')
        return result

    @staticmethod
    def parseExpression():
        
        result = Parser.term()
        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
            if Parser.tokens.actual.value == "+":
                Parser.tokens.selectNext()
                
                if Parser.tokens.actual.type == "INT":
                    result += Parser.term()
                else:
                    raise ValueError('Erro')
            if Parser.tokens.actual.value == "-":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "INT":
                    result -= Parser.term()
                else:
                    raise ValueError('Erro')

        Parser.tokens.selectNext()
        if Parser.tokens.actual.type != "EOF": 
            raise ValueError('Erro')
        return result

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        return Parser.parseExpression()

class PrePro:
    @staticmethod
    def filter(code):
        return re.sub(r'/\*.*?\*/',"", code)

def main(code):
    code = PrePro.filter(code)
    #print(code)
    return Parser.run(code)

if __name__ == "__main__":
   print(main(sys.argv[1:][0]))
