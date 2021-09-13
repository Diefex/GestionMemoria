import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from memoria import canvasRAM

from segmentacion import Segmentacion
from paginacion import Paginacion
import particiones as particiones

from math import floor
from info import tabla

class Aplicacion:
    def __init__(self):
        self.init_ven_sel_gestores()
               

    def panel_nproceso(self):
        lf=ttk.LabelFrame(self.ventana,text="Nuevo Proceso")
        lf.grid(column=0, row=0, sticky="w")
        ttk.Label(lf, text="Tamaño (Kb):").grid(column=0,row=0, padx=5, pady=5)
        self.dato1=tk.StringVar()
        ttk.Entry(lf, textvariable=self.dato1).grid(column=1, row=0, padx=0, pady=5)
        ttk.Label(lf, text="Kb").grid(column=2, row=0, padx=0, pady=5)
        ttk.Button(lf, text="Agregar Proceso", command=self.nuevo_proceso).grid(column=0, row=3, columnspan=3, padx=5, pady=5, sticky="we")
        if isinstance(self.gestor, particiones.EstaticaFija) or isinstance(self.gestor, particiones.EstaticaVariable) or isinstance(self.gestor, particiones.Dinamica):
            ttk.Button(lf, text="Tabla de Particiones", command=lambda: self.hacer_tabla(self.gestor.get_tabla_par())).grid(column=0, row=4, columnspan=3, padx=5, sticky="we")
        if isinstance(self.gestor, particiones.Dinamica) or isinstance(self.gestor, Segmentacion):
            ttk.Button(lf, text="Tabla de Espacios", command=lambda: self.hacer_tabla(self.gestor.get_tabla_esp())).grid(column=0, row=5, columnspan=3, padx=5, sticky="we")

    def panel_qproceso(self):
        self.lf2=ttk.LabelFrame(self.ventana,text="Procesos")
        self.lf2.grid(column=2, row=0, sticky="w")
        self.ipr = tk.IntVar()
    
    def act_panel_qproceso(self):
        for w in self.lf2.grid_slaves():
            w.destroy()
        
        for i in range(len(self.gestor.procesos)):
            if self.gestor.procesos[i][1] == True:
                cl = self.RAM.colores[(i+1)%len(self.RAM.colores)]
                tk.Radiobutton(self.lf2, text="Proceso_"+str(i), bg=cl, variable=self.ipr, value=i).grid(column=i%9, row=1+floor(i/9), padx=5, pady=5, sticky="we")
                
        ttk.Button(self.lf2, text="Terminar Proceso", command=self.quitar_proceso).grid(column=0, row=3+floor(i/9), columnspan=2, padx=5, pady=5, sticky="we")
        if isinstance(self.gestor, Paginacion):
            ttk.Button(self.lf2, text="Tabla de Páginas", command=lambda: self.hacer_tabla(self.gestor.get_tabla_pag(i))).grid(column=2, row=3+floor(i/9), columnspan=2, padx=5, sticky="we")
        if isinstance(self.gestor, Segmentacion):
            ttk.Button(self.lf2, text="Tabla de Segmentos", command=lambda: self.hacer_tabla(self.gestor.get_tabla_seg(i))).grid(column=2, row=3+floor(i/9), columnspan=2, padx=5, sticky="we")

    def panel_algoritmos(self, c):
        lf=ttk.LabelFrame(self.ventana,text="Ajustes")
        lf.grid(column=1, row=0, sticky="w")
        self.ajuste = tk.IntVar()
        pr=ttk.Radiobutton(lf, text="Primer Ajuste", variable=self.ajuste, value=1)
        pr.grid(column=0, row=0, padx=5, pady=1, sticky="we")
        pr.invoke()
        ttk.Radiobutton(lf, text="Mejor Ajuste", variable=self.ajuste, value=2).grid(column=0, row=1, padx=5, pady=1, sticky="we")
        ttk.Radiobutton(lf, text="Peor Ajuste", variable=self.ajuste, value=3).grid(column=0, row=2, padx=5, pady=1, sticky="we")
        if c:
            ttk.Checkbutton(lf, text="Compactar", variable=self.comp).grid(column=0, row=3, padx=5, pady=7, sticky="we")
            

    def nuevo_proceso(self):
        tam = self.dato1.get()
        if tam!='':
            if len(tam.split(','))>2 and isinstance(self.gestor, Segmentacion):
                pass
            elif len(tam.split(','))>1:
                tam = 0
            elif isinstance(self.gestor, Segmentacion):
                tam = 0
            else:
                try:
                    tam = int(tam)*1024
                except:
                    tam=0
                    messagebox.showinfo('Solo enteros', 'Por favor introduzca un numero entero')
        else:
            tam = 0
        if tam!=0:
            if isinstance(self.gestor, particiones.Dinamica) or isinstance(self.gestor, Segmentacion):
                if self.gestor.nuevo_proceso(tam, self.ajuste.get()):
                    self.act_panel_qproceso()
                else:
                    messagebox.showerror('No Hay Memoria', "No queda memoria donde ubicar el proceso")
            else:
                if self.gestor.nuevo_proceso(tam):
                    self.act_panel_qproceso()
                else:
                    messagebox.showerror('No Hay Memoria', "No queda memoria donde ubicar el proceso")
        else:
            messagebox.showwarning('Tamaño no Valido', "Introduzca un tamaño de proceso válido")
    
    def quitar_proceso(self):
        pr = self.ipr.get()
        if len(self.gestor.procesos)!=0:
            self.gestor.terminar_proceso(pr)
            if self.comp.get():
                self.gestor.compactar()
            self.act_panel_qproceso()

    def hacer_tabla(self, tbl):
        tabla(tbl)

    def init_ventana_principal(self, gestor):
        self.ven_sel_gestores.destroy()
        self.ventana=tk.Tk()
        self.RAM = canvasRAM()

        if(gestor==1):
            self.gestor = particiones.EstaticaFija(self.RAM)
        elif(gestor==2):
            self.gestor = particiones.EstaticaVariable(self.RAM)
        elif(gestor==3):
            self.gestor = particiones.Dinamica(self.RAM)
        elif(gestor==4):
            self.gestor = Paginacion(self.RAM)
        elif(gestor==5):
            self.gestor = Segmentacion(self.RAM)
        else:
            return

        self.panel_nproceso()
        self.panel_qproceso()

        self.comp = tk.BooleanVar()
        self.comp.set(False)

        if isinstance(self.gestor, particiones.Dinamica):
            self.panel_algoritmos(True)
        elif isinstance(self.gestor, Segmentacion):
            self.panel_algoritmos(False)
               
        self.RAM.grid(column=0, row=2, columnspan=3)

        self.ventana.resizable(0,0)
        self.ventana.mainloop()
    
    def init_ven_sel_gestores(self):
        self.ven_sel_gestores = tk.Tk()
        lf=ttk.LabelFrame(self.ven_sel_gestores,text="Seleccionar Gestor")
        lf.grid(column=0, row=0, sticky="w", padx=10, pady=10)

        gestor = tk.IntVar()
        gestor.set(1)
        ttk.Radiobutton(lf, text="Particiones Estáticas Fijas", variable=gestor, value=1).grid(column=0, row=0, sticky="w")
        ttk.Radiobutton(lf, text="Particiones Estáticas Variables", variable=gestor, value=2).grid(column=0, row=1, sticky="w")
        ttk.Radiobutton(lf, text="Particiones Dinámicas", variable=gestor, value=3).grid(column=0, row=2, sticky="w")
        ttk.Radiobutton(lf, text="Paginación", variable=gestor, value=4).grid(column=0, row=3, sticky="w")
        ttk.Radiobutton(lf, text="Segmentación", variable=gestor, value=5).grid(column=0, row=4, sticky="w")
        ttk.Button(self.ven_sel_gestores, text="Seleccionar", command=lambda: self.init_ventana_principal(gestor.get())).grid(column=0, row=1)
        
        self.ven_sel_gestores.resizable(0,0)
        self.ven_sel_gestores.mainloop()
        
ap = Aplicacion()