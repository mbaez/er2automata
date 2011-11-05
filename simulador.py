#! /usr/bin/env python
# -*- coding: utf-8 -*-

from svg_manager import *
from afd_minimo import TablaTransiciones

"""
:author: Maximiniliano Báez González
:contact: mxbg.py@gmail.com
"""

class SimulardorAFD :
    
    def __init__(self, afd, secuencia_caracteres):
        """
        @type afd  : Automata
        @param afd : automata apartir del cual se realiza al simulación
        
        @type secuencia_caracteres  : String
        @param secuencia_caracteres : representa a la cadena de caracteres
                                    a ser utilizados en la simulación.
        """
        self.afd =  afd
        self.svg = SVGManager("afd_.svg")
        #se construye el grafico apartir del afd
        self.svg.gen_svg_from_automata(afd)
        #se procesa el afd
        self.svg.load_nodes()
        #se construye la tabla de transiciones apartir del afd
        self.tabla_transiciones = TablaTransiciones(afd)
        self.tabla_transiciones.build_table()
        #estados que representaran las transiciones
        self.estado_origen = afd.get_estado_inicial()
        self.estado_destino = None
        self.estado_anterior = None
        #el indice del caracter acualtmente procesado
        self.simbol_index = 0
        self.secuencia_caracteres = secuencia_caracteres
   
    def next_state(self): 
        """
        Este metodo realiza la transicion de un estado origen al siguiente
        estado mediante el simbolo de transición especificado por el 
        caracter actual del la secuencia de caracteres.
        
        @rtype  : Boolean
        @return : True si se pudo realizar la transición, en caso contrario
                  retorna False
        """
        #si es el estado inicial se pinta unicamente ese estado
        if self.simbol_index == 0 :
            self.svg.set_node_color(self.estado_origen.id)
            self.svg.write_svg()
            self.simbol_index+=1
            
        elif self.simbol_index  >= 1 and \
            self.simbol_index < len(self.secuencia_caracteres): 
            
            self.__next_state()
        else :
            return False
        
        return True
    
    def previous_state(self): 
        """
        Este metodo realiza la transición de un estado origen al estado 
        que fue procesado anteriormente.
        
        @rtype  : Boolean
        @return : True si se pudo realizar la transición, en caso contrario
                  retorna False
        """
        if self.simbol_index >= 1 and \
            self.simbol_index < len(self.secuencia_caracteres): 
            
            self.__previous_state()
        else :
            return False
        
        return True
            
    def __next_state(self):  
        """
        Este metodo realiza la transicion de un estado origen al siguiente
        estado mediante el simbolo de transición especificado por el 
        caracter actual del la secuencia de caracteres.
        """
        #se obiente el siguiente caracter
        caracter = self.secuencia_caracteres[self.simbol_index]
        #se establece el estado anterior
        self.estado_anterior =  self.estado_origen
        #se obiene el estado destino resultante de la transicion 
        #producida por el simbolo caracter del estado origen
        id = self.estado_origen.id + caracter
        self.estado_destino = self.tabla_transiciones.get_table_value(id)
        #si el estado destino es None ocurrio un error
        if self.estado_destino != None :
            #se reestablece el color del estado origen
            self.svg.set_node_color(self.estado_origen.id, "none")
            #se resalta el color del estado destino
            self.svg.set_node_color(self.estado_destino.id)
            #se actulaiza el svg
            self.svg.write_svg()
            #el estado origen pasa a ser el estado actualmente procesado
            #el estado destino
            self.estado_origen = self.estado_destino
        else :
            #si ocurrio un error se reslata en rojo el color del estado
            #actual
            self.svg.set_node_color(self.estado_origen.id, "#FF0000")
            #se actualiza el svg
            self.svg.write_svg()
        
        self.simbol_index+=1
        
    def __previous_state(self):
        """
        Este metodo realiza la transición de un estado origen al estado 
        que fue procesado anteriormente.
        """
        self.svg.set_node_color(self.estado_origen.id,"none")
        
        if self.estado_anterior != None :
            self.svg.set_node_color(self.estado_anterior.id)
            self.estado_origen = self.estado_anterior
        #se actualiza el indice
        self.simbol_index -= 1
        #se actualiza el svg
        self.svg.write_svg()
