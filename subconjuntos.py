#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from automata import *
from keys import *
from collections import deque
from stack import *
from afd import *

"""
:author: Maria Jose Lopez
:contact: majito033@gmail.com
"""

class Subconjuntos:
    
    def __init__(self, afn) :
        self.automatas = []
        self.afn = afn
        self.afd = Afd()
        self.estadosD = []
        self.colaTemp = deque()
        self.estProcesados = (self.afn.getEstadoFinal()).ID - 1
    
    def item_in_list(self,U):
        if (self.estadosD.__contains__(U)):
            return True
        else:
            return False
    
    def cerraduraVaciaInicial(self, estado):
        if DEBUG :
            print "CERRADURA VACIA INICIAL"

        resultado = []
        resultado = self.recorridoSimple(estado, Keys.VACIO)
        return resultado
        
    def cerraduraVacia(self, estados):
        if DEBUG :
            print "CERRADURA VACIA"
            
        resultado = []
        resultado = self.recorrer(estados, Keys.VACIO)
        return resultado
    
    def mover(self, estados, simboloBuscado):
        if DEBUG :
            print "MOVER"
            
        resultado = []
        resultado = self.recorrer(estados, simboloBuscado)
        return resultado
        
    
    def recorridoSimple(self, estado, simboloBuscado):
        if DEBUG :
            print "RECORRIDO SIMPLE"
            print "SIMBOLO BUSCADO : " + str(simboloBuscado)
        pila = Stack()
        alcanzados = []
        
        #Si el simbolo buscado es igual al simbolo vacio, debe incluirse
        #el estado actual
        if (simboloBuscado.find(Keys.VACIO) >= 0):
            alcanzados.append(estado)

        #Meter el estado actual en la pila
        pila.push(estado)
        
        while (pila.isEmpty() == False):
            estado = pila.pop()
            transiciones = self.afn.get_transicion(estado)
            
            if DEBUG :
                print "ESTADO SACADO DE LA PILA : " + str(estado)
 
                for t in transiciones:
                    print "TRANSICIONES" + str(t)
            
            for t in transiciones:
                e = ""
                e = t.destino
                s = ""
                s = t.simbolo
                boolean_simbolo = False
                if (s == simboloBuscado):
                    boolean_simbolo = True
                boolean_alcanzados = alcanzados.__contains__(e)
                
                if DEBUG :
                    print "ESTADO DESTINO : " + str(e)

                    print "SIMBOLO : " + str(s)

                    print "BOOLEAN SIMBOLO : " + str(boolean_simbolo)
                    print "BOOLEAN ALCANZADOS : " + str(boolean_alcanzados)
                
                if (s.find(simboloBuscado) >= 0 and alcanzados.__contains__(e) == False):
                    alcanzados.append(e)
                    
                    if DEBUG :
                        print "ENTRO EN ALCANZADOS"
                    
                    #Si el simbolo buscado es el simbolo vacio, se debe
                    #recorrer recursivamente los estados alcanzados,
                    #agregando a la pila si esto sucede
                    if (simboloBuscado.find(Keys.VACIO) >= 0):
                        pila.push(e)
            if DEBUG :
                for i in alcanzados:
                    print "ALCANZADOS : " + str(i)
        return alcanzados
    
    
    def recorrer(self, estados, simboloBuscado):
        if DEBUG :
            print "RECORRER"
            
        alcanzados = []
        for e in estados:
            alc = []
            alc = self.recorridoSimple(e, simboloBuscado)
            #alc.sort()
            for i in alc:
                if (alcanzados.__contains__(i) == False):
                    alcanzados += alc
        return alcanzados
        

    def getAfd(self):
        
        #Calcular la cerradura vacia del Estado inicial
        estado_inicial = self.afn.getEstadoInicial()
        estado_final = (self.afn.getEstadoFinal()).ID - 1
        if DEBUG :
            print "ESTADO INICIAL : " + str(estado_inicial)
            print "ESTADO FINAL : " + str(estado_final)
            
        
        resultado = []
        resultado = self.cerraduraVaciaInicial(estado_inicial)

        if DEBUG :
            for r in resultado:
                print "RESULTADO : " + str(r)

        #Agregar la cerradura vacia del estado inicial del AFN a estadosD
        #sin marcar
        self.estadosD.append(resultado)
        self.colaTemp.append(resultado)
        
        if DEBUG :
            for i in self.estadosD:
                print "ESTADOS D : " + str(i)
        
        #Se inicia el ciclo principal del algoritmo
        while (self.colaTemp):
            #Marcar T 
            T = self.colaTemp.popleft()
            
            if DEBUG :
                for i in T:
                    print "T : " + str(i)
            
            #Agregamos el estado al AFD
            if (self.afd.cantidad_estados() < len(self.estadosD)):
                e = Estado()
                self.afd.add_estado(e)
                
                if DEBUG :
                    print "ESTADO " + str(e)
                    
            #Estado a procesar
            self.estProcesados += 1
            estadoOrigen = self.afd.get_estado(self.estProcesados)
            
            
            if DEBUG :
                print "ORIGEN " + str(estadoOrigen)
            
            #Buscar transiciones por cada simbolo
            for simbolo in Keys.ALFABETO:
                #Aplicar cerraduraVacia(mueve(T, simbolo))
                M = []
                M = self.mover(T, simbolo)
                
                if DEBUG :
                    for i in M:
                        print "M : " + str(i)
                
                U = []
                U = self.cerraduraVacia(M)
                
                if DEBUG :
                    for j in U:
                        print "U : " + str(j)
                
                if (self.estadosD.__contains__(U)):
                    posicion = self.estadosD.index(U)
                    estad = self.estadosD[posicion]

                    p = estado_final + posicion + 1
                    
                    if DEBUG :
                        print "P : " + str(p)
                        print "POSICION : " + str(posicion)
                        
                        for i in estad:
                            print "ESTAD : " + str(i)
                        print "ESTADO[0] : " + str(estad[0])  
                    
                    estadoDestino = self.afd.get_estado(p)
                elif (U != []):
                    estadoDestino = Estado()
                    self.afd.add_estado(estadoDestino)
                    
                    #Agregar U a estadosD sin marcar
                    self.estadosD.append(U)
                    self.colaTemp.append(U) 
                else:
                    break
                #Se añade el estado inicial del automata 
                if self.afd.estado_inicial == None :
                    self.afd.estado_inicial = estadoOrigen
                    
                #Agregamos la transicion al AFD
                self.afd.add_transicion(estadoOrigen, estadoDestino, simbolo)
        
        #Establecer los estados finales del AFD
        if DEBUG :
            print "**** ESTABLECER LOS ESTADOS FINALES DEL AFD ****"
            
        i = 0
        fin = len(self.estadosD)
        if DEBUG :
            print "LONGITUD DE ESTADOS D : " + str(fin)
        while (i < fin):
            if DEBUG :
                print "i : " + str(i)
                print "LONGITUD estadosD[i] : " + str(len(self.estadosD[i]))
            estadoAFD = self.afd.get_estado(estado_final+i+1)
            for es in self.estadosD[i]:            
                if (es.get_final()):
                    estadoAFD.set_final(True)
            i += 1

        
        print "******** AFD ********"
        i = 0
        fin = len(self.estadosD)
        while (i < fin):
            print "ESTADO DEL AFD : " + str(i)
            for es in self.estadosD[i]:
                print "          ESTADO DEL AFN : " + str(es)
            i += 1
        
 
        self.automatas.append(self.afd)
        return self.afd
