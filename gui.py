#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygraphviz as pgv


def draw(automatas) :
    gr = pgv.AGraph(directed=True)

    for automata in automatas :
        for arco in automata.arcos :
            gr.add_edge((arco.origen.id,arco.destino.id),\
                        label=arco.simbolo,color='#8dad48')

    gr.layout()
    gr.draw('automata.svg')


