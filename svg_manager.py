#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygraphviz as pgv
import re
from xml.dom.minidom import parse

class SVGManager :

    document = None
    nodes = {}

    def __init__(self, svg_file_name) :
        """
        Este metodo se encarga de encarga de inicializar los atributos
        y parsea el archivo svg para que sea manejable

        @type svg_file_name  : String
        @param svg_file_name : nombre del archivo svg
        """
        self.svg_file_name = svg_file_name



    def load_nodes(self) :
        """
        Se encarga de prosesar los tags que poseen la siguiente estructura

        <g id="node2" class="node">
            <title>E4</title>
            <ellipse fill="none" stroke="black"/>
            <text>E4</text>
        </g>

        Apartir de esta información se generan entradas en un diccionario
        donde la clave es el texto contenido en <title> </title> y el
        es la referncia al atributo de ellipse.

        ["E4"] -> <ellipse fill="none" stroke="black"/>

        """
        self.document = parse(self.svg_file_name)
        self.document.normalize()
        self.elements = self.document.documentElement
        self.polygons = []
        #se obtiene del svg todos los elementos  que contienen el tag
        #<g> ... </g>
        for polygon in self.elements.getElementsByTagName("g") :
            #se procesan unicamente aquellos tags que son del tipo nodo
            if polygon.attributes["class"].value == "node" :
                #se obiene el tag <title>.. </title>
                title = polygon.getElementsByTagName("title")[0]
                #se verifica si el tag posee un valor
                if title.firstChild !=  None:
                    #se obtiene el valor contenido dentro del tag
                    label = str(title.firstChild.data).strip()
                    #se obtiene el tag <ellipse>... </ellipse>
                    ellipse = polygon.getElementsByTagName("ellipse")[0]
                    self.polygons.append(ellipse)
                    #se guarda en el diccionario el id del estado y la
                    #referencia a la figura
                    # ["E4"] -> <ellipse fill="none" stroke="black"/>
                    #print ellipse
                    self.nodes[label] = ellipse#len(self.polygons)-1

    def set_node_color(self, node_id, color="#ADD8E6") :
        """
        Este método se encarga de reemplazar el fill del la ellipse
        identificado por el id node_id y establecer el valor color.

        [node_id] --> <ellipse fill=color stroke="black

        @type node_id  : String
        @param node_id : identificador del estado al cual se desea cambiar
                         el color.
        @type color  : String
        @param color : color que sera asignado al estado identificado por
                       node_id
        """
        #print node_id
        if self.nodes.has_key(node_id) :
            self.nodes[node_id].attributes["fill"].value = color

            #print  node_id + "->" +  self.nodes[node_id].attributes["fill"].value


    def write_svg(self, svg_file_name=None) :
        """
        Este metodo se volcar el el svg en un archivo de nombre
        svg_file, si svg_file no es especificado se sobrescribe el archivo
        original

        @type svg_file_name  : String
        @param svg_file_name : nombre del archivo en el cual se va
                               a escribir el svg, si no se especifica
                               el nombre sobrescribe el archivo original

        """
        if svg_file_name == None :
            svg_file_name =  self.svg_file_name
        #se el archivo, si no existe se crea
        source = open(svg_file_name, 'w+')
        # se escribe en el archivo el contenido del documento xml actual
        ugly = self.document.toxml()
        source.write(ugly)
        #se cierra el archivo
        source.close()

    def gen_svg_from_automata(self, automata, layout_prog="dot") :
        """
        Este método genera una imagen svg apartir de un automata

        @type automata  : Automata
        @param automata : automata apartil del cual se generará la imagen

        @type layout_prog  : String
        @param layout_prog : indica el algoritmo que será utilizado para
                             dibujar el grafo. los valores posibles son
                             neato|dot|twopi|circo|fdp, el valor por
                             defecto es dot.
        """
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
        gr.add_node(u"\u2205",width="0",height="0")
        #se añade un arcon entre el nodo vacio y el estado inicial del
        #automata, con esto se obtiene el siguiente grafico :
        # --Inicio--> (Estado Inicial)
        gr.add_edge((u"\u2205",inicio.id), label="Inicio", color='#8dad48')
        #por cada arco definido se añade las relaciones entre los nodos
        #definidos anteriormente
        for arco in automata.arcos :
            #se añaden los arcos entre los estados y el simbolo de
            #de transicion, con esto se consigue un lo siguiente :
            #(inicio) ---simbolo --->(destino)
            gr.add_edge((arco.origen.id,arco.destino.id),\
                        label=arco.simbolo ,color='#8dad48')

        #se utiliza el agoritmo dot para el grafo
        #neato|dot|twopi|circo|fdp
        gr.layout(prog=layout_prog)
        #se escribe el grafo resultado en un archivo
        gr.draw(self.svg_file_name)

