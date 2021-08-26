import tkinter as tk


class canvasRAM(tk.Canvas):
    def __init__(self, master=None):
        super().__init__(master, bg='black', width=1100, height=100)
        self.pack()
        self.crr = (int(self['width'])-1024)/2
        
        self.create_polygon(self.crr,3,self.crr+1024+2,3,self.crr+1024+2,100,self.crr,100,outline='white')
        pass

    def convertir(self, p):
        p = int((p/pow(2,24))*1024)
        return p

    def pintarSegmento(self, x, t):
        x = self.convertir(x)
        t = self.convertir(t)
        x = x+self.crr+1
        h = int(100)
        canvas.create_polygon(x,4,x+t+2,4,x+t+2,h-1,x,h-1,outline='red')

    def pintarProceso(self, x, t):
        x = self.convertir(x)
        t = self.convertir(t)
        x = x+self.crr+2
        h = int(100)
        canvas.create_polygon(x,5,x+t,5,x+t,h-2,x,h-2,fill='green')



#Creacion de la ventana
ventana = tk.Tk()
tk.Label(ventana, text="RAM").pack()

#canvas para dibujar la RAM
canvas = canvasRAM(master=ventana)
canvas.pack()


#Puebas de pintar
canvas.pintarSegmento(0x0,0xFFFFF)
canvas.pintarSegmento(0xFFFFF,0x1FFFFE)

canvas.pintarProceso(0x0, 0xAF000)
canvas.pintarProceso(0xFFFFF, 0xFFFFF)


#Correr ventana
ventana.mainloop()