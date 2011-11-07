# -*- coding: utf-8 -*-
#! /usr/bin/env python

"""
:author: Maximiniliano Báez González
:contact: mxbg.py@gmail.com
"""
class StringTokenizer:
    """
    Divide un string en substrings o tokens apartir de los siguentes 
    delimitadores o caracteres:
    
    OPERADORES = "|+*?()"
    ALFABETO = Conjunto de carcteres permitidos
    DEFINICION REGULAR = "$"
    """
    
    def __init__ (self, expresion, keys):
        """
        Se encarga de inicializar los atributos de clase.
        
        @type  expresion : String
        @param expresion : la expresion que se desea separar en tokens
        
        @type  keys : Keys
        @param keys : continen los parametros que se necesitan para 
                      separar los tokens.
        """
        self.expresion = expresion
        self.tokens = []
        self.token_index = 0
        self.operadores = keys.operadores
        self.alfabeto = keys.alfabeto 
        self.definicion_regular = keys.definicion_regular
        self.__tokenizar__(keys);
        
        
    def __tokenizar__(self, keys):
        """
        Este método se encarga de separar la cadena en tokens segun 
        los delimitadores y alfabetos definidos.
        
        @type  keys : Keys
        @param keys : continen los parametros que se necesitan para 
                      separar los tokens.
        """
        token = ""
        index = 0
        
        while (index < len(self.expresion)):
            
            #se obtiene el caracter actual
            c = self.expresion[index]
            
            if self.alfabeto.find(c) >= 0:
                
                #Si el caracter pertenece al alfabeto se añade el 
                #caracter al token
                token += c
                self.tokens.append(token)
                #se reinicia el token
                token = ""
                
            elif self.operadores.find(c) >= 0:
                
                #Si el caracter actual es un operador se añade a la 
                #lista de tokens
                self.tokens.append(c)
                #se reinicia el token
                token = ""
                
            elif self.definicion_regular.find(c) >= 0:

                #Si el caracter posee el signo $ inidica que es un 
                #definción regular y por lo tanto debe terminar con el 
                #caracter ';'
                end = self.expresion.find(";", index, len(self.expresion))

                #Si en es menor a cero, la definicion regular no esta 
                #definida correctamente, por lo que se emite un error
                if end < 0 :
                    raise Exception("ERROR: Se esperaba un ';'")
                #Si la definición regular es correcta se añade a la lista 
                #de tokens
                self.tokens.append(self.expresion [(index):end])
                #Se actualiza el indice para que apunte al final de la
                #definición regular
                index = end 
                #se reinicia el token
                token = ""
                
            else:
                #Si el caracter no se encuentra en el alfabeto, no es 
                #un oprador y tampoco definición regular, se emite un 
                #mensaje de error
                
                raise Exception( "ERROR: El caracter '" + c + \
                    "' no se encuentra definido")
                #exit();
            #se incrementa el valor del indice para que apunte al siguiente
            #caracter
            index += 1
        

    
    def len(self):
        """
        Este método se encarga de obtener la cantidad de tokens existentes.
        
        @rtype  : Integer
        @return : la cantidad de tokens
        """
        return len (self.tokens)
        
    def get_next_token(self):
        
        """
        Este método obtiene el siguiente token de la lista y actualiza
        el indice para que apunte al siguiente token.
        
        @rtype  : String
        @return : El siguiente token
        """
        #si no existen mas tokens se retorna none
        if self.token_index >= self.len():
            return None
        
        #se obtiene el siguiente token de la lista
        token = self.tokens[self.token_index]
        
        #Se actualiza el indice para que apunte al siguiente elemento
        self.token_index += 1
        
        #retorna el token 
        return token
        
