#! /usr/bin/env python
# -*- coding: utf-8 -*-

from string_tokenizer import *
from automata import *
"""
:author: Maximiniliano Báez González
:contact: mxbg.py@gmail.com
"""

#Variable global que define si se mostran los detalles del proceso
DEBUG = False

class Analizador:
    """
    BNF Para una expresion regular
    ===============================================================
    ExpReg    -> Term SubExpReg
    SubExpReg -> '|' Term {print '|'} SubExpReg | VACIO
    Term      -> Factor SubTerm
    SubTerm   -> '.' Factor {print '.'} SubTerm | VACIO

    Factor    -> DefReg   {print DefReg}   (OperUna|VACIO) |
    Factor    -> Alfabeto {print Alfabeto} (OperUna|VACIO) |
    Factor    -> (ExpReg) (OperUna|VACIO)

    OperUna   -> + | * | ? {print OperUna}
    VACIO     -> ''
    """

    def __init__ (self, tokens, keys):
        self.tokens = tokens
        self.token = self.tokens.get_next_token()
        self.index = 0
        self.operadores_binarios = keys.operadores_binarios
        self.operadores_unarios = keys.operadores_unarios
        self.alfabeto = keys.alfabeto
        self.definicion_regular = keys.definicion_regular
        self.postfija = []

    def start(self):
        """
        Este método inica el analizador sintactico.
        
        @rtype  : Boolean
        @return : True si es que el proceso a finalizado correctamente

        """
        self.exp_reg()
        return True

    def exp_reg(self):
        """
         ExpReg -> Term SubExpReg
        """
        if DEBUG:
            print "exp_reg -> Token = ", self.token
            
        self.term();
        self.sub_exp_reg();

    def sub_exp_reg(self):
        """
        SubExpReg -> '|' Term {print '|'} SubExpReg | VACIO
        """
        if DEBUG:
            print "sub_exp_reg -> Token = ", self.token
            
        if self.token != "|":
            return;

        self.match('|')
        self.term()
        self.postfija.append("|")
        self.sub_exp_reg();

    def term (self):
        """
        Term -> Factor SubTerm
        """
        if DEBUG:
            print "term -> Token = ", self.token

        self.factor();
        self.sub_term();

    def sub_term (self):
        """
        SubTerm   -> '.' Factor {print '.'} SubTerm | VACIO
        """
        if DEBUG:
            print "sub_term-> Token = ", self.token

        if self.token != ".":
            return;

        self.match(".");
        self.factor();
        self.postfija.append(".")
        self.sub_term();


    def factor(self):
        """
        Factor    -> DefReg   {print DefReg}   (OperUna|VACIO) |
        Factor    -> Alfabeto {print Alfabeto} (OperUna|VACIO) |
        Factor    -> (ExpReg) (OperUna|VACIO)
        """
        if DEBUG:
            print "factor -> Token = ", self.token

        if self.token.find(self.definicion_regular) >= 0:
            if DEBUG:
                print "def_reg -> Token = ", self.token
                
            self.postfija.append(self.token)
            self.match(self.token)

        elif self.alfabeto.find(self.token) >= 0:
            if DEBUG:
                print "alfabeto -> Token = ", self.token
                
            self.postfija.append(self.token)
            self.match(self.token)

        else:
            self.match("(")
            self.exp_reg()
            self.match(")")

        if self.operadores_unarios.find(self.token) >= 0:
            self.oper_una()

    def oper_una(self):
        """
        OperUna   -> + | * | ? {print OperUna}
        """

        if DEBUG:
            print "oper_una-> Token = ", self.token

        if self.operadores_unarios.find(self.token) < 0:
            print "ERROR DE SINTAXIS, se esperaba un operador unario"
            exit();
        
        self.postfija.append(self.token)
        self.match(self.token)

    def match (self, t):
        """
        Se encarga de consumir el token y solicitar el siguente token
        si es que no existe un error de sintaxis.
        
        @type  t : String
        @param t : token que se desea consumir.
        """
        if self.token == t:
            self.index += 1
            if  self.index < self.tokens.len():
                self.token = self.tokens.get_next_token()

            if DEBUG:
                print "MATCH ('" + t + "') -> NEXT('" + self.token + "')\n"
                
            return;

        else:
            print "ERROR DE SINTAXIS, inesperado '", t, "' se esperaba '"\
                , self.token, "'"; 
            exit()



if __name__ == "__main__":

    er = "a.b.c.d.a"

    keys = Keys()
    print er
    print "Start.."
    tokens = StringTokenizer (er, keys)
    a = Analizador(tokens, keys);
    if a.start():
        print "Done.." + str(a.postfija)

    t = Thompson(a.postfija)
    t.start()
    print t
    

    #for c in a.postfija:
    
    #postfija += c
    #print postfija
    #print a.postfija
