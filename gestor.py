from math import floor
import tkinter as tk
from memoria import canvasRAM

tam_pag = 0x10000
tam_ram = 0x1000000

marcos=[]

n_marcos = int(tam_ram/tam_pag)

for i in range(n_marcos):
    marcos.append(0)


def asignar_proceso(tam):
    p = []
    n = floor(tam/tam_pag)
    if(tam%tam_pag != 0):
        n+=1
    for i in range(n):
        j = 0
        m = marcos[j]
        while m!=0:
            j+=1
            m = marcos[j]
        if(tam <= tam_pag):
            marcos[j] = tam
        else:
            tam = tam-tam_pag
            marcos[j] = tam_pag
        p.append(j)
    
    return p

def terminar_proceso(tbl):
    for pag in tbl:
        marcos[pag] = 0


P1 = asignar_proceso(110*1024)
P2 = asignar_proceso(60*1024)
P3 = asignar_proceso(150*1024)
terminar_proceso(P2)
P4 = asignar_proceso(240*1024)


#Creacion de la ventana
ventana = tk.Tk()
tk.Label(ventana, text="RAM").pack()

#canvas para dibujar la RAM
canvas = canvasRAM(master=ventana)
canvas.pack()

#Puebas de pintar
canvas.pintarSegmentos(64*1024)
for i in range(len(marcos)):
    canvas.pintarProceso(i, marcos[i])

#Correr ventana
ventana.mainloop()