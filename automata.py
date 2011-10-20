#! /usr/bin/env python
# -*- coding: utf-8 -*-
from keys import *

"""
:author: Maximiniliano Báez González
:contact: mxbg.py@gmail.com
"""

class Estado :
    ID = 1
    
    def __init__ (self, final=False) :
        self.id = "E" + str(Estado.ID)
        Estado.ID += 1
        self.final = final
    def __str__(self):
        return self.id

class Arco :

    def __init__ (self, origen=None, destino=None, simbolo=None) :
        self.simbolo = simbolo
        self.origen = origen
        self.destino = destino

    def __str__(self) :
        return "(" + self.origen.id + ")== " + self.simbolo +\
               " ==>(" + self.destino.id + ")"
        
class Automata : 

    def __init__(self):
        
        self.estado_inicial = None
        self.estado_final = None
        
        self.estados = {}
        self.arcos = []
        
    def add_arcos(self, arcos):
        self.arcos += arcos
        
    def __add_estado(self, estado) :
        self.estados[estado.id] = estado
        
    def add_estado_inicial(self, estado): 
        self.estado_inicial = estado
        self.__add_estado(estado)
        
    def add_estado_final(self, estado): 
        self.estado_final = estado
        self.__add_estado(estado)
        
    def add_transicion(self, ori_estado, sig_estado, simbolo):
        
        self.estados[ori_estado.id] = ori_estado
        self.estados[sig_estado.id] = sig_estado
        
        self.arcos.append(Arco(ori_estado, sig_estado, simbolo))
        return

    def __str__(self) :
        cad = ""
        for estado in self.arcos :
            cad += str(estado) + "\n"
        cad = cad[0:-1]
        cad += "" 
        return cad
        
class Thompson :
    
    def __init__(self, tokens_infija) :
        self.automatas = []
        self.tokens_infija = tokens_infija
        self.index = 0
        
    def start(self):
        for token in self.tokens_infija :
            if token == Keys.STAR :
                self.star()
            elif token == Keys.PLUS :
                self.puls()
            elif token == Keys.NONE_OR_ONE :
                self.none_or_one()
            elif token == Keys.OR :
                self._or()
            elif token == Keys.CONCAT :
                self.concat()
            else : 
                self.single(token)
            
    def single(self, simbolo):
        automata =  Automata()
        
        estado_inicial = Estado()
        estado_final = Estado()
        
        automata.estado_inicial = estado_inicial
        automata.estado_final = estado_final
        
        automata.add_transicion(estado_inicial, estado_final, simbolo)
        self.automatas.append(automata)
        
    def _or(self) :
        automata =  Automata()
        
        afnd_final = self.automatas.pop()
        afnd_inicial = self.automatas.pop()
        
        estado_inicial = Estado()
        estado_final = Estado()
        
        automata.add_estado_inicial(estado_inicial)
        automata.add_estado_final(estado_final)
        
        automata.add_transicion(estado_inicial, afnd_inicial.estado_inicial, Keys.VACIO)
        automata.add_transicion(estado_inicial, afnd_final.estado_inicial, Keys.VACIO)
        
        automata.add_arcos(afnd_inicial.arcos)
        automata.add_arcos(afnd_final.arcos)
        
        automata.add_transicion(afnd_inicial.estado_final,estado_final, Keys.VACIO)
        automata.add_transicion(afnd_final.estado_final, estado_final, Keys.VACIO)
        
        
        self.automatas.append(automata)
        
        
        pass
    def concat(self) :
        automata =  Automata()
        
        afnd_final = self.automatas.pop()
        afnd_inicial = self.automatas.pop()
        
        automata.add_estado_inicial(afnd_inicial.estado_inicial)
        automata.add_estado_final(afnd_final.estado_final)
        
        automata.add_arcos(afnd_inicial.arcos)
        
        automata.add_transicion(afnd_inicial.estado_final, afnd_final.estado_inicial, Keys.VACIO)
        
        automata.add_arcos(afnd_final.arcos)
        
        self.automatas.append(automata)
        
    def none_or_one (self) :
        pass
    def plus (self) :
        pass
    def star (self) :
        pass
        
    def __str__(self) :
        cad = ""
        for automata in self.automatas :
            cad += str(automata) +"\n"
        
        cad = cad[0:-1]
        cad += "" 
        return cad

