
class Keys :
    """
    Conjunto de variables claves del analizador
    """
    
    VACIO = "VACIO"
    OR = "|"
    PLUS = "+"
    STAR = "*"
    CONCAT = "."
    NONE_OR_ONE = "?"
    
    def __init__ (self) :
        self.operadores_binarios = "|."
        self.operadores_unarios = "+*?"
        self.agrupadores = "()"
        self.operadores =  self.operadores_binarios + \
                           self.operadores_unarios + \
                           self.agrupadores
        self.alfabeto = "abcd"
        self.definicion_regular = "$"
