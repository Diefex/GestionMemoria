import tkinter as tk
from tkinter import ttk
from memoria import canvasRAM
from gestor import Paginacion

class Aplicacion:
    def __init__(self):
        self.ventana=tk.Tk()
        self.RAM = canvasRAM()
        self.gestor = Paginacion(self.RAM)

        self.panel_nproceso()
        self.panel_qproceso()
        self.panel_inf()
               
        self.RAM.grid(column=0, row=2, columnspan=2)
        
        self.ventana.mainloop()
        

    def panel_nproceso(self):
        self.lf1=ttk.LabelFrame(self.ventana,text="Nuevo Proceso")
        self.lf1.grid(column=0, row=0, sticky="w")
        self.label1=ttk.Label(self.lf1, text="Tamaño:")
        self.label1.grid(column=0,row=0, padx=5, pady=5)
        self.dato1=tk.StringVar()
        self.entry1=ttk.Entry(self.lf1, textvariable=self.dato1)
        self.entry1.grid(column=1, row=0, padx=5, pady=5)
        self.boton1=ttk.Button(self.lf1, text="Agregar Proceso", command=self.nuevo_proceso)
        self.boton1.grid(column=0, row=3, columnspan=2, padx=5, pady=5, sticky="we")

    def panel_qproceso(self):
        self.lf2=ttk.LabelFrame(self.ventana,text="Quitar Proceso")
        self.lf2.grid(column=1, row=0, sticky="w")
        self.ipr = tk.IntVar()
    
    def act_panel_qproceso(self):
        for w in self.lf2.grid_slaves():
            w.destroy()
        j = 0
        for i in range(len(self.gestor.procesos)):
            if self.gestor.procesos[i][1] == True:
                ttk.Radiobutton(self.lf2, text="Proceso "+str(i), variable=self.ipr, value=i).grid(column=j, row=1, padx=5, pady=5, sticky="we")
                j+=1
        ttk.Button(self.lf2, text="Terminar Proceso", command=self.quitar_proceso).grid(column=0, row=3, columnspan=2, padx=5, pady=5, sticky="we")
        
    def panel_inf(self):
        self.lf3=ttk.Labelframe(self.ventana, text="Informacion")
        self.lf3.grid(column=0, row=1, columnspan=2, sticky="w")
        self.lbl=ttk.Label(self.lf3, text="Informacion")
        self.lbl.grid(column=0, row=0, padx=5, pady=5, sticky="we")

    def nuevo_proceso(self):
        tam = self.dato1.get()
        if tam!='':
            tam = int(tam)
        else:
            tam = 0

        self.gestor.nuevo_proceso(tam)
        self.act_panel_qproceso()
    
    def quitar_proceso(self):
        pr = self.ipr.get()
        if len(self.gestor.procesos)!=0:
            self.gestor.terminar_proceso(pr)
            self.act_panel_qproceso()
    
    def pintar_division(self, tam):
        self.RAM.pintar_division(tam)
        
ap = Aplicacion()