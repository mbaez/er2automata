#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Librerias externas
import pygraphviz as pgv
#librerias internas del proyecto
from analizador import *
from thompson import *
from subconjuntos import *
from afd_minimo import AFD
from bnf import *
from simulador import *

import pygtk
pygtk.require("2.0")
import gtk, gtk.glade

class App:
 
    def __init__(self):
        self.glade = gtk.glade.XML("gui.glade")
        
        self.glade.signal_autoconnect(self)
        
        self.glade.get_widget("window1").show_all()
        
        self.entry1 = self.glade.get_widget("entry1")

        self.label3 = self.glade.get_widget("label3")
        
        self.label5 = self.glade.get_widget("label5")

        self.image1 = self.glade.get_widget("image1")
        
        self.image2 = self.glade.get_widget("image2")
        
        self.image3 = self.glade.get_widget("image3")
        

    def on_window1_delete_event(self, widget, event):
        gtk.main_quit()
    
    
    def on_button1_clicked(self, widget):
        """
            Se encarga de abrir una ventana para que el usuario realice
            las configuraciones
        """
        self.glade1 = gtk.glade.XML("configuraciones.glade")
        
        self.glade1.signal_autoconnect(self)
        
        self.glade1.get_widget("window1").show_all()
        self.window2 = self.glade1.get_widget("window1")
        
        self.entry2 = self.glade1.get_widget("entry1")


    def on_window2_delete_event(self, widget, event):
        self.window2.destroy()
        
    def on_button4_clicked(self, widget):
        """
            Se encarga de agregar un alfabeto ingresado por el usuario 
            
        """

    def on_button5_clicked(self, widget):
        """
            Se encarga de agregar una definicion regular ingresada por 
            el usuario a la tabla de simbolos
        """
        
        texto = self.entry2.get_text()
        pos = texto.index("=")
        
        def_r = texto[1:pos]
        value = texto[pos+1:len(texto)]
        
        keys = Keys()
        keys.set_tabla_simbolos_value_at(def_r,value)
        
        self.window2.destroy()
        
        tabla = keys.print_tabla_simbolos()
        self.label3.set_text('\n'.join([str(tabla[t]) for t in tabla]))
    
    def on_button6_clicked(self, widget):
        self.window2.destroy()

    def on_button2_clicked(self, widget):
        """
            Se en carga realizar el analisis lexico de la expresion 
            ingresada por el usuario
        """
        texto = self.entry1.get_text()
        
        keys = Keys()
        keys.set_tabla_simbolos_value_at("a_or_b","(a|b)")
        print "Start.."
        a = Analizador(texto, keys);
        if a.start():
            print "Done.." + str(a.postfija)
        t = Thompson(a.postfija)

        t.start()

        print len(t.automatas[0].estados)

        draw(t.automatas[0])
        
        s = Subconjuntos(t.automatas[0])
        af = s.start_subconjutos()
        
        draw(af, "afd")
        afd = AFD(af)
        afd_min = afd.minimizar()
        draw(afd_min, "minimo")

        b = Bnf(afd_min)
        b.start_bnf()
        
        self.image1.set_from_file('automata.svg')
        self.image2.set_from_file('afd.svg')
        self.image3.set_from_file('minimo.svg')
        
        tabla = keys.print_tabla_simbolos()
        self.label3.set_text('\n'.join([str(tabla[t]) for t in tabla]))
        
        bnf = b.print_bnf()
        self.label5.set_text('\n'.join([str(bnf[b]) for b in bnf]))



def draw(automata, file_name="automata") :
    #se crea un grafo dirigido
    gr = pgv.AGraph(directed=True,rankdir="LR", strict=False)
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
                    label=arco.simbolo ,color='#8dad48')

        #gr.draw(str(arco.origen.id) + "-"+arco.simbolo + "--"+str(arco.destino.id) + '.svg')
        #str(arco.origen) + "="+arco.simbolo + "=>"+str(arco.destino)

    #se utiliza el agoritmo dot para el grafo
    #neato|dot|twopi|circo|fdp|nop
    gr.layout(prog='dot')
    #se escribe el grafo resultado en un archivo
    gr.draw(file_name + '.svg')



if __name__ == "__main__":

    
    try:
        a = App()
        gtk.main()
    except KeyboardInterrupt:
        pass
    
    er = "$a_or_b;*.a.b.b"

    keys = Keys()
    keys.set_tabla_simbolos_value_at("a_or_b","(a|b)")
    print er
    print "Start.."
    #tokens = StringTokenizer (er, keys)
    a = Analizador(er, keys);
    if a.start():
        print "Done.." + str(a.postfija)

    t = Thompson(a.postfija)

    t.start()

    print len(t.automatas[0].estados)

    draw(t.automatas[0])
    sim = SimuladorAFN(t.automatas[0], "abb")
    sim.gen_camino()
    
    """
    s = Subconjuntos(t.automatas[0])
    af = s.start_subconjutos()
    
    #draw(af, "afd")
    afd = AFD(af)
    afd_min = afd.minimizar()
    #draw(afd_min, "minimo")
    sim = SimulardorAFD(afd_min, "aabc")
    has_more = sim.next_state()
    while has_more : 
        direccion = raw_input()
        
        if direccion == "N" :
            has_more = sim.next_state()
        elif direccion == "P" :
            has_more = sim.previous_state()
            
    #b = Bnf(afd_min)
    #b.start_bnf()
    """
