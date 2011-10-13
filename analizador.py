
"""
BNF

ExpReg    -> Factor OperUna SubExpReg | Factor SubExpReg
SubExpReg -> OperBin Factor SubExpReg | Factor SubExpReg | VACIO
Factor    -> DefReg | Alfabeto | (ExpReg)
OperBin   -> '|' | . 
OperUna   -> + | * | ? 
VACIO     -> ''
"""
OPERADORES_BINARIOS = "|"
OPERADORES_UNARIO = "+*?"
OPERADORES = OPERADORES_BINARIOS + OPERADORES_UNARIO + "()"
ALFABETO = "abcd"
DEFINICION_REGULAR = "$"
DEBUG = True

class Analizador:
    token = None
    index = 0;
    tokens =[]
    def __init__ (self, all_tokens):
        self.tokens = all_tokens
        self.token =  self.tokens[0]
        self.index = 0
        
    def exp_reg(self):
        if DEBUG : 
            print "exp_reg-> Token = ", self.token
        self.factor();
        while len(self.tokens) > self.index :
            self.match(self.token);
            if OPERADORES_UNARIO.find(self.token) >= 0 :
                self.oper_una();
                self.match(self.token);
            self.sub_exp_reg();
        
    def sub_exp_reg(self):
        if DEBUG : 
            print "sub_exp_reg-> Token = ", self.token
        while len(self.tokens) > self.index :
            if OPERADORES_BINARIOS.find(self.token) < 0 :
                return;
            
            self.oper_bin();
            self.match(self.token);
            self.factor();
            self.match(self.token);
            self.sub_exp_reg();
            
    
    def factor(self) :
        if DEBUG : 
            print "factor -> Token = ", self.token
        while len(self.tokens) > self.index :
            if self.token.find(DEFINICION_REGULAR) > 0 :
                #self.def_reg();
                if DEBUG : 
                    print "def_reg -> Token = ", self.token
                self.match(self.token)
                return;
            elif ALFABETO.find(self.token) >= 0 : 
                if DEBUG : 
                    print "alfabeto -> Token = ", self.token
                return;
            else :
                self.match("(")
                self.exp_reg()
                self.match(")")
    
    def oper_bin(self):
        if DEBUG : 
            print "oper_bin-> Token = ", self.token
        if OPERADORES_BINARIOS.find(self.token) < 0 :
            print "ERROR"
            return;
            
        
    
    def oper_una(self):
        if DEBUG : 
            print "oper_una-> Token = ", self.token
        if OPERADORES_UNARIO.find(self.token) < 0 :
            print "ERROR"
            return;
        
    def match (self, t) : 
        if self.token == t :
            self.index +=1
            if  self.index < len(self.tokens) :
                self.token = self.tokens [self.index]
            if DEBUG : 
                print "MATCH (" , t, ") -> NEXT( ", self.token,")" 
            return;
            
        else : print "ERROR DE SINTAXIS, inesperado '", t, "' se esperaba '", self.token, "'" ; exit()
            
        
if __name__ == "__main__" :
    er = "a*(b|c)?d+a$HOLA;bcd*"
    token = ""
    tokens = []
    index = 0
    while (index < len(er)) :
        c = er[index]
        if ALFABETO.find(c)>=0 :
            token += c
            tokens.append(token)
            token = ""
            
        elif OPERADORES.find(c)>=0 :
            tokens.append(c)
            token = ""
            
        elif DEFINICION_REGULAR.find(c) >=0 :
            end = er.find(";", index, len(er))
            tokens.append(er [(index):end])
            index = end 
            token = ""
        else :
            print "ERROR: El caracter '" + c + "' no se encuentra definido"
            exit();

        index +=1

    print er
    print tokens

    a = Analizador(tokens);
    a.exp_reg();
