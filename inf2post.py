#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from keys import *
from string_tokenizer import *
from stack import *
from analizador import *


class inf2post:
    """
    Convierte una notacion infija a postfija
    """
    
    def __init__(self, tokenList, keys):
        """
        tokenList = lista que contiene los tokens en notacion infija
        """
        
        self.tokenList = tokenList
        self.operadores_binarios = keys.operadores_binarios
        self.operadores_unarios = keys.operadores_unarios
        self.operadores = keys.operadores
        self.alfabeto = keys.alfabeto 
        self.pila = Stack()
        self.listaFinal = []
        
        aux = ""
        aux2 = []
        index = 0
        
        while (index < len(self.tokenList)) :
            token = self.tokenList[index]
            
            if self.alfabeto.find(token)>=0 :
                self.listaFinal += token
                
                if DEBUG :
                    print "Token -> ", token
                    print "Lista -> ", self.listaFinal
            
            elif token.find("$") >=0 :
                aux2.append(token)
                self.listaFinal += aux2
                aux2 = ""    
                
                if DEBUG :
                    print "Token -> ", token
                    print "Lista -> ", self.listaFinal
            
            elif token == "(":
                self.pila.push(token)
                
                if DEBUG :
                    print "Token -> ", token
            
            elif token == ")":
                #~ print "Token ->", token
                aux = self.pila.pop()
                self.pila.push(aux)
                while (self.pila.isEmpty()== False and aux != "("):
                    aux = ""
                    aux = self.pila.pop()
                    self.listaFinal += aux
                    aux = ""
                    aux = self.pila.pop()
                    self.pila.push(aux)
                
                if DEBUG :
                    print "Token -> ", token
                    print "Lista -> ", self.listaFinal
                    
                if aux == "(" :
                    aux = self.pila.pop()
                    aux = ""
                else :
                    print "ERROR DE SINAXIS, no se encuentra el operador ("
                    exit()
            
            elif self.operadores.find(token) >= 0:
                    if token == "|" :
                        #~ print "Token ->", token
                        if (self.pila.isEmpty() == True):
                            self.listaFinal += token
                        else :
                            aux = self.pila.getFin()
                            while ((self.pila.isEmpty() == False) and \
                                  (self.operadores_unarios.find(aux) >= 0 or \
                                   self.operadores_binarios.find(aux) >= 0)):
                                aux = ""
                                aux = self.pila.pop()
                                self.listaFinal += aux
                                aux = ""
                                aux = self.pila.getFin()
                            self.pila.push(token)
                            
                            if DEBUG :
                                print "Token ->", token
                                print "Lista -> ", self.listaFinal
                                
                    elif token == "." :
                        #~ print "Token ->", token
                        if (self.pila.isEmpty() == True):
                            self.listaFinal += token
                            if DEBUG :
                                print "Lista -> ", self.listaFinal
                        else :
                            aux = self.pila.getFin()
                            while ((self.pila.isEmpty() == False) and \
                                  (self.operadores_unarios.find(aux) >= 0 or \
                                   token == ".")):
                                aux = ""
                                aux = self.pila.pop()
                                self.listaFinal += aux
                                aux = ""
                                aux = self.pila.getFin()
                            self.pila.push(token)
                            
                            if DEBUG :
                                print "Token ->", token
                                print "Lista -> ", self.listaFinal
                        
                    elif self.operadores_unarios.find(token) >= 0 :
                        #~ print "Token ->", token
                        if (self.pila.isEmpty() == True):
                            self.listaFinal += token
                            if DEBUG :
                                print "Lista -> ", self.listaFinal
                            
                        else :
                            aux = self.pila.getFin()
                            while ((self.pila.isEmpty() == False) and \
                                  (self.operadores_unarios.find(aux) >= 0)):
                                aux = ""
                                aux = self.pila.pop()
                                self.listaFinal += aux
                                aux = ""
                                aux = self.pila.getFin()
                            self.pila.push(token)
                            
                            if DEBUG :
                                print "Token ->", token
                                print "Lista -> ", self.listaFinal
                            
                    else :
                        print "ERROR DE SINTAXIS"
                        exit()
            index +=1
        
        while (self.pila.isEmpty() == False):
            aux = self.pila.pop()
            self.listaFinal += aux
            if DEBUG :
                print "Lista -> ", self.listaFinal
        
        postfija = ""
        for t in self.listaFinal:
            postfija +=t
        print "POSTFIJA -> ", postfija
        
        print "FIN"
