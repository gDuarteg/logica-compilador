import sys
import re

reserved = ["println", "readln", "while", "if", "else", "and", "or", "int", "bool", "string", "true", "false", "return"]

func_st = {}

class SymbolTable():
    def __init__(self):
        self.st = dict()
        # self.last = None
    
    def setter(self, key, value):
        # print(self.st)
        if key in self.st.keys():
            self.st[key][0] = value
            return
        else:
            raise ValueError("Variavel não inicializada")

    def getter(self, key):
        if key in self.st.keys():
            return (self.st.get(key))

        else:
            raise ValueError("Erro Semantico")

    def typer(self, key, type):
        if key in self.st.keys():
            raise ValueError("Variavel já declarada")
        else:
            self.st[key] = [None, type]
            return 
        
class Token:
    def __init__(self, _type, _value):
        self.type = _type
        self.value = _value

class Tokenizer:
    def __init__(self, _origin):
        self.origin = str(_origin)
        self.position = 0
        self.actual = Token("INT", ' ')
        self.PreviousPosition = 0
        self.PreviousActual = Token("INT", ' ')
        self.selectNext()

    def selectPrevious(self):
        self.position = self.PreviousPosition
        self.actual = self.PreviousActual
        return self.actual

    def selectNext(self):
        self.PreviousPosition = self.position
        self.PreviousActual = self.actual

        while self.position < len(self.origin) and (self.origin[self.position].isspace() or self.origin[self.position] == '\n'):
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

        elif self.origin[self.position] == ",":
            self.position += 1
            self.actual = Token('COMMA',',')

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
        
        elif self.origin[self.position] == '"':
            string = ""
            self.position += 1
            while self.origin[self.position] != '"' and self.position < len(self.origin):
                string = string + self.origin[self.position]
                self.position += 1
            self.position += 1
            self.actual = Token('STRING', str(string))


        elif self.origin[self.position].isalpha():
            var = ""
            while self.position < len(self.origin) and ( self.origin[self.position].isalpha() or self.origin[self.position].isnumeric() or self.origin[self.position] == "_"):
                
                var = var + self.origin[self.position]
                self.position += 1
            if var not in reserved:
                self.actual = Token('IDENTIFIER', var)
            else:
                if var == "int" or var == "bool" or var == "string":
                    self.actual = Token("TYPE", var.upper())
                elif var == "true":
                    self.actual = Token("BOOL", True)
                elif var == "false":
                    self.actual = Token("BOOL", False)
                else:
                    self.actual = Token(var.upper(), var)

        else:
            raise ValueError('Erro')
        return self.actual
    
class Parser:
    @staticmethod
    def typeexpr():
        if Parser.tokens.actual.type == "TYPE":
            if Parser.tokens.actual.value == "INT":
                Parser.tokens.selectNext()
                return Type("INT", [])

            if Parser.tokens.actual.value == "BOOL":
                Parser.tokens.selectNext()
                return Type("BOOL", [])

            if Parser.tokens.actual.value == "STRING":
                Parser.tokens.selectNext()
                return Type("STRING", [])

    @staticmethod
    def relexpr():
        left = Parser.parseExpression()
        while Parser.tokens.actual.type == "LESS" or Parser.tokens.actual.type == "BIGGER":
            if Parser.tokens.actual.value == "<":
                Parser.tokens.selectNext()
                right = Parser.parseExpression()
                left = BinOp('<',[left,right])
                return left

            if Parser.tokens.actual.value == ">":
                Parser.tokens.selectNext()
                right = Parser.parseExpression()
                left = BinOp('>',[left,right])
                return left
        return left
    
    @staticmethod
    def eqexpr():
        left = Parser.relexpr() 
        while Parser.tokens.actual.type == "EQUAL":
            if Parser.tokens.actual.value == "==":
                Parser.tokens.selectNext()
                right = Parser.relexpr()
                left = BinOp('==',[left,right])
                return left
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
        
        elif Parser.tokens.actual.type == "BOOL":
            result = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "BOOL":
                raise ValueError('Erro')
            return BoolVal(result, [])

        elif Parser.tokens.actual.type == "STRING":
            # print(Parser.tokens.actual.value)
            result = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            # print(Parser.tokens.actual.value)
            if Parser.tokens.actual.type == "STRING":
                raise ValueError('Erro')
            return StringVal(result, [])

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
            identifier = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            func_var = []
            if Parser.tokens.actual.type == "OPEN":
                Parser.tokens.selectNext()
                while Parser.tokens.actual.type != "CLOSE":
                    func_var.append(Parser.orexpr())
                    if Parser.tokens.actual.type == "COMMA":
                        Parser.tokens.selectNext()
                
                if Parser.tokens.actual.type == "CLOSE":
                    Parser.tokens.selectNext()
                    return FuncCall(identifier.value, func_var)
            else:         
                return identifier

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
                right = Parser.factor()
                left = BinOp('*',[left,right])

            if Parser.tokens.actual.value == "/":
                Parser.tokens.selectNext()
                right = Parser.factor()
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

    @staticmethod #v2.4
    def funcdefblock():
        children = []
        while Parser.tokens.actual.type != "EOF":

            if Parser.tokens.actual.type == "TYPE":
                _type = Parser.typeexpr()
                # Parser.tokens.selectNext()

                if Parser.tokens.actual.type == "IDENTIFIER":
                    identifier = Parser.tokens.actual.value
                    Parser.tokens.selectNext()
                    
                    func_varDec = [TypeVar(identifier,[identifier, _type])]
                    
                    if Parser.tokens.actual.type == "OPEN":
                        Parser.tokens.selectNext()

                        while Parser.tokens.actual.type != "CLOSE":
                            # print("1: ",Parser.tokens.actual.value)
                            if Parser.tokens.actual.type == "TYPE":
                                func_params_type = Parser.typeexpr()
                                # Parser.tokens.selectNext()

                                if Parser.tokens.actual.type == "IDENTIFIER":
                                    func_params_identifier = Parser.tokens.actual.value#Identifier(Parser.tokens.actual.value, [])
                                    func_varDec.append(TypeVar(func_params_identifier, [func_params_identifier, func_params_type]))
                                    Parser.tokens.selectNext()
                                else:
                                    raise ValueError("ERRO  FUNC Type Identifier not found")
                                
                                if Parser.tokens.actual.type == "COMMA":

                                    if Parser.tokens.actual.type == "CLOSE":
                                        raise ValueError("Error: FUNC COMMA")
                                else:
                                    break
                                
                            else:
                                raise ValueError("Error: FUNC TYPE PARAMS")
                            Parser.tokens.selectNext()

                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == "OPEN_BLOCK":
                            func_command = Parser.command()
                            varDec = VarDec("", func_varDec)
                            children.append(FuncDec(identifier, [varDec ,func_command]))
                        else:
                            raise ValueError("Error: FUNC WITHOUT COMMAND")        
                    else:
                        raise ValueError("Error: FUNC OPEN (")
                else:
                    raise ValueError("Error: FUNC IDENTIFIER")
            Parser.tokens.selectNext()

        if Parser.tokens.actual.type == "EOF":
            children.append(FuncCall('main',[]))
            return Statements("", children)

    @staticmethod
    def command():
        if Parser.tokens.actual.type == "OPEN_BLOCK":
            return Parser.block()
        
        elif Parser.tokens.actual.type == "RETURN":
            Parser.tokens.selectNext()
            res = Return("", [Parser.orexpr()])
            if Parser.tokens.actual.type != "SEPARATOR":
                raise ValueError("Erro return ;")

            while Parser.tokens.actual.type != 'CLOSE_BLOCK' or Parser.tokens.actual.type == 'EOF':
                Parser.tokens.selectNext()
            Parser.tokens.selectPrevious()
            return res

        elif Parser.tokens.actual.type == "TYPE":
            _type = Parser.typeexpr()
            if Parser.tokens.actual.type == "IDENTIFIER":
                identifier = Parser.tokens.actual.value#Identifier(Parser.tokens.actual.value, [])
                Parser.tokens.selectNext()
                return TypeVar("", [identifier, _type])
            else:
                raise ValueError("Type Identifier not found")

        elif Parser.tokens.actual.type == "IDENTIFIER":
            identifier = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "ASSIGNMENT":
                Parser.tokens.selectNext()
                result = Parser.orexpr()
                return Assignment("", [identifier, result])

            
            elif Parser.tokens.actual.type == "OPEN":
                Parser.tokens.selectNext()
                func_var = []
                while Parser.tokens.actual.type != "CLOSE":
                    func_var.append(Parser.orexpr())
                    if Parser.tokens.actual.type == "COMMA":
                        Parser.tokens.selectNext()
                
                if Parser.tokens.actual.type == "CLOSE":
                    Parser.tokens.selectNext()
                    return FuncCall(identifier.value, func_var)
            # else:
            #     raise ValueError("Erro Identifier Parenteses")
            
            else:
                raise ValueError("Erro Identifier")

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
                    raise ValueError("while close")
            else:
                raise ValueError("while open")

        elif Parser.tokens.actual.type == "IF":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "OPEN":
                Parser.tokens.selectNext()
                condition = Parser.orexpr()
                if Parser.tokens.actual.type == "CLOSE":
                    Parser.tokens.selectNext()
                    if_com = Parser.command()
                    Parser.tokens.selectNext()
                    
                    if Parser.tokens.actual.type == "ELSE":
                        Parser.tokens.selectNext()
                        else_com = Parser.command()
                        return If('', [condition, if_com, else_com])
                    else:
                        Parser.tokens.selectPrevious()
                        return If('', [condition, if_com])
                else:
                    raise ValueError("Erro")
            else:
                raise ValueError("Erro")

        elif Parser.tokens.actual.type == "ELSE":
            raise ValueError("else without if")
        else:
            return NoOp("",[])

    @staticmethod
    def block():
        children = []
        end_semicolon = ["SEPARATOR", "IDENTIFIER", "PRINTLN", "TYPE"]
        if Parser.tokens.actual.type == "OPEN_BLOCK":
            Parser.tokens.selectNext()

            while Parser.tokens.actual.type != "CLOSE_BLOCK": #or Parser.tokens.actual == "RETURN":
                if Parser.tokens.actual.type in end_semicolon:
                    children.append(Parser.command())
                    if Parser.tokens.actual.type == "SEPARATOR":
                        Parser.tokens.selectNext()
                    else:
                        raise ValueError("Error: ;")
                else:
                    children.append(Parser.command())
                    Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "CLOSE_BLOCK": #or Parser.tokens.actual.type == "EOF":
                # Parser.tokens.selectNext()
                return Statements("", children)
        else:
            raise ValueError("Erro Open {")

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        # result = Parser.block()
        result = Parser.funcdefblock()
        # print(result.children[0].children)
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
        x = self.children[0].Evaluate(symbol_table)
        if x[1] == "BOOL":
            while self.children[0].Evaluate(symbol_table)[0]:
                self.children[1].Evaluate(symbol_table)
        else:
            raise ValueError('While bool')

class If(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbol_table):
        x = self.children[0].Evaluate(symbol_table)
        if x[1] == "STRING":
            raise ValueError('Erro If Type')
        if x[0] == True or (x[1] == "INT" and x[0] != 0):
            return self.children[1].Evaluate(symbol_table)
        elif len(self.children) == 3:
            return self.children[2].Evaluate(symbol_table)

class Identifier(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, symbol_table):
        st = symbol_table.getter(self.value)[0] ############################################################### FIX
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
        txt = self.children[0].Evaluate(symbol_table)
        print(txt[0])

class Readln(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, symbol_table):
        return (int(input()), "INT")

class Statements(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, symbol_table):        
        for child in self.children:
            # print("child: ",child)
            res = child.Evaluate(symbol_table)
            if res=="return":
                return "return"

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, symbol_table):
        x = self.children[0].Evaluate(symbol_table)
        y = self.children[1].Evaluate(symbol_table)
        if x[1] == "INT" and y[1] == "INT":
            if self.value == "+":
                return (x[0] + y[0], "INT")
            elif self.value == "-":
                return (x[0] - y[0], "INT")
            elif self.value == "*":
                return (x[0] * y[0], "INT")
            elif self.value == "/":
                return (x[0] // y[0], "INT")
            elif self.value == ">":
                return (x[0] > y[0], "BOOL")
            elif self.value == "<":
                return (x[0] < y[0], "BOOL")
            elif self.value == "==":
                return (x[0] == y[0], "BOOL")
            elif self.value == "||":
                return (x[0] == y[0], "BOOL")
            elif self.value == "&&":
                return (x[0] == y[0], "BOOL")
            
        elif x[1] == "BOOL" and y[1] == "BOOL":
            if self.value == "&&":
                return (x[0] and y[0], "BOOL")
            elif self.value == "||":
                return (x[0] or y[0], "BOOL")
            elif self.value == "==":
                return (x[0] == y[0], "BOOL")
        
        elif (x[1] == "BOOL" and y[1] == "INT") or (x[1] == "INT" and y[1] == "BOOL"):
            if self.value == "+":
                return (x[0] + y[0], "INT")
            elif self.value == "-":
                return (x[0] - y[0], "INT")
            elif self.value == "*":
                return (x[0] * y[0], "INT")
            elif self.value == "/":
                return (x[0] / y[0], "INT")
            elif self.value == "||":
                return (x[0] or y[0], "INT")
        
        elif (x[1] == "STRING" and y[1] == "INT") or (x[1] == "INT" and y[1] == "STRING"):
            if self.value == "*":
                return (x[0] * y[0], "STRING")
            else:
                raise ValueError('ERRO: BinOp String + INT')
        
        elif x[1] == "STRING" and y[1] == "STRING":
            if self.value == "+":
                return (x[0] + y[0], "STRING")
            if self.value == "==":
                return (x[0] == y[0], "BOOL")
            if self.value == "&&":
                return (x[0] and y[0], "STRING")
            elif self.value == "||":
                return (x[0] or y[0], "STRING")
        else:
            raise ValueError('Erro BinOp')
        
class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbol_table):
        if self.children[0].Evaluate(symbol_table)[1] == "INT":
            if self.value == "+":
                return (self.children[0].Evaluate(symbol_table)[0], "INT")
            elif self.value == "-":
                return (-self.children[0].Evaluate(symbol_table)[0], "INT")
            elif self.value == "!":
                # print(self.children[0].Evaluate(symbol_table))
                return (not self.children[0].Evaluate(symbol_table)[0], "BOOL")
            else:
                raise ValueError('Erro')
        if self.children[0].Evaluate(symbol_table)[1] == "BOOL":
            if self.value == "!":
                return (not self.children[0].Evaluate(symbol_table)[0], "BOOL")


class IntVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, symbol_table):
        return (self.value, "INT")

class BoolVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, symbol_table):
        return (self.value, "BOOL")

class StringVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, symbol_table):
        return (self.value, "STRING")

class Type(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbol_table):
        return (self.value, "TYPE")

class TypeVar(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbol_table):
        symbol_table.typer(self.children[0], self.children[1].Evaluate(symbol_table)[0])

class Return(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, symbol_table):
        symbol_table.st["return"] = self.children
        return "return"


class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, symbol_table):
        # print(self.children)
        for dec in self.children:
            # print(dec.children)
            dec.Evaluate(symbol_table)
        # symbol_table.typer(self.children[0].value, self.children[1].Evaluate(symbol_table)[0])
        # return (self.value, "VARDEC")

class FuncDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbol_table):
        if self.value not in func_st.keys():
            func_st[self.value] = self
        else:
            raise ValueError("Erro FuncDec ja declarada")

class FuncCall(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbol_table):
        # print(func_st)
        # print(self.value)
        new_ST = SymbolTable()
        if self.value not in func_st.keys():
            raise ValueError("Func not dec")
            
        funcDec = func_st[self.value]
        # print(funcDec.children[0].children)

        if len(funcDec.children[0].children)-1 != len(self.children):
            raise ValueError("Func Params Errors")
        
        funcDec.children[0].Evaluate(new_ST)
        # print(new_ST.st)
        # print(func_st)    
        
        for i in range(len(self.children)):
            arg = self.children[i].Evaluate(symbol_table)
            if(new_ST.getter(funcDec.children[0].children[i+1].value)[1] == arg[1]):
                # print(arg)
                new_ST.setter(funcDec.children[0].children[i+1].value, arg)
            else:
                raise ValueError("Erro func call params type")
        funcDec.children[1].Evaluate(new_ST)

        if("return" in new_ST.st):
            res = new_ST.getter("return")[0].Evaluate(new_ST)
            ftype = funcDec.children[0].children[0].children[1].value
            if ftype != res[1]:
                raise ValueError("Error")
            return res

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
