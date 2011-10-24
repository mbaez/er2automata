#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

class ConjuntoPi :

    def __init__(self) :
        #diccionario que posee como clave el id del grupo y como 
        #valor los estados pertenecientes al grupo.
        self.grupos = {}
        #diccionario que posee como clave el id del estado y como valor
        #la referencia al grupo al cual pertenece.
        self.estados = {}
    
    def add_estado_to_group(self, id_grupo ,estado) :
        """
        Este método añade un estado al grupo de id id_grupo
         
        @type id_grupo  : String
        @param id_grupo : Id del grupo 
        
        @type estado  : Estado
        @param estado : estado que sera añadido al grupo id_grupo
        
        """
        if self.grupos.has_key(id_grupo) :
            self.grupos[id_grupo] = []
        
        self.grupos[id_grupo].append(estado)
        
        self.estados[estado.id] = self.grupos[id_grupo]
        
    def add_estados_to_group(self, id_grupo ,estados) :
        """
        Este método añade la lista de estados al grupo de id id_grupo
         
        @type id_grupo  : String
        @param id_grupo : Id del grupo 
        
        @type estado  : Estado[]
        @param estado : estados que seran añadido al grupo id_grupo
        
        """
        id_grupo = str(id_grupo)
        if not self.grupos.has_key(id_grupo) :
            self.grupos[id_grupo] = []
            self.grupos[id_grupo] = estados
            
        else :
            self.grupos[id_grupo] = self.grupos[id_grupo] + estados
        
        for estado in estados:
            self.estados[estado.id] = self.grupos[id_grupo]
    
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
        
        @rtype  : Estado[]
        @return : estados que pertenecen al grupo en el cual esta 
                contenido el estado
        """
        return self.estados[estado.id]
    
    def __str__(self):
        _str = ""
        
        for i in range(len(self.grupos)) : 
            _str += "\nGrupo " + str(i) + " : {" 
            for estado in self.grupos.get(str(i)) :
                _str += str(estado) + ","
            
            _str = _str[0:-1] + "}"
        
        return _str 

class AFDMinimo :
    
    def __init__(self, automata):
        #representa la tabla de transiciones de los estados del afd
        self.tabla = TablaTransiciones(automata)
        self.tabla.build_table()
        self.automata = automata
        self.conjunto_pi = ConjuntoPi()
        
        self.conjunto_pi.add_estados_to_group("0", self.tabla.\
                            get_estados_finales())
                            
        self.conjunto_pi.add_estados_to_group("1", self.tabla.\
                            get_estados_no_finales())

    
    def start(self): 
        
        pass
