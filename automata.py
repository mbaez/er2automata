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
    
    def merge (self, estado) : 
        """
        Este método se encarga de fucionar 2 estados, la instancia 
        actual es consumida por el estado que es parametro del método,
        la mescla se realiza sin perder la referencia de los objetos.
        
        @type estado  : Estado
        @param estado : estado con el cual se realizara la fusion
        """
        self.id = estado.id
        self.final = estado.final
        
    def copy(self) :
        """
        Este método genera una copia de la instancia actual.
        
        @rtype  : Estado
        @return : una copia del estado actual
        """
        estado = Estado()
        estado.id = self.id + "CP"
        estado.final = self.final
        
        return estado
    
    def __str__(self):
        return self.id

class Arco :

    def __init__ (self, origen=None, destino=None, simbolo=None) :
        self.simbolo = simbolo
        self.origen = origen
        self.destino = destino
    
    def copy(self):
        """
        Este método genera una copia de la instancia actual.
        
        @rtype  : Arco
        @return : una copia del arco actual
        """
        arco = Arco()
        arco.simbolo = self.simbolo
        
        arco.origen = self.origen.copy()
        arco.destino = self.destino.copy()
        
        return arco

    def __str__(self) :
        """
        Este método formatea la salida de la clase Arco
        
        @rtype  : String
        @return : una cadena con la informacion de los arcos formateados
        """
        return "(" + self.origen.id + ")== " + self.simbolo +\
               " ==>(" + self.destino.id + ")"
        
class Automata : 

    def __init__(self):
        
        self.estado_inicial = None
        self.estado_final = None
        
        self.estados = {}
        self.arcos = []
        
    def add_arcos(self, arcos) :
        """
        Este método se encarga de añadir los arcos a la lista de arcos
        del automata.
        
        @type arcos  : Arco []
        @param arcos : los arcos que serán añadidos a lista de arcos del
                        automata.
        """
        self.arcos += arcos
        
    def __add_estado(self, estado) :
        """
        Este método se encarga de añadir un estado a la lista de estados
        del automata.
        
        @type estado  : Estado
        @param estado : el estado que será añadido a la lista.
        """
        self.estados[estado.id] = estado
        
    def add_estado_inicial(self, estado):
        """
        Este método se encarga de establecer el estado inicial del 
        automata y añadir a la lista de estados
        
        @type estado  : Estado
        @param estado : el estado inicial del automata.
        """
        self.estado_inicial = estado
        self.__add_estado(estado)
        
    def add_estado_final(self, estado): 
        """
        Este método se encarga de establecer el estado final del 
        automata y añadir a la lista de estados
        
        @type estado  : Estado
        @param estado : el estado final del automata.
        """
        self.estado_final = estado
        self.__add_estado(estado)
        
    def add_transicion(self, ori_estado, sig_estado, simbolo):
        """
        Este método se encarga de añadir un arco entre los estados
        ori_estado y sig_estado, mediante el caracter de transición 
        simbolo. Posteriormente los estados son añadidos a la lista de 
        estados del automata.
        
        @type ori_estado  : Estado
        @param ori_estado : el estado inicial.
        
        @type sig_estado  : Estado
        @param sig_estado : el estado final.
        
        @type simbolo  : String
        @param simbolo : el simbolo que indica la transicion del estado
                        ori_estado al sig_estado.
        """
        self.estados[ori_estado.id] = ori_estado
        self.estados[sig_estado.id] = sig_estado
        
        self.arcos.append(Arco(ori_estado, sig_estado, simbolo))
        
    def copy(self) :
        """
        Este método genera una copia de la instancia actual.
        
        @rtype  : Automata
        @return : una copia del automata actual
        """
        #se crea un automata que sera la copia a retornar
        automata =  Automata()
        
        for estado in self.estados.values() :
            #se copia el estado actual
            copy = estado.copy()
            #se añade el estado copia al diccionario de estados del 
            #automata copia.
            automata.estados[copy.id] = copy
        #se obiene el id del estado y se añade la terminación CP que 
        #indica que este estado es una copia.
        estado_inicial_str = self.estado_inicial.id + "CP"
        estado_final_str = self.estado_final.id + "CP"
        
        #se establecen los estados inicial y final de automata copia.
        #Los estados inicial y final son obtenidos de la lista de 
        #estados del automata copia, mediante el id generado 
        #anteriormente. La obtención de los estados se realiza desta 
        #forma para mantener las referencias entre los objetos
        automata.estado_inicial = automata.estados[estado_inicial_str]
        automata.estado_final = automata.estados[estado_final_str]
                
        for arco in self.arcos :
            #por cada arco existente se obtiene los id's de los estados
            #inicial y final y se les concatena el caracter CP para 
            #generar el id de los estados copia
            origen_str = arco.origen.id + "CP"
            destino_str = arco.destino.id + "CP"
            
            #Se añade los arcos al automata copia, oteniendo las
            #referencias de los estados copias cuyo id esta definido
            #por origen_str y destino_str
            
            automata.arcos.append(Arco(automata.estados[origen_str], \
                    automata.estados[destino_str], arco.simbolo))
 
        #retorna el automata copia
        return automata

    def __str__(self) :
        """
        Este método formatea la salida de la clase Automata
        
        @rtype  : String
        @return : una cadena con la informacion de los estados formateados
        """
        cad = ""
        for arco in self.arcos :
            cad += str(arco) + "\n"
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
                self.plus()
            elif token == Keys.NONE_OR_ONE :
                self.none_or_one()
            elif token == Keys.OR :
                self._or()
            elif token == Keys.CONCAT :
                self.concat()
            else : 
                self.single(token)
            
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
        
    def none_or_one (self) :
        
        self.single(Keys.VACIO)
        self._or()
        
    def plus (self) :
        automata = self.automatas.pop()
        
        self.automatas.append(automata)
        self.automatas.append(automata.copy())

        self.star()
        self.concat()
        
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
        
        
    def __str__(self) :
        cad = ""
        for automata in self.automatas :
            cad += str(automata) +"\n"
        
        cad = cad[0:-1]
        cad += "" 
        return cad

