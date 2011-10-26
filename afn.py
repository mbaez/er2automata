#! /usr/bin/env python
# -*- coding: utf-8 -*-
from keys import *
from automata import *

class Afn(Automata):

    def __init__(self):
        self.estado_inicial = None
        self.estado_final = None
        
        self.estados = {}
        self.arcos = []
        pass
     

