import sys
import re

def main(argv):
    try:
        
        n = re.split("[+-]", argv[0])
        print(n)

        for i in range(len(n)):
            count = 0
            for e in n[i].split(" "):
                if e.isnumeric():
                    count +=1
                if count > 1:
                    print("[ERRO] numero separado por espaço")
                    break
            
            if n[i].replace(" ","").isnumeric() == False:
                n[i] = '0'
            n[i] = n[i].replace(" ","")
        print(n)
        
        op = []
        operations = ['+','-']

        for i in argv[0]:
            if i in operations:
                op.append(i)
        print(op)

        if len(n) > 1:
            calc = float(n[0])
            for i in range(len(n) - 1):
                if op[i] == '+':
                    calc += float(n[i + 1])
                elif op[i] == '-':
                    calc -= float(n[i + 1])
        else:
            calc = float(n[0])
        print(calc)
    except:
        print("Error")

if __name__ == "__main__":
   main(sys.argv[1:])