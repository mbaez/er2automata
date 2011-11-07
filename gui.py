#! /usr/bin/env python
# -*- coding: utf-8 -*-

#librerias internas del proyecto
from analizador import *
from thompson import *
from subconjuntos import *
from afd_minimo import *
from bnf import *
from simulador import *

import pygtk
pygtk.require("2.0")
import gtk, gtk.glade

class EditorAlfabeto:
    def __init__(self, keys):
        self.keys = keys
        self.glade = gtk.glade.XML("glade/editor_alfabeto.glade")
        self.glade.signal_autoconnect(self)
        self.main_window = self.glade.get_widget("main_window")
        self.main_window.show_all()
        self.alfabeto_text = self.glade.get_widget("alfabeto_text")
        buffer = self.alfabeto_text.get_buffer()
        buffer.set_text(self.keys.alfabeto)
    
    def on_aplicar_clicked(self, widget):
        buffer = self.alfabeto_text.get_buffer()
        start = buffer.get_start_iter() 
        end = buffer.get_end_iter() 
        
        self.keys.alfabeto = buffer.get_text(start, end)
        
        self.main_window.destroy()
    
    def on_cancelar_clicked(self, widget):
        self.main_window.destroy()
        

class Simulador:
    def __init__(self, afd, afn):
        self.afd = afd
        self.afn = afn
        self.__init_params__()
        self.__init_widgets__()
        
    def __init_params__(self):

        self.sim_afd = None
        self.sim_afn = None
        self.afn_svg="images/sim_afn.svg"
        self.afd_svg="images/sim_afd.svg"
    
    def __init_widgets__(self):
        self.glade = gtk.glade.XML("glade/simulador.glade")
        self.glade.signal_autoconnect(self)
        self.main_window = self.glade.get_widget("main_window")
        self.main_window.show_all()
        self.secuencia_entry = self.glade.get_widget("secuencia_entry")
        
        self.aplicar_button = self.glade.get_widget("aplicar_button")
        self.actualizar_button = self.glade.get_widget("actualizar_button")
        
        self.atras_afd_button = self.glade.get_widget("atras_afd_button")
        self.adelante_afd_button = self.glade.get_widget("adelante_afd_button")
        self.afd_image = self.glade.get_widget("afd_image")

        
        self.atras_afn_button = self.glade.get_widget("atras_afn_button")
        self.adelante_afn_button = self.glade.get_widget("adelante_afn_button")
        self.afn_image = self.glade.get_widget("afn_image")
        
    
    def on_aplicar_clicked(self, widget):
        secuencia = self.secuencia_entry.get_text()
        
        self.sim_afd = SimuladorAFD(self.afd, secuencia, self.afd_svg)
        self.afd_image.set_from_file(self.afd_svg)
        
        self.sim_afn = SimuladorAFN(self.afn, secuencia, self.afn_svg)
        self.afn_image.set_from_file(self.afn_svg)
        
    def on_actualizar_clicked(self, widget):
        self.on_aplicar_clicked(None)
        
    def on_atras_afn_clicked(self, widget):
        if self.sim_afn != None :
            if self.sim_afn.previous_state(): 
                self.afn_image.set_from_file(self.afn_svg)
        
    def on_adelante_afn_clicked(self, widget):
        if self.sim_afn != None :
            if self.sim_afn.next_state(): 
                self.afn_image.set_from_file(self.afn_svg)
        
    def on_atras_afd_clicked(self, widget):
        if self.sim_afd != None :
            if self.sim_afd.previous_state(): 
                self.afd_image.set_from_file(self.afd_svg)
        
    def on_adelante_afd_clicked(self, widget):
        if self.sim_afd != None :
            if self.sim_afd.next_state(): 
                self.afd_image.set_from_file(self.afd_svg)
    
class App:
 
    def __init__(self):
        
        self.glade = gtk.glade.XML("glade/gui.glade")
        
        self.glade.signal_autoconnect(self)
        self.main_window = self.glade.get_widget("main_window")
        self.main_window.show_all()
        self.expresion_entry = self.glade.get_widget("expresion_entry")
        
        self.__init_tree_view__()
        self.__init_automata_params__()
        self.__init_canvas__()

    def __init_tree_view__(self):
        """
        Este método inicializa los treeview de la aplicacion, obiene
        los widgets y los vuelve construir para corregir los errores
        al procesar el archivo .glade
        """
        self.bnf_treeview = self.glade.get_widget("bnf_treeview")
        self.thompson_treeview = self.glade.get_widget("thompson_treeview")
        self.subconjuntos_treeview = self.glade.get_widget("subconjuntos_treeview")
        self.minimo_treeview = self.glade.get_widget("minimo_treeview")
        
        self.tabla_simbolos_treeview = self.glade.get_widget("tabla_simbolos_treeview")
        
        self.bnf_store = self.build_tree_view("BNF",self.bnf_treeview)
        label = "Tabla de transiciones"
        self.thompson_store = self.build_tree_view(label,\
                self.thompson_treeview)
        
        self.subconjuntos_store = self.build_tree_view(label,\
                self.subconjuntos_treeview)
        
        self.minimo_store = self.build_tree_view(label,\
                self.minimo_treeview)
                
        self.tabla_simbolos_store = self.build_tree_view(\
                "Tabla de Simbolos",self.tabla_simbolos_treeview)
                
    def __init_canvas__(self):
        """
        Este método obtiene las referencias de los labels en los cuales
        se cargaran las imagenes
        """
        self.thompson_image = self.glade.get_widget("thompson_image")
        self.subconjutos_image = self.glade.get_widget("subconjuntos_image")
        self.minimo_image = self.glade.get_widget("minimo_image")
        
    def __init_automata_params__(self):
        """
        Este método inicializa las variables que seran utilizadas por
        los algorimtos
        """
        self.keys = Keys()
        self.afn = None
        self.afn_svg = "images/afn.svg"
        self.afd_svg = "images/afd.svg"
        self.afd_min_svg = "images/afd_min.svg"
        self.afd = None
        self.afd_min = None
        self.bnf = None

    
    def on_main_delete_event(self, widget, event):
        """
        Este metodo se encarga de salir del bucle de enventos de gtk 
        para finalizar la aplicación
        """
        gtk.main_quit()
    
    def on_simulacion_clicked(self, widget):
        """
        Este método se encarga de inicializar el simulador
        """        
        Simulador(self.afd_min ,self.afn)

    def on_ejecutar_clicked(self, widget):
        """
        Se en carga realizar el analisis lexico de la expresion 
        ingresada por el usuario
        """
        texto = self.expresion_entry.get_text().strip()
        if texto == "" :
            self.show_error_dialog("Debe especificar una expresión")
        
        try:
            a = Analizador(texto, self.keys);
            a.start()
        except Exception as inst:
            self.show_error_dialog(str(inst))
            return;
        
        self.__ejecutar_thompson(a.postfija)
        
        self.__ejecutar_subconjutos()
        
        self.__ejecutar_minimo()

        #se reinicia el indice de los estados
        Estado.ID = 1
        #se obtiene el bnf apartir del afd_minimo
        _bnf = Bnf(self.afd_min)
        self.bnf = _bnf.start_bnf()
        #se limpia el store del bnf
        self.__clean_store__(self.bnf_store)
        #se añaden el store del treeview
        for produccion in self.bnf : 
            self.bnf_store.append([self.bnf[produccion]])

    def __ejecutar_thompson(self, expresion_postfija):
        """
        Este método se encarga de ejecutar el algoritmo de thompson
        """
        thompson = Thompson(expresion_postfija)
        self.afn = thompson.start()
        #se dibuja el automata
        svg = SVGManager(self.afn_svg)
        svg.gen_svg_from_automata(self.afn)
        #se actualiza las el canvas
        self.thompson_image.set_from_file(self.afn_svg)
        
        for arco in self.afn.arcos :
            self.thompson_store.append([str(arco)])
    
    def __ejecutar_subconjutos(self):
        """
        Este método se encarga de ejecutar el algoritmo de subconjuntos
        """
        subconjuntos = Subconjuntos(self.afn, self.keys)
        self.afd = subconjuntos.start_subconjutos()
        #se dibuja el automata
        svg = SVGManager(self.afd_svg)
        svg.gen_svg_from_automata(self.afd)
        #se actualiza las el canvas
        self.subconjutos_image.set_from_file(self.afd_svg)
        for arco in self.afd.arcos :
            self.subconjuntos_store.append([str(arco)])
        
    def __ejecutar_minimo(self):
        """
        Este método se encarga de ejecutar el algoritmo de minimización
        """
        _afd = AFD(self.afd)
        self.afd_min = _afd.minimizar()
        #se dibuja el automata
        svg = SVGManager(self.afd_min_svg)
        svg.gen_svg_from_automata(self.afd_min)
        #se actualiza las el canvas
        self.minimo_image.set_from_file(self.afd_min_svg)
        for arco in self.afd_min.arcos :
            self.minimo_store.append([str(arco)])
            
    def on_anhadir_clicked(self, widget):
        """
        Se encarga de agregar una definicion regular ingresada por 
        el usuario a la tabla de simbolos
        """
        
        texto = self.expresion_entry.get_text().strip()
        def_reg = texto.split("=")
        print def_reg
        if len(def_reg) != 2 or def_reg[0] == "" or def_reg[1] == "":
            self.show_error_dialog(\
                "Introdusca correctamente la definición regular")
            
            return

        self.keys.set_tabla_simbolos_value_at(def_reg[0],def_reg[1])
        self.tabla_simbolos_store.append([texto])


    def on_editar_clicked(self, widget):
        EditorAlfabeto(self.keys)
        
        
    ###################################################################
    def __clean_store__(self, store) :
        """
        Este método limpia el store del tree view
        """
        store = gtk.ListStore(str)
        
    def show_error_dialog(self, message):
        """
        Este método genera un dialogBox de error.
        """
        dialog = gtk.MessageDialog(self.main_window,
                type=gtk.MESSAGE_ERROR, 
                buttons=gtk.BUTTONS_CLOSE,
                message_format=message)
        dialog.set_title("Error")
        dialog.run()
        dialog.destroy()
    
    def create_column(self, tree_view, column_title):
        """
        Este metodo crea una columna en el tree_view
        """
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn(column_title, rendererText, text=0)
        tree_view.append_column(column)
    
    def build_tree_view(self, column, tree_view):
        """
        Este metodo se encarga de construir un tree_view
        """
        store_model = gtk.ListStore(str)
        tree_view.set_model(store_model)
        tree_view.set_rules_hint(True)
        self.create_column(tree_view, column)
        return store_model



if __name__ == "__main__":

    try:
        a = App()
        gtk.main()
    except KeyboardInterrupt:
        pass
    
    #~ er = "(a|b)+"
    #~ 
    #~ keys = Keys()
    #~ keys.set_tabla_simbolos_value_at("a_or_b","(a|b)")
    #~ print er
    #~ print "Start.."
    #~ #tokens = StringTokenizer (er, keys)
    #~ a = Analizador(er, keys);
    #~ if a.start():
        #~ print "Done.." + str(a.postfija)
    #~ 
    #~ t = Thompson(a.postfija)

    #~ t.start()

    #~ print len(t.automatas[0].estados)
    #~ 
    #~ draw(t.automatas[0])
    #~ sim = SimuladorAFN(t.automatas[0], "abb")
    #~ sim.gen_camino()
    #~ 
    #~ s = Subconjuntos(t.automatas[0])
    #~ af = s.start_subconjutos()
    #~ 
    #~ draw(af, "afd")
    #~ afd = AFD(af)
    #~ afd_min = afd.minimizar()
    #~ draw(afd_min, "minimo")
    #~ sim = SimulardorAFD(afd_min, "aabc")
    #~ has_more = sim.next_state()
    #~ while has_more : 
        #~ direccion = raw_input()
        #~ 
        #~ if direccion == "N" :
            #~ has_more = sim.next_state()
        #~ elif direccion == "P" :
            #~ has_more = sim.previous_state()
            #~ 
    #~ #b = Bnf(afd_min)
    #~ #b.start_bnf()

