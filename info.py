from tkinter import *
from tkinter import ttk
import random as r #esto quitelo, lo use para meter datos aleatorios

ventana = Tk()
ventana.geometry("1000x400")
ventana.title("Tabla de procesos")

arbol = ttk.Treeview(ventana,height=12, columns=("","","","")) #en columns especificamos la cantidad de columanas que va a tener la tabla (4)  

arbol.column("#0", width = 500) #A cada columna le asignamos un tamaño
arbol.column("#1", width = 100)
arbol.column("#2", width = 100)
arbol.column("#3", width = 100)
arbol.column("#4", width = 100)

arbol.heading("#0",text="Info Procesos") #Tambien le asignamos un nombre
arbol.heading("#1",text="datos")
arbol.heading("#2",text="datos")
arbol.heading("#3",text="datos")
arbol.heading("#4",text="datos")

#Esta es la lista de donde tomas los datos
#Cada sublista es un proceso de la tabla principal, y cada elemento de esa sublista es la tabla interna del proceso en mencion
lista = ( (10,20,30), (12,40,40), (12,40,50), (112,1221,123), (123,33,4101), (1223,32,123) ) #esto tabula sin importar la cantidad de elementos de la tupla 

for i in lista: 
    datos_proc = ""
    
    #aqui se llenan los datos del proceso de la tabla principal (yo lo llene con aleatorios) pero en values se ponen los datos del proceso
    arbol.insert("", END , text="Proceso "+str(lista.index(i)), values=( str(r.randint(0,1000)), str(r.randint(0,100000)),str(r.randint(0,100000)),str(r.randint(0,100000)))) 
    #si es para tabular como una tabla normal (el gestor de particiones) todo lo de abajo no se necesita


    #sacamos la lista con los procesos para saber el index de la info de cada uno
    procesos = arbol.get_children() 
    
    #aqui hay dos formas de hacerlo, dentro de la misma columna de info procesos meter los datos del proceso:
    arbol.insert(procesos[lista.index(i)],END,text="DATOS\t\tDATOS\t\tDATOS")

    for k in i:
        datos_proc+=str(k) + "\t\t" #pero entonces concatenamos los datos con un string 
    arbol.insert(procesos[lista.index(i)],END,text=datos_proc) #Esto se puede meter en un for si necesita poner mas filas
    '''

    #La otra forma es poner la info de cada proceso en las mismas columnas de la tabla principal:
    arbol.insert(procesos[lista.index(i)],END,text="Informacion adcional", values = i) #Esto se puede meter en un for si necesita poner mas filas
                                                                           #La cantidad de values debe ser menor o igual que la cantidad de columnas
    '''

arbol.place(x=50,y=50)
#print(arbol.get_children())
ventana.mainloop()
