import sys
import re

reserved = ["println"]

class SymbolTable():
    def __init__(self):
        self.st = dict()
    
    def setter(self, key, value):
        self.st.update({key: value})
    
    def getter(self, key):
        if key in self.st.keys():
            return self.st.get(key)
        else:
            raise ValueError("Erro Semantico")

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
        while self.position < len(self.origin) and (self.origin[self.position] == ' ' or self.origin[self.position] == '\n'):
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
        
        elif self.origin[self.position] == "=":
            self.position += 1
            self.actual = Token('ASSIGNMENT','=')

        elif self.origin[self.position] == ";":
            self.position += 1
            self.actual = Token('SEPARATOR',';')

        elif self.origin[self.position].isalpha():
            var = ""
            while self.position < len(self.origin) and ( self.origin[self.position].isalpha() or self.origin[self.position].isnumeric() or self.origin[self.position] == "_"):
                var = var + self.origin[self.position]
                self.position += 1
    
            if var not in reserved:
                self.actual = Token('IDENTIFIER', var)
        
            else:
                self.actual = Token(var.upper(), var)
                
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
            return IntVal(result, [])
        
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
            result = Parser.factor()
            return UnOp('+', [result]) 

        elif Parser.tokens.actual.type == "MINUS":
            Parser.tokens.selectNext()
            result = Parser.factor()
            return UnOp('-', [result])

        elif Parser.tokens.actual.type == "IDENTIFIER":
            result = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            return result
        
        else:
            raise ValueError('Erro')

        return result

    @staticmethod
    def term():
        left = Parser.factor()
        while Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV":
            if Parser.tokens.actual.value == "*":
                Parser.tokens.selectNext()
                right = Parser.term()
                left = BinOp('*',[left,right])

            if Parser.tokens.actual.value == "/":
                Parser.tokens.selectNext()
                right = Parser.term()
                left = BinOp('/',[left,right])
        return left

    @staticmethod
    def parseExpression():
        left = Parser.term()
        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
            if Parser.tokens.actual.value == "+":
                Parser.tokens.selectNext()
                right = Parser.term()
                left = BinOp('+',[left,right])

            if Parser.tokens.actual.value == "-":
                Parser.tokens.selectNext()
                right = Parser.term()
                left = BinOp('-',[left,right])
        return left

    @staticmethod
    def command():
        if Parser.tokens.actual.type == "IDENTIFIER":
            identifier = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()

            if Parser.tokens.actual.type == "ASSIGNMENT":
                Parser.tokens.selectNext()
                result = Parser.parseExpression()
                return Assignment("", [identifier, result])
            else:
                raise ValueError("Erro")

        elif Parser.tokens.actual.type == "PRINTLN":
            Parser.tokens.selectNext()
            
            if Parser.tokens.actual.type == "OPEN":
                Parser.tokens.selectNext()
                result = Parser.parseExpression()
                if Parser.tokens.actual.type == "CLOSE":
                    Parser.tokens.selectNext()
                    return Println('', [result])
                else:
                    raise ValueError("Erro")
        else:
            return NoOp("",[])

    @staticmethod
    def block():
        children = []
        
        while Parser.tokens.actual.type != "EOF":
            children.append(Parser.command())

            if Parser.tokens.actual.type == "SEPARATOR":
                Parser.tokens.selectNext()
            else:
                raise ValueError("Error: ;")

        if Parser.tokens.actual.type == "EOF":
            return Statements("", children)

        else:
            raise ValueError("Erro")

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        result = Parser.block()
        symbol_table = SymbolTable()
        return result.Evaluate(symbol_table)

class Node:
    def __init__(self, _value, _children):
        self.value = _value
        self.children = _children
    
    def Evaluate(self, symbol_table):
        pass

class Identifier(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, symbol_table):
        st = symbol_table.getter(self.value)
        return st 

class Assignment(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbol_table):
        key = self.children[0].value
        value = self.children[1].Evaluate(symbol_table)
        symbol_table.setter(key, value)

class Println(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, symbol_table):
        print(int(self.children[0].Evaluate(symbol_table)))

class Statements(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, symbol_table):        
        for child in self.children:
            # print(child)
            child.Evaluate(symbol_table)

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, symbol_table):
        if self.value == "+":
            return self.children[0].Evaluate(symbol_table) + self.children[1].Evaluate(symbol_table)
        elif self.value == "-":
            return self.children[0].Evaluate(symbol_table) - self.children[1].Evaluate(symbol_table)
        elif self.value == "*":
            return self.children[0].Evaluate(symbol_table) * self.children[1].Evaluate(symbol_table)
        elif self.value == "/":
            return self.children[0].Evaluate(symbol_table) / self.children[1].Evaluate(symbol_table)
        else:
            raise ValueError('Erro')
        
class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbol_table):
        if self.value == "+":
            return self.children[0].Evaluate(symbol_table)
        elif self.value == "-":
            return -self.children[0].Evaluate(symbol_table)
        else:
            raise ValueError('Erro')

class IntVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, symbol_table):
        return self.value

class NoOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbol_table):
        pass

class PrePro:
    @staticmethod
    def filter(code):
        return re.sub(r'/\*.*?\*/',"", code)

def main(file_name):
    code = open(file_name, 'r').read()
    code = PrePro.filter(code)
    result = Parser.run(code)
    return result

if __name__ == "__main__":
    res = main(sys.argv[1:][0])
