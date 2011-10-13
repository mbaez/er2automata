
class StringTokenizer :
    """
    Divide un string en substrings o tokens apartir de los siguentes 
    delimitadores o caracteres:
    
    OPERADORES = "|+*?()"
    ALFABETO = Conjunto de carcteres permitidos
    DEFINICION REGULAR = "$"
    """
    
    def __init__ (self, expresion, keys) :
        """
        """
        self.expresion = expresion
        self.tokens = []
        self.token_index = 0
        self.operadores = keys.operadores
        self.alfabeto = keys.alfabeto 
        self.definicion_regular = keys.definicion_regular
        self.__tokenizar__();
        
        
    def __tokenizar__(self) :
        """
        """
        token = ""
        index = 0
        
        while (index < len(self.expresion)) :
            
            c = self.expresion[index]
            
            if self.alfabeto.find(c)>=0 :
                """
                """
                token += c
                self.tokens.append(token)
                token = ""
                
            elif self.operadores.find(c)>=0 :
                """
                """
                self.tokens.append(c)
                token = ""
                
            elif self.definicion_regular.find(c) >=0 :
                """
                """
                end = self.expresion.find(";", index, len(self.expresion))
                self.tokens.append(self.expresion [(index):end])
                index = end 
                token = ""
                
            else :
                """
                """
                print "ERROR: El caracter '" + c + "' no se encuentra definido"
                exit();

            index +=1
    
    def len(self):
        """
        """
        return len (self.tokens)
        
    def get_next_token(self):
        """
        """
        
        if self.token_index >= self.len() :
            return None
            
        token = self.tokens[self.token_index]
        self.token_index += 1
        
        return token
        
