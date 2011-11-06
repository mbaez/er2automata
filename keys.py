#! /usr/bin/env python
# -*- coding: utf-8 -*-
from analizador import *
"""
:author: Maximiniliano Báez González
:contact: mxbg.py@gmail.com
"""
class Keys :
    """
    Conjunto de variables claves del analizador
    """

    VACIO = "Ɛ"
    OR = "|"
    PLUS = "+"
    STAR = "*"
    CONCAT = "."
    NONE_OR_ONE = "?"
    COPY_LABEL ="B" 
    ALFABETO = "ab"
    

    def __init__ (self) :
        self.operadores_binarios = "|."
        self.operadores_unarios = "+*?"
        self.agrupadores = "()"
        self.operadores =  self.operadores_binarios + \
                           self.operadores_unarios + \
                           self.agrupadores
        self.alfabeto = "abcd"
        self.definicion_regular = "$"
        self.tabla_simbolos = {}
        self.tabla = {}
        self.j = 0
    
    def get_tabla_simbolos_value_at(self, def_regular):
        """
        Este método apartir de id de una definición regular obtiene
        el valor de la misma en notación postfija.
        
        @type  def_regular: String
        @param def_regular: el id de una definición regular
        
        @rtype  : String
        @return : el valor de la definición regular en notación postfija
        """
        if self.tabla_simbolos.has_key(def_regular) :
            return self.tabla_simbolos[def_regular]
        return None
        
    def set_tabla_simbolos_value_at(self, def_regular, value):
        """
        Este método genera una entrada en la tabla de simbolos con el id
        de la definición regular y establece como el value la expresión
        regular en notación postfija.
        
        @type  def_regular: String
        @param def_regular: el id de una definición regular
        
        @type  value: String
        @param value: la expresión regular que pertenece a la def_regular
        
        @rtype  : String
        @return : el valor de la definición regular en notación postfija
        """
        
        analizar_def_reg = Analizador(value, self);
        
        analizar_def_reg.start()
        
        self.tabla_simbolos[def_regular] = analizar_def_reg.postfija
        
        t = def_regular + "->" + value
        
        self.tabla[self.j] = t
        
        self.j += 1
    
    def print_tabla_simbolos(self):
        
        i = 0 
        while (i<len(self.tabla)):
            print self.tabla[i]
            i += 1
        return self.tabla
