from tkinter import *
from tkinter import ttk

def tabla(tbl):
    ventana = Tk()
    head = tbl.pop(0)
    arbol = ttk.Treeview(ventana,height=12, columns=head[1:])

    for i in range(len(head)):
        arbol.heading("#"+str(i),text=head[i])

    for r in tbl: 
        arbol.insert("", END , text=r[0], values=r[1:])

    arbol.pack()
    ventana.mainloop()
