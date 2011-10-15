#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from keys import *
from string_tokenizer import *

DEBUG = False

class Analizador:
    """
    BNF Para una expresion regular
    ===============================================================
    ExpReg    -> Term SubExpReg 
    SubExpReg -> '|'Term SubExpReg | VACIO
    Term      -> Factor OperUna SubTerm | Factor SubTerm
    SubTerm   -> '.' Factor SubTerm | VACIO 
    Factor    -> DefReg | Alfabeto | (ExpReg) 
    OperUna   -> + | * | ? 
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
    
    def start(self): 
        self.exp_reg()
        return True
    
    def exp_reg(self):
        """
         ExpReg -> Term SubExpReg 
        """
        if DEBUG : 
            print "exp_reg -> Token = ", self.token
        self.term();
        self.match(self.token);
        self.sub_exp_reg();
    
    def sub_exp_reg(self):
        """
        SubExpReg -> '|'Term SubExpReg | VACIO
        """
        if DEBUG : 
            print "sub_exp_reg -> Token = ", self.token
        if self.token.find("|") <0 :
            return;
        
        self.term()
        self.match(self.token);
        self.sub_exp_reg();

    def term (self):
        """
        Term -> Factor OperUna SubTerm | Factor SubTerm
        """
        if DEBUG : 
            print "term -> Token = ", self.token
        self.factor();
        while self.tokens.len() > self.index :
            self.match(self.token);
            if self.operadores_unarios.find(self.token) >= 0 :
                self.oper_una();
                self.match(self.token);
            self.sub_term();
        
    def sub_term (self):
        """
        SubTerm   -> '.' Factor SubTerm | VACIO 
        """
        if DEBUG : 
            print "term-> Token = ", self.token
        while self.tokens.len() > self.index :
            if self.token.find(".") < 0 :
                return;
            
            self.oper_bin();
            self.match(self.token);
            self.factor();
            self.match(self.token);
            self.sub_term();
            
    
    def factor(self) :
        """
        Factor    -> DefReg | Alfabeto | (ExpReg)
        """
        if DEBUG : 
            print "factor -> Token = ", self.token
        while self.tokens.len() > self.index :
            if self.token.find(self.definicion_regular) > 0 :
                #self.def_reg();
                if DEBUG : 
                    print "def_reg -> Token = ", self.token
                self.match(self.token)
                return;
            elif self.alfabeto.find(self.token) >= 0 : 
                if DEBUG : 
                    print "alfabeto -> Token = ", self.token
                return;
            else :
                self.match("(")
                self.exp_reg()
                self.match(")")
    
    def oper_bin(self):
        """
        OperBin   -> '|' | . 
        """
        if DEBUG : 
            print "oper_bin-> Token = ", self.token
        if self.operadores_binarios.find(self.token) < 0 :
            print "ERROR DE SINTAXIS, se esperaba un operador binario"
            exit();
            
        
    
    def oper_una(self):
        """
        OperUna   -> + | * | ? 
        """
        if DEBUG : 
            print "oper_una-> Token = ", self.token
        if self.operadores_unarios.find(self.token) < 0 :
            print "ERROR DE SINTAXIS, se esperaba un operador unario"
            exit();
        
    def match (self, t) : 
        """
        Se encarga de consumir el token y solicitar el siguente token
        si es que no existe un error de sintaxis.
        """
        if self.token == t :
            self.index +=1
            if  self.index < self.tokens.len() :
                self.token = self.tokens.get_next_token()
                
            if DEBUG : 
                print "MATCH (" , t, ") -> NEXT( ", self.token,")" 
            return;
            
        else : 
            print "ERROR DE SINTAXIS, inesperado '", t,"' se esperaba '"\
                , self.token, "'" ; exit()
            


if __name__ == "__main__" :
    
    er = "a*(b|c?)*d+a$HOLA;*bcd*"
    
    keys =  keys()
    print "Start.."
    tokens = StringTokenizer (er, keys)
    print er
    a = Analizador(tokens, keys);
    if a.start() :
        print "Done.."
