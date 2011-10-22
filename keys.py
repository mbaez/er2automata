#! /usr/bin/env python
# -*- coding: utf-8 -*-

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

    def __init__ (self) :
        self.operadores_binarios = "|."
        self.operadores_unarios = "+*?"
        self.agrupadores = "()"
        self.operadores =  self.operadores_binarios + \
                           self.operadores_unarios + \
                           self.agrupadores
        self.alfabeto = "abcd"
        self.definicion_regular = "$"
