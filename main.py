import sys
import re

reserved = ["println", "readln", "while", "if", "else", "and", "or"]

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
            if self.origin[self.position + 1] == "=":
                self.position += 2
                self.actual = Token('EQUAL','==')
            else:
                self.position += 1
                self.actual = Token('ASSIGNMENT','=')

        elif self.origin[self.position] == ";":
            self.position += 1
            self.actual = Token('SEPARATOR',';')

        elif self.origin[self.position] == "{":
            self.position += 1
            self.actual = Token('OPEN_BLOCK','{')

        elif self.origin[self.position] == "}":
            self.position += 1
            self.actual = Token('CLOSE_BLOCK','}')

        elif self.origin[self.position] == ">":
            self.position += 1
            self.actual = Token('BIGGER','>')
        
        elif self.origin[self.position] == "<":
            self.position += 1
            self.actual = Token('LESS','<')

        elif self.origin[self.position] == "!":
            self.position += 1
            self.actual = Token('NOT','!')

        elif self.origin[self.position] == "&" and self.origin[self.position + 1] == "&":
            self.position += 2
            self.actual = Token('AND','&&')

        elif self.origin[self.position] == "|" and self.origin[self.position + 1] == "|":
            self.position += 2
            self.actual = Token('OR','||')

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
    def relexpr():
        left = Parser.parseExpression()
        while Parser.tokens.actual.type == "LESS" or Parser.tokens.actual.type == "BIGGER":
            if Parser.tokens.actual.value == "<":
                Parser.tokens.selectNext()
                right = Parser.parseExpression()
                left = BinOp('<',[left,right])

            if Parser.tokens.actual.value == ">":
                Parser.tokens.selectNext()
                right = Parser.parseExpression()
                left = BinOp('>',[left,right])
        return left
    
    @staticmethod
    def eqexpr():
        left = Parser.relexpr() 
        while Parser.tokens.actual.type == "EQUAL":
            if Parser.tokens.actual.value == "==":
                Parser.tokens.selectNext()
                right = Parser.parseExpression()
                left = BinOp('==',[left,right])
        return left

    @staticmethod
    def andexpr():
        left = Parser.eqexpr() 
        while Parser.tokens.actual.type == "AND":
            if Parser.tokens.actual.value == "&&":
                Parser.tokens.selectNext()
                right = Parser.andexpr()
                left = BinOp('&&',[left,right])
        return left

    @staticmethod
    def orexpr():
        left = Parser.andexpr() 
        while Parser.tokens.actual.type == "OR":
            if Parser.tokens.actual.value == "||":
                Parser.tokens.selectNext()
                right = Parser.orexpr()
                left = BinOp('||',[left,right])
        return left

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
            result = Parser.orexpr()
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
        
        elif Parser.tokens.actual.type == "NOT":
            Parser.tokens.selectNext()
            result = Parser.factor()
            return UnOp('!', [result])

        elif Parser.tokens.actual.type == "IDENTIFIER":
            result = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            return result

        elif Parser.tokens.actual.type == "READLN":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "OPEN":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "CLOSE":
                    Parser.tokens.selectNext()
                    return Readln('', [])
                else:
                    raise ValueError("Erro")

        else:
            raise ValueError('Erro')

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
        if Parser.tokens.actual.type == "OPEN_BLOCK":
            return Parser.block()

        elif Parser.tokens.actual.type == "IDENTIFIER":
            identifier = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "ASSIGNMENT":
                Parser.tokens.selectNext()
                result = Parser.orexpr()
                return Assignment("", [identifier, result])
            else:
                raise ValueError("Erro")

        elif Parser.tokens.actual.type == "PRINTLN":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "OPEN":
                Parser.tokens.selectNext()
                result = Parser.orexpr()
                if Parser.tokens.actual.type == "CLOSE":
                    Parser.tokens.selectNext()
                    return Println('', [result])
                else:
                    raise ValueError("Erro")
        
        elif Parser.tokens.actual.type == "WHILE":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "OPEN":
                Parser.tokens.selectNext()
                condition = Parser.orexpr()
                if Parser.tokens.actual.type == "CLOSE":
                    Parser.tokens.selectNext()
                    while_com = Parser.command()
                    return While('', [condition, while_com])
                else:
                    raise ValueError("Erro")

        elif Parser.tokens.actual.type == "IF":
            Parser.tokens.selectNext()
            condition = None
            else_com = None
            if_com = None
            if Parser.tokens.actual.type == "OPEN":
                Parser.tokens.selectNext()
                condition = Parser.orexpr()
                print(Parser.tokens.actual.type)
                if Parser.tokens.actual.type == "CLOSE":
                    Parser.tokens.selectNext()
                    if_com = Parser.command()

                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "ELSE":
                        Parser.tokens.selectNext()
                        else_com = Parser.command()
                        return If('', [condition, if_com, else_com])
                else:
                    raise ValueError("Erro")
            else:
                raise ValueError("Erro")
            return If('', [condition, if_com, else_com])

        else:
            return NoOp("",[])

    @staticmethod
    def block():
        children = []
        end_semicolon = ["SEPARATOR", "IDENTIFIER", "PRINTLN"]
        if Parser.tokens.actual.type == "OPEN_BLOCK":
            Parser.tokens.selectNext()
            while Parser.tokens.actual.type != "CLOSE_BLOCK":
                if Parser.tokens.actual.type in end_semicolon:
                    children.append(Parser.command())
                    if Parser.tokens.actual.type == "SEPARATOR":
                        Parser.tokens.selectNext()
                    else:
                        raise ValueError("Error: ;")
                else:
                    children.append(Parser.command())
                    Parser.tokens.selectNext()

            if Parser.tokens.actual.type == "CLOSE_BLOCK":
                # Parser.tokens.selectNext()
                return Statements("", children)
        else:
            raise ValueError("Erro Open {")

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

class While(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbol_table):
        while self.children[0].Evaluate(symbol_table) == True:
            self.children[1].Evaluate(symbol_table)

class If(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbol_table):
        if self.children[0].Evaluate(symbol_table) == True:
            return self.children[1].Evaluate(symbol_table)
        elif len(self.children) == 3:
            return self.children[2].Evaluate(symbol_table)

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
        print(self.children[0].Evaluate(symbol_table))

class Readln(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, symbol_table):
        return int(input())

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
        elif self.value == "==":
            return self.children[0].Evaluate(symbol_table) == self.children[1].Evaluate(symbol_table)
        elif self.value == "&&":
            return self.children[0].Evaluate(symbol_table) and self.children[1].Evaluate(symbol_table)
        elif self.value == "||":
            return self.children[0].Evaluate(symbol_table) or self.children[1].Evaluate(symbol_table)
        elif self.value == ">":
            return self.children[0].Evaluate(symbol_table) > self.children[1].Evaluate(symbol_table)
        elif self.value == "<":
            return self.children[0].Evaluate(symbol_table) < self.children[1].Evaluate(symbol_table)
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
        elif self.value == "!":
            return not self.children[0].Evaluate(symbol_table)
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
