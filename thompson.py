#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from automata import *
from keys import *
from afn import *
        
class Thompson :
    
    def __init__(self, tokens_infija) :
        self.automatas = []
        self.tokens_infija = tokens_infija
        self.index = 0
        
    def start(self):
        a = Automata()
        for token in self.tokens_infija :
            if token == Keys.STAR :
                a= self.star()
            elif token == Keys.PLUS :
                a= self.plus()
            elif token == Keys.NONE_OR_ONE :
                a= self.none_or_one()
            elif token == Keys.OR :
                a= self._or()
            elif token == Keys.CONCAT :
                a= self.concat()
            else : 
                a= self.single(token)
        
        self.automatas[0].estado_final.final = True
        
        return a
        
    def single(self, simbolo):
        """
        
        @type simbolo  : String 
        @paran simbolo : simbolo que genra una transición entre estados
        """
        automata =  Automata()
        #Se crean los estados inicial y final
        estado_inicial = Estado()
        estado_final = Estado()
        #Se establecen los estados inicial y final
        automata.estado_inicial = estado_inicial
        automata.estado_final = estado_final
        #Se crea un arco entre los estados incial y final con el simbolo
        #de transicion correspondiente.
        automata.add_transicion(estado_inicial, estado_final, simbolo)
        #se añade  el automata a la pila
        self.automatas.append(automata)
        
        return automata
        
    def _or(self) :

        automata =  Automata()
        
        afnd_final = self.automatas.pop()
        afnd_inicial = self.automatas.pop()
        
        estado_inicial = Estado()
        estado_final = Estado()
        
        automata.add_estado_inicial(estado_inicial)
        automata.add_estado_final(estado_final)
        
        automata.add_transicion(estado_inicial, afnd_inicial.estado_inicial,\
                                Keys.VACIO)

        automata.add_transicion(estado_inicial, afnd_final.estado_inicial,\
                                Keys.VACIO)
        
        automata.add_arcos(afnd_inicial.arcos)
        automata.add_arcos(afnd_final.arcos)
        
        automata.add_transicion(afnd_inicial.estado_final,estado_final,\
                                Keys.VACIO)
        automata.add_transicion(afnd_final.estado_final, estado_final,\
                                Keys.VACIO)
        
        
        self.automatas.append(automata)
        
        return automata
        
    def concat(self) :
        automata =  Automata()
        
        afnd_final = self.automatas.pop()
        afnd_inicial = self.automatas.pop()
        
        automata.add_estado_inicial(afnd_inicial.estado_inicial)
        automata.add_estado_final(afnd_final.estado_final)
        #se añade los arcos al automata
        automata.add_arcos(afnd_inicial.arcos)
        automata.add_arcos(afnd_final.arcos)
        #se hace un merge en entre los estados para no generar estados
        #que no son necesarios
        afnd_inicial.estado_final.merge(afnd_final.estado_inicial)
        #se añade el alutomata a la pila
        self.automatas.append(automata)
        
        return automata
        
    def none_or_one (self) :
        
        self.single(Keys.VACIO)
        self._or()
        
        return automata
        
    def plus (self) :
        automata = self.automatas.pop()
        
        self.automatas.append(automata)
        self.automatas.append(automata.copy())

        self.star()
        self.concat()
        
        return automata
        
    def star (self) :
        automata = self.automatas.pop()
        
        self.single(Keys.VACIO)
        
        automata.add_transicion(automata.estado_final,automata.\
                                estado_inicial,Keys.VACIO)
        self.automatas.append(automata)
        
        self.concat()
        self.single(Keys.VACIO)
        self.concat()
        
        automata = self.automatas.pop()
        automata.add_transicion(automata.estado_inicial,automata.\
                                estado_final,Keys.VACIO)
                                
        self.automatas.append(automata)
        
        return automata
        
        
    def __str__(self) :
        cad = ""
        for automata in self.automatas :
            cad += str(automata) +"\n"
        
        cad = cad[0:-1]
        cad += "" 
        return cad

