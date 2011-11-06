#! /usr/bin/env python
# -*- coding: utf-8 -*-

from automata import *
from keys import *
from collections import deque
from stack import *

"""
:author: Maria Jose Lopez
:contact: majito033@gmail.com
"""

class Bnf:
    
    def __init__(self, afd_min):
        self.afd_min = afd_min
        self.estados = [] + afd_min.get_estados().values()
        self.__cola_temp = deque()
        self.lista = ""
        self.bnf = {}
        
        #Renombra el id de los estados
        for es in self.estados:
            print es.id
            es.id = "A" + es.id
            self.__cola_temp.append(es)
        
    def print_bnf(self):
        """
        Este método se encarga de imprimir el BNF resultante
        
        """
        j=0
        while (j <len(self.bnf)):
            print self.bnf[j]
            j+=1
        return self.bnf
        
    def start_bnf(self):
        """
        Este método aplica el algoritmo para covertir un afd minimo en BNF.
        
        """
        
        print "***** BNF ****"
        j = 0
        while (self.__cola_temp):
            
            e = self.__cola_temp.popleft()
            transiciones = self.afd_min.get_transicion(e)
            self.lista = ""
            array = []
            
            for t in transiciones:
                e_destino = t.destino
                e_simbolo = t.simbolo
                
                if (e_simbolo.find(Keys.VACIO) < 0):
                    c = ""
                    c = str(e_simbolo) + str(e_destino.id)
                    array.append(c)
                else:
                    c = ""
                    c = str(e_destino.id)
                    array.append(c)
            
            e_final = self.afd_min.get_estado_final()
                
            if (e.final == True):
                c = "Ɛ"
                array.append(c) 
            
            i = 0
            
            while (i < len(array)-1):
                self.lista += str(array[i]) + "|"
                i += 1
            self.lista += str(array[i])
            
            #Almacena en un array el Bnf
            if (self.lista != ""):
                b = (str(e.id) + "->" + self.lista)
                self.bnf[j] = b
                j +=1


