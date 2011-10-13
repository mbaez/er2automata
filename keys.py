
class keys :
    """
    Conjunto de variables claves del analizador
    """
    def __init__ (self) :
        self.operadores_binarios = "|."
        self.operadores_unarios = "+*?"
        self.agrupadores = "()"
        self.operadores =  self.operadores_binarios + \
                           self.operadores_unarios + \
                           self.agrupadores
        self.alfabeto = "abcd"
        self.definicion_regular = "$"
