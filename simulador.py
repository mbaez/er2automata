#! /usr/bin/env python
# -*- coding: utf-8 -*-

from svg_manager import *
from afd_minimo import TablaTransiciones
from keys import Keys

"""
:author: Maximiniliano Báez González
:contact: mxbg.py@gmail.com
"""

class SimuladorAFD :
    
    def __init__(self, afd, secuencia_caracteres, svg_file):
        """
        @type afd  : Automata
        @param afd : automata apartir del cual se realiza al simulación
        
        @type secuencia_caracteres  : String
        @param secuencia_caracteres : representa a la cadena de caracteres
                                    a ser utilizados en la simulación.
                                    
        @type svg_file  : String
        @param svg_file : nombre del archivo de salida
        """
        self.afd =  afd
        self.svg = SVGManager(svg_file)
        #se construye el grafico apartir del afd
        self.svg.gen_svg_from_automata(afd)
        #se procesa el afd
        self.svg.load_nodes()
        #se construye la tabla de transiciones apartir del afd
        self.tabla_transiciones = TablaTransiciones(afd)
        self.tabla_transiciones.build_table()
        #estados que representaran las transiciones
        self.estado_origen = self.afd.get_estado_inicial()
        self.estado_destino = None
        self.estado_anterior = {}
        #el indice del caracter acualtmente procesado
        self.simbol_index = -1
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
        if self.simbol_index == -1 :
            print self.svg.svg_file_name
            self.svg.set_node_color(self.estado_origen.id)
            self.svg.write_svg()
            self.simbol_index += 1
            print self.estado_origen
            
        elif self.simbol_index  >= 0 and \
            self.simbol_index < len(self.secuencia_caracteres): 
            print "next"
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
        if self.simbol_index >= 0: 
            
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
        self.estado_anterior[str(self.simbol_index)] =  self.estado_origen
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
        if (self.simbol_index - 1) >= 0 :
            self.svg.set_node_color(self.estado_origen.id,"none")
            id = str(self.simbol_index - 1)
            if self.estado_anterior.has_key(id) :
                self.simbol_index -= 1
                self.svg.set_node_color(self.estado_anterior[id].id)
                self.estado_origen = self.estado_anterior[id]
            #se actualiza el indice
            
            #se actualiza el svg
            self.svg.write_svg()

class SimuladorAFN : 

    def __init__(self, afn, secuencia_caracteres, svg_file):
        """
        @type afn  : Automata
        @param afn : automata apartir del cual se realiza al simulación
        
        @type secuencia_caracteres  : String
        @param secuencia_caracteres : representa a la cadena de caracteres
                                    a ser utilizados en la simulación.
        """
        self.afn =  afn
        self.svg = SVGManager(svg_file)
        self.svg.gen_svg_from_automata(afn)
        self.camino = []
        #se procesa el afd
        self.svg.load_nodes()
        self.index = 0
        self.secuencia_caracteres = secuencia_caracteres
    
    def gen_camino(self):
        """
        Este metodo utiliza la técnica de backtracking para validar la
        secuencia de caracteres de entrada con el afn.
        
        @rtype  : Boolean
        @return : True si la cadena es aceptada, en caso contrario
                  retorna False
        """
        print self.secuencia_caracteres
        print "*"*10
        self.camino = []
        self.alternativas = []
        
        if self.__gen_camino(self.afn.get_estado_inicial()) :
            #si es aceptada se imprime el camino que lleva a que la 
            #cadena sea aceptada
            for c in self.camino :
                print "=> " +str(c)
            return True
        else :
            #en caso de que la cadena sea rechazada se imprime las 
            #combinaciones realizadas con el fin de validar la cadena.
            index =0
            for a in self.alternativas :
                print "A" + str(index)
                print "="*10
                for e in a:
                    print str(e) 
                index += 1

            return False
        
    def __gen_camino(self, origen):
        """
        Este metodo utiliza la técnica de backtracking para validar la
        secuencia de caracteres de entrada con el afn.
        
        @type afn  : Estado
        @param afn : estado origen apartir del cual se tratará de consumir
                     la entrada
        
        @rtype  : Boolean
        @return : True si la cadena es aceptada, en caso contrario
                  retorna False
        """
        if len(self.secuencia_caracteres) == self.index :
            #se consumio la totalidad de los caracteres
            #si el estado es un estado final el algoritmo termina
            if origen.final :
                return True
            
            final = True 
            for arco in self.afn.get_transicion(origen):
                if arco.simbolo == Keys.VACIO :
                    self.camino.append(arco)
                    if self.__gen_camino(arco.destino) :
                        return True
                    
                    self.alternativas.append([]+self.camino)
                    self.camino.pop()

                    
            if final :
                return origen.final
        #Se obtine el caracter actual a procesar.
        caracter = self.secuencia_caracteres[self.index]
        #se obienen  las transiciones del estado origen
        for arco in self.afn.get_transicion(origen) :  
            if caracter == arco.simbolo : 
                self.index += 1
                #anade al camino la posible solución
                self.camino.append(arco)
                #se realiza una llamada recursiva para tratar de 
                #llegar al final
                if self.__gen_camino(arco.destino) :
                    #la cadena es aceptada
                    return True
                
                #se añade como un alternativa
                self.alternativas.append([]+self.camino)
                #se acutaliza el indice de la secuencia de caracteres
                self.index -= 1
                #se elimina del camino debido a que no llevo a la
                #solución
                self.camino.pop()
                
            elif arco.simbolo == Keys.VACIO :
                self.camino.append(arco)
                if self.__gen_camino(arco.destino) :   
                    #la cadena es aceptada
                    return True
                #se añada como una alternativa el camino
                self.alternativas.append([]+self.camino)
                #se elimina del camino debido a que no llevo a la
                #solución
                self.camino.pop()

        return False

    def next_state(self):
        
        if self.camino == [] :
            self.state = self.gen_camino()
            if not self.state :
                return False
            self.index = 0
            e = self.camino[self.index]
            self.svg.set_node_color(e.origen.id)
            self.svg.write_svg()
            return True
        
        if self.state and self.index<len(self.camino):
            e = self.camino[self.index]
            self.svg.set_node_color(e.origen.id, "none")
            self.svg.set_node_color(e.destino.id)
            self.index += 1
            self.svg.write_svg()
            return True
        
        return False
        
        
    def previous_state(self): 

        if self.state and self.index >= 1:
            self.index -= 1
            e = self.camino[self.index]
            self.svg.set_node_color(e.destino.id, "none")
            self.svg.set_node_color(e.origen.id)
            self.svg.write_svg()
            return True
        
        return False
