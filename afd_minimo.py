#!/usr/bin/env python
# -*- coding: utf-8 -*-
from automata import *
"""
:author: Maximiniliano Báez González
:contact: mxbg.py@gmail.com
"""
class TablaTransiciones :
    def __init__(self, automata):
        self.table = {}
        self.estados = {}
        self.automata = automata
        self.estados_finales = {}
        #Se inicializa el diccionario de estados finales
        self.estados_finales[True] = []
        self.estados_finales[False] = []
        self.simbolos = {}

    def build_table(self):
        """
        Este método se encarga de construir la tabla de transiciones en
        donde la calve de la tabla esta determinada por :

            calve = id del estado origen + simbolo de transición

        El valor correspondiente a la clave es la referencia al estado
        destino o esado hacia el cual se produce la transcición.
        """
        self.table = {}
        for arco in self.automata.arcos:
            self.table[arco.origen.id + arco.simbolo] = arco.destino
            #se añaden los simbolos utilizados en el afd
            self.simbolos [arco.simbolo] = arco.simbolo
            #se controla que no se cargen estados repetidos
            if not self.estados.has_key(arco.origen.id) :
                self.estados[arco.origen.id] = arco.origen
                self.estados_finales [arco.origen.final].append(arco.origen)

            if not self.estados.has_key(arco.destino.id) :
                self.estados[arco.destino.id] = arco.destino
                #se añade en un diccionario todos los estados
                self.estados_finales [arco.destino.final].append(arco.destino)
        
    def get_estados_finales (self):
        """
        Este método devuelve la lista de de estados finales del automata.

        @rtype  : Estado[]
        @return : estados finales del automata
        """
        return self.estados_finales[True]

    def get_estados_no_finales(self):
        """
        Este método devuelve la lista de de estados no finales del automata.

        @rtype  : Estado[]
        @return : estados no finales del automata
        """
        return self.estados_finales[False]

    def get_table_value(self, id_grupo) :
        """
        @type id_grupo  : String
        @param id_grupo : Id del grupo

        @rtype  : Estado
        @return : el esado correspondiente en la tabla para el id
        """
        
        if self.table.has_key(str(id_grupo)) :
            return self.table[str(id_grupo)]
        
        return None

class ConjuntoPi :

    ID_GRUPO = 0

    def __init__(self) :
        #diccionario que posee como clave el id del grupo y como
        #valor los estados pertenecientes al grupo.
        self.grupos = {}
        #diccionario que posee como clave el id del estado y como valor
        #la referencia al grupo al cual pertenece.
        self.estados = {}
        #variables utilizadas a la hora de determinar el punto de parada
        #del algoritmo
        self.len_grupos = 0
        self.count_same_len = 0

    def add_estado (self, estado):

        self.add_estado_to_group(ConjuntoPi.ID_GRUPO, estado)

        ConjuntoPi.ID_GRUPO += 1

        return ConjuntoPi.ID_GRUPO -1

    def add_estado_to_group(self, id_grupo ,estado) :
        """
        Este método añade un estado al grupo de id id_grupo

        @type id_grupo  : String
        @param id_grupo : Id del grupo

        @type estado  : Estado
        @param estado : estado que sera añadido al grupo id_grupo

        """
        id_grupo = str(id_grupo)

        if self.grupos.has_key(id_grupo) :
            self.grupos[id_grupo] = []

        self.grupos[id_grupo].append(estado)

        self.estados[estado.id] = id_grupo

    def add_estados(self, estados) :

        self.add_estados_to_group(ConjuntoPi.ID_GRUPO, estados)

        ConjuntoPi.ID_GRUPO += 1

        return ConjuntoPi.ID_GRUPO -1

    def add_estados_to_group(self, id_grupo ,estados) :
        """
        Este método añade la lista de estados al grupo de id id_grupo

        @type id_grupo  : String
        @param id_grupo : Id del grupo

        @type estado  : Estado[]
        @param estado : estados que serán añadido al grupo id_grupo

        """
        id_grupo = str(id_grupo)
        if not self.grupos.has_key(id_grupo) :
            self.grupos[id_grupo] = []
            self.grupos[id_grupo] = estados

        else :
            self.grupos[id_grupo] = self.grupos[id_grupo] + estados

        for estado in estados:
            self.estados[estado.id] = id_grupo

    def get_group_by_id(self, id) :
        """
        Este método retorna el grupo identificado por id

        @type id  : String
        @param id : Id del grupo

        @rtype  : Estado[]
        @return : estados que pertenecen al grupo
        """
        return self.grupos[id]

    def get_group_by_estado(self, estado):
        """
        Este método retorna el grupo en el cual esta contenido el estado

        @type esado   : Estado
        @param estado : estado que pertenece a algun grupo de de conjunto

        @rtype  : String
        @return : el id del grupo al cual pertenece
        """
        return self.estados[estado.id]
    
    def get_next_group(self):
        """
        @rtype  : String
        @return : el id del siguiente grupo
        """
        len_grupos = len(self.grupos.keys())
        for id_grupo in self.grupos.keys()  :

            if len(self.grupos[id_grupo]) > 1 and self.count_same_len < len_grupos:
                if len_grupos == self.len_grupos :
                    self.count_same_len+=1
                else:
                    self.len_grupos = len_grupos
                    self.count_same_len = 0
                
                return id_grupo

        return None

    def len(self):
        """
        @rtype  : Integer
        @return : la cantidad de grupos existentes.
        """
        return len(self.grupos)
    
    def remove_group (self, key) :

        self.grupos.pop(key)

    def __str__(self):
        _str = ""
        values = self.grupos.values()
        id = 1;
        for value in values :
            _str += "\nGrupo " + str(id) + " : {"
            for estado in value :
                _str += str(estado) + ","

            _str = _str[0:-1] + "}"

            id +=1

        return _str

class AFD :

    def __init__(self, automata):
        ConjuntoPi.ID_GRUPO = 0
        #representa la tabla de transiciones de los estados del afd
        self.tabla = TablaTransiciones(automata)
        self.tabla.build_table()
        self.automata = automata
        self.conjunto_pi = ConjuntoPi()

        self.conjunto_pi.add_estados(self.tabla.\
                            get_estados_finales())

        self.conjunto_pi.add_estados(self.tabla.\
                            get_estados_no_finales())


    def minimizar(self):
        """
        """
        group_id = self.conjunto_pi.get_next_group()
        while group_id != None :
            #se obtienen los estados del grupo
            estados = self.conjunto_pi.get_group_by_id(group_id)
            
            self.__procesar_grupo(estados, group_id)
            #se obtiene el id del siguiente grupo a evaluar
            group_id = self.conjunto_pi.get_next_group()
        
        #print self.conjunto_pi.grupos
        return self.__transformar_conjunto_pi()

    def __transformar_conjunto_pi(self) : 
        
        afd_minimo = Automata()
        transiciones = {}
        
        for arco in self.automata.arcos :
            grupo_origen = self.conjunto_pi.get_group_by_estado(arco.origen)
            grupo_destino = self.conjunto_pi.get_group_by_estado(arco.destino)
            grupo_id = grupo_origen + arco.simbolo
            
            if not transiciones.has_key(grupo_id) :
                
                transiciones[grupo_id] = grupo_destino
                                
                
                origen = afd_minimo.get_estado_id(grupo_origen)
                if origen == None :
                    origen = Estado(id=grupo_origen)
                if arco.origen.final : 
                    origen.final = True
                
                destino = afd_minimo.get_estado_id(grupo_destino)
                if destino == None :
                    destino = Estado(id=grupo_destino)
                if arco.destino.final : 
                    destino.final = True

                afd_minimo.add_transicion(origen, destino, arco.simbolo)
                
                if self.automata.get_estado_inicial().id == arco.origen.id :
                    afd_minimo.estado_inicial = origen
        
        
        return afd_minimo
            
            
    def __procesar_grupo (self, estados, group_id) :
        """
        """
        sub_grupos = {}
        for estado in estados :
            #print "\t->"+str(estado)
            self.__dividir_grupo(estado, sub_grupos)

        #si existen mas de 1 subgrupo se elimina el grupo y se añaden los
        #sub grupos derivados a conjunto pi
        if len (sub_grupos) > 1:
            self.conjunto_pi.remove_group(group_id)
            #se añaden los subgrupos
            for sub_grupo in sub_grupos.values() :
                self.conjunto_pi.add_estados(sub_grupo)

    def __dividir_grupo (self, estado, sub_grupos) :
        """
        """
        id_sub_grupo = "";
        for simbolo in self.tabla.simbolos :
            grupo = self.tabla.get_table_value(estado.id + simbolo)
            if grupo != None : 
                #print "\t#" + str(grupo)
                id_sub_grupo += ":" + self.conjunto_pi.get_group_by_estado(grupo)
        #print "\t$" + id_sub_grupo

        if not sub_grupos.has_key(id_sub_grupo) :
            #si no se encuentra en el sub grupo se inicializa una lista para
            #añadir los estados
            sub_grupos[id_sub_grupo] = []

        sub_grupos[id_sub_grupo].append(estado)

