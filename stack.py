#! /usr/bin/env python 
# -*- coding: utf-8 -*- 

from analizador import *

class Stack : 
    """
    Operaciones sobre una pila
    """
    def __init__(self) : 
        self.items = [] 

    def push(self, item) : 
        self.items.append(item)
        if DEBUG :
            self.imprimir(self.items) 

    def pop(self) : 
        if DEBUG :
            self.imprimir(self.items)
        return self.items.pop() 
        

    def isEmpty(self) : 
        if (self.items == []):
            return True
        else :
            return False
    
    def imprimir(self, items):
        print "Pila ->", items
    
    def getFin(self):
        return self.items[-1]


