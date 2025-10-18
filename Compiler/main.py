from Lexer import lexer
from Parser import Parser
from Evaluator import Interpreter


def main():
    print("====== Mini-C Compiler with AI Assistant ======\n")
    

    
    
    code_lines=open('main.txt','r').read()
    

    
        

    

        #AI suggests fixes or auto-correction before running
   

        
            #Lexer
    tokens = lexer(code)

            #Parser
    parser = Parser(tokens)
    tree = parser.parse_program()

            #Interpreter
    interp = Interpreter()
    interp.eval(tree)

    print(interp)

           
            

        

        

if __name__ == "__main__":
    main()
