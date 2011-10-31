#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Librerias externas
import pygraphviz as pgv
#librerias internas del proyecto
from string_tokenizer import *
from analizador import *
from thompson import *
from subconjuntos import *
#from automata import *

def draw(automata, file_name="automata") :
    #se crea un grafo dirigido
    gr = pgv.AGraph(directed=True,rankdir="LR")
    estados = {}
    inicio = automata.estado_inicial
    #se otienen todos los estados del dict
    estado_list = [] + automata.estados.values()
    #se ordenan los estados
    estado_list.sort()

    for estado in estado_list :
        if estado.final :
            #si es un estado final se añade con un doble circulo
            gr.add_node(estado.id, shape = "doublecircle")
        else :
            #si no es un estado final se añade con un circulo
            gr.add_node(estado.id, shape = "circle")

    #Se añade un nodo "invisible"
    gr.add_node("",width="0",height="0")
    #se añade un arcon entre el nodo vacio y el estado inicial del
    #automata, con esto se obtiene el siguiente grafico :
    # --Inicio--> (Estado Inicial)
    gr.add_edge(("",inicio.id), label="Inicio", color='#8dad48')
    #por cada arco definido se añade las relaciones entre los nodos
    #definidos anteriormente
    for arco in automata.arcos :
        #se añaden los arcos entre los estados y el simbolo de
        #de transicion, con esto se consigue un lo siguiente :
        #(inicio) ---simbolo --->(destino)
        gr.add_edge((arco.origen.id,arco.destino.id),\
                    label= arco.simbolo ,color='#8dad48')

    #se utiliza el agoritmo dot para el grafo
    gr.layout(prog='dot')
    #se escribe el grafo resultado en un archivo
    gr.draw(file_name + '.svg')




if __name__ == "__main__":

    er = "(a|b)+"

    keys = Keys()
    print er
    print "Start.."
    tokens = StringTokenizer (er, keys)
    a = Analizador(tokens, keys);
    if a.start():
        print "Done.." + str(a.postfija)

    t = Thompson(a.postfija)

    t.start()

    print len(t.automatas[0].estados)

    draw(t.automatas[0])
    
    s = Subconjuntos(t.automatas[0])
    af = s.start_subconjutos()
    

    draw(af, "afd")

