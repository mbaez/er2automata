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

class Subconjuntos:

    def __init__(self, afn) :
        self.automatas = []
        self.afn = afn
        self.cola_estados = [] + afn.get_estados().values()
        self.afd_estados_to_afn = {}
        self.afd = Automata()
        self.__estados_d = []
        self.__cola_temp = deque()

    def __cerradura_vacia_inicial(self, estado):
        """
        @type estados  : Estado
        @param estados : el estado inicial.

        @rtype  : Estado[]
        @return : conjunto de estados alcanzados desde el estado 'estado'
        """
        return self.__recorrido_simple(estado, Keys.VACIO)


    def __cerradura_vacia(self, estados):
        """
        @type estados  : Estado[]
        @param estados : los estados inicial.

        @rtype  : Estado[]
        @return : conjunto de estados alcanzados desde el estado 'estado'
        """
        return self.__recorrer(estados, Keys.VACIO)


    def __mover(self, estados, simbolo_buscado):
        """
        @type estado  : Estado
        @param estado : el estado inicial.

        @type simbolo_buscado  : String
        @param simbolo_buscado : simbolo que que genera la transición.

        @rtype  : Estado[]
        @return : conjunto de estados alcanzados desde el estado 'estado'
        """
        return self.__recorrer(estados, simbolo_buscado)

    def __recorrido_simple(self, estado, simbolo_buscado):
        """
        @type estado  : Estado
        @param estado : el estado inicial.

        @type simbolo_buscado  : String
        @param simbolo_buscado : simbolo que que genera la transición.

        @rtype  : Estado[]
        @return : conjunto de estados alcanzados desde el estado 'estado'
        """
        pila = Stack()
        alcanzados = []
        #Si el simbolo buscado es igual al simbolo vacio, debe incluirse
        #el estado actual
        if (simbolo_buscado == Keys.VACIO ):
            alcanzados.append(estado)

        #Meter el estado actual en la pila
        pila.push(estado)

        while not pila.isEmpty() :
            estado = pila.pop()            
            transiciones = self.afn.get_transicion(estado)            
            
            for transicion in transiciones:
                #print "\t\t\t\tA == > " + str(transicion)
                estado_destino = transicion.destino
                simbolo = transicion.simbolo
                #se verifica si el simbolo actual es el buscado
                boolean_simbolo = simbolo == simbolo_buscado

                boolean_alcanzados = alcanzados.__contains__(estado_destino)

                if (boolean_simbolo and not boolean_alcanzados):

                    alcanzados.append(estado_destino)
                    #Si el simbolo buscado es el simbolo vacio, se debe
                    #__recorrer recursivamente los estados alcanzados,
                    #agregando a la pila si esto sucede
                    if (simbolo_buscado == Keys.VACIO):
                        pila.push(estado_destino)

        return alcanzados

    def __recorrer(self, estados, simbolo_buscado):
        """
        @type estados  : Estado[]
        @param estados : conjunto de estados

        @type simbolo_buscado  : String
        @param simbolo_buscado : simbolo que que genera la transición.

        @rtype  : Estado[]
        @return : conjunto de estados alcanzados desde los estados 'estados'
        """
        alcanzados = []
        for e in estados :
            estados_alcanzados = self.__recorrido_simple(e, simbolo_buscado)
            for estado in estados_alcanzados:
                
                if (alcanzados.__contains__(estado) == False):
                    alcanzados.append(estado)

        return alcanzados

    def start_subconjutos(self):
        """
        Este método aplica el algoritmo de subconjuntos al afn definido
        anteriormente para obtener un afd.
        
        @rtype  : Automata
        @return : un afd equivalente al afn definido
        """
        #Calcular la cerradura vacia del Estado inicial
        estado_inicial = self.afn.get_estado_inicial()
        estado_final = self.afn.get_estado_final()

        resultado = self.__cerradura_vacia_inicial(estado_inicial)
        #Agregar la cerradura vacia del estado inicial del AFN a __estados_d
        #sin marcar
        self.__estados_d.append(resultado)
        self.__cola_temp.append(resultado)
        #Se inicia el ciclo principal del algoritmo
        while (self.__cola_temp):
            #Marcar T
            T = self.__cola_temp.popleft()
            #Agregamos el estado al AFD
            t_id = self.__gen_list_id(T)
            #~ se otiene el estado mediante el t_id
            estado_origen = self.get_estado_or_create(t_id)
            __estado = self.afn.get_next_estado()
            #Buscar transiciones por cada simbolo
            for simbolo in Keys.ALFABETO:
                #Aplicar __cerradura_vacia(mueve(T, simbolo))
                M = self.__mover(T, simbolo)
                U = self.__cerradura_vacia(M)
                
                if (self.__estados_d.__contains__(U)):
                    posicion = self.__estados_d.index(U)
                    estado_destino = self.afd_estados_to_afn[posicion]
                elif U:
                    u_id = self.__gen_list_id(U)
                    estado_destino = self.get_estado_or_create(u_id)
                    #Agregar U a __estados_d sin marcar
                    index = len(self.__estados_d)
                    self.afd_estados_to_afn[index] = estado_destino

                    self.__estados_d.append(U)
                    self.__cola_temp.append(U)
                else:
                    continue
                #Se añade el estado inicial del automata
                if self.afd.estado_inicial == None :
                    self.afd.estado_inicial = estado_origen
                #Agregamos la transicion al AFD
                self.afd.add_transicion(estado_origen, estado_destino, simbolo)
        
        self.__rename_estados()
        return self.afd
    
    def __rename_estados (self) :
        """
        Se encarga de renombrar los estados del afd, de forma que tengan
        un id secuencial y no un id resultado de la concatenación de los
        id's de los estados del afn consumidos.
        """ 
        i = 1
        for arco in self.afd.arcos : 
            _estados = [arco.origen, arco.destino]
            for estado in _estados : 
                #~ Se renombra cada estado
                if estado.id.find("(") >= 0 :
                    #~ se genera el nuevo id
                    estado.id = "E" + str(i)
                    #~ se incrementa el id secuencial
                    i+=1
        
    def get_estado_or_create(self, id) : 
        """
        @type id  : String
        @param id : id del estado buscado

        @rtype  : Estado
        @return : un estado identificado por id
        """
        #~ se obtiene del afd, si no existe retorna None
        estado = self.afd.get_estado_id(id)
        #~ si no existe el estado , se crea un nuevo esado identificado
        #~ por el id especificado
        if estado == None :
            estado = Estado(id=id)
        #~ si el id del estado posee doble parentesis es un estado final
        if id.find("((") >= 0 :
            estado.set_final(True)
        #~ se retorna el estado.
        return estado
        
    def __gen_list_id(self, estados) : 
        """
        @type estados  : Estado[]
        @param estados : lista de estados

        @rtype  : String
        @return : una cadena que contiene todos los ids de los estados
                  incluidos en la lista 'estados'
        """
        id_str = ""
        for estado in estados :
            id_str += str(estado) + ", "
        
        #~ se remueve de la cadena la coma y el espacio del final
        return id_str[:-2]
