import sys

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
                # print("aloooooo", num)
                self.position += 1
            self.actual = Token('INT', int(num))

        elif self.origin[self.position] == "+":
            self.position += 1
            self.actual = Token('PLUS','+')
        
        elif self.origin[self.position] == '-':
            self.position += 1
            self.actual = Token('MINUS','-')
        
        else:
            raise ValueError('Erro')
        return self.actual
    
class Parser:
    @staticmethod
    def parseExpression():
        if Parser.tokens.actual.type == "INT":
            result = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            
            while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
                if Parser.tokens.actual.value == "+":
                    Parser.tokens.selectNext()
                    
                    if Parser.tokens.actual.type == "INT":
                        
                        result += Parser.tokens.actual.value
                    else:
                        raise ValueError('Erro')
                if Parser.tokens.actual.value == "-":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "INT":
                        result -= Parser.tokens.actual.value
                    else:
                        raise ValueError('Erro')
                Parser.tokens.selectNext()
            return result
        else: 
            raise ValueError('Erro')

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        return Parser.parseExpression()


def main(argv):
    # print(type(argv[0]))
    # print(argv[0])
    
    return Parser.run(argv[0])


if __name__ == "__main__":
   print(main(sys.argv[1:]))