#! /usr/bin/env python
# -*- coding: utf-8 -*-
from keys import *

"""
:author: Maximiniliano Báez González,
:contact: mxbg.py@gmail.com 

:author: Maria Jose Lopez
:contact: majito033@gmail.com
"""

class Estado :
    ID = 1

    def __init__ (self, final=False, id=None, prefijo="E") :
        if id == None:
            self.id = prefijo + str(Estado.ID)
            Estado.ID += 1
        else :
            self.id = id

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
        estado.id = self.id + Keys.COPY_LABEL
        estado.final = self.final

        return estado

    def get_final(self):
        """
        Este método retorna el valor del atributo final del estado

        @rtype  : boolean
        @return : valor del atributo final
        """
        return self.final

    def set_final(self, final):
        """
        Este método esablece el valor del atributo final del estado

        @type  : boolean
        @param : valor del atributo final
        """
        self.final = final

    def __str__(self):
        __id = "(" + str(self.id) + ")"

        if self.final :
            __id = "(" + __id + ")"

        return __id

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
        return str(self.origen) + " == " + self.simbolo +\
               " ==> " + str(self.destino)

class Automata :

    def __init__(self):

        self.estado_inicial = None
        self.estado_final = None
        self.is_sorted = False
        self.index = 0
        self.estados_ordenados = []
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
        for arco in arcos :
            self.estados[arco.origen.id] = arco.origen
            self.estados[arco.destino.id] = arco.destino

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

    def get_estado_inicial(self):
        """
        Este método retorna la referencia al estado inicial del automata

        @rtype  : Estado
        @return : estado inicial del automata
        """
        return self.estado_inicial

    def add_estado_final(self, estado):
        """
        Este método se encarga de establecer el estado final del
        automata y añadir a la lista de estados

        @type estado  : Estado
        @param estado : el estado final del automata.
        """
        self.estado_final = estado
        self.__add_estado(estado)

    def get_estado_final(self):
        """
        Este método retorna la referencia al estado final del automata

        @rtype  : Estado
        @return : estado final del automata
        """
        return self.estado_final


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

        for arco in self.arcos :
            #se copia el estado actual
            src_copy = arco.origen.copy()
            dest_copy = arco.destino.copy()
            #se añade el estado copia al diccionario de estados del
            #automata copia.
            automata.estados[src_copy.id] = src_copy
            automata.estados[dest_copy.id] = dest_copy

        #se obiene el id del estado y se añade la terminación CP que
        #indica que este estado es una copia.
        estado_inicial_str = self.estado_inicial.id + Keys.COPY_LABEL
        estado_final_str = self.estado_final.id + Keys.COPY_LABEL

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
            origen_str = arco.origen.id + Keys.COPY_LABEL
            destino_str = arco.destino.id + Keys.COPY_LABEL

            #Se añade los arcos al automata copia, oteniendo las
            #referencias de los estados copias cuyo id esta definido
            #por origen_str y destino_str

            automata.arcos.append(Arco(automata.estados[origen_str], \
                    automata.estados[destino_str], arco.simbolo))

        #retorna el automata copia
        return automata

    def get_transicion(self, ori_estado) :
        """
        Este método se encarga de obtener un arco a partir del estado
        ori_estado.

        @type ori_estado  : Estado
        @param ori_estado : el estado inicial.

        @rtype  : Arco[]
        @return : los arcos correspondientes al estado ori_estado.
        """
        arc = []
        for arco in self.arcos:
            if (ori_estado.id == arco.origen.id):
                arc.append(arco)

        return arc

    def cantidad_estados(self):
        """
        Este método se encarga de obtener la cantidad de estados del
        AFD.

        @rtype  : Integer
        @return : longitud del AFD

        """
        return len(self.estados)

    def add_estado(self, estado) :
        """
        Este método se encarga de añadir un estado a la lista de estados
        del automata.

        @type estado  : Estado
        @param estado : el estado que será añadido a la lista.
        """
        self.estados[estado.id] = estado

    def get_estado(self, idi):
        """
        Este método se encarga de obtener un estado de la lista de
        estados del automata a partir del id numerico.

        @type idi  : Integer
        @param idi : el id que sera buscado en la lista de estados

        @rtype  : Estado
        @return : el estado obtenido
        """
        est = self.estados[idi]
        return est

    def get_estado_id(self, idi):
        """
        Este método se encarga de obtener un estado de la lista de
        estados del automata a partir del id alfanumerico.

        @type idi  : String
        @param idi : el id que sera buscado en la lista de estados

        @rtype  : Estado
        @return : el estado obtenido
        """
        if self.estados.has_key(idi) : 
            return self.estados[idi]
        
        return None

    def get_estados(self):
        """
        @rtype  : Estado[]
        @return : los estados del automata
        """
        return self.estados

    def get_next_estado(self):
        """
        Este método obiente el siguiente estado de la lista de estados 
        ordenados del automata.
        
        @rtype  : Estado
        @return : el siguiente estado de la lista de estados.
        """
        if not self.is_sorted :
            self.__ordenar_estados__()
        #~ verifica si no se sobrepasa el indice de la lista
        if len(self.estados_ordenados) > self.index :
            #~ se incrementea el puntero
            self.index +=1
            #~ se retorna el estado
            return self.estados_ordenados [self.index-1]
        
        return None


    def reset_index (self) :
        """
        Este método reinicia el puntero de la lista de estados
        """
        self.index = 0

    def __ordenar_estados__(self):
        """
        Este método se encarga de ordenar los estados del automata.
        """
        #~ obtiene el estado inicial del automata
        estado_origen = self.get_estado_inicial()
        #~ añade el estado inicial a la lista de estados ordenados
        self.estados_ordenados.append(estado_origen)
        origenes = []
        #~ se ordenan todos los estados
        while len(self.estados_ordenados) < len(self.estados) - 1 :
            #~ se obienen los estados a los cuales el estado origen 
            #~ posee una transicion
            arcos_destinos = self.get_transicion(estado_origen)
            
            for arco in arcos_destinos :
                #~ para cada transición del estado ordena
                if not self.estados_ordenados.\
                    __contains__(arco.destino) :
                        #~ se añade a la ista de estados ordenados
                        self.estados_ordenados.append(arco.destino)
                        #~ se añade a la lista de posibles estados 
                        #~ origenes para ser evaluados
                        origenes.append(arco.destino)
            
            if len(origenes) > 0 :
                #~ se obtiene el siguiente estado origen
                estado_origen = origenes.pop(0)
        #~ se establece el parametro que indica que esta ordenado
        self.is_sorted = True


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
