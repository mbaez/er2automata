#! /usr/bin/env python
# -*- coding: utf-8 -*-
from keys import *
from automata import *

"""
:author: Maria Jose Lopez
:contact: majito033@gmail.com
"""

class Afd(Automata):

    def __init__(self):
        self.estado_inicial = None
        self.estado_final = None
        
        self.estados = {}
        self.arcos = []    

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
        i = "E"+ str(idi)
        est = self.estados[i]
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
        est = self.estados[idi]
        return est


