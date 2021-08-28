import tkinter as tk


class canvasRAM(tk.Canvas):
    def __init__(self, master=None):
        super().__init__(master, bg='black', width=1280, height=400)
        self.pack()

        self.crr = (int(self['width'])-1040)/2
        self.h = 20
        
        
        for i in range(16):
            hc = i*self.h
            p0 = i*0x100000
            p1 = p0+0xFFFFF
            self.create_text(self.crr-35, 3+hc+self.h/2, text=hex(p0), fill="white", font="consolas 10")
            self.create_text(35+self.crr+1040, 3+hc+self.h/2, text=hex(p1), fill="white", font="consolas 10")
            self.create_polygon(self.crr,3+hc,self.crr+1040+2,3+hc,self.crr+1040+2,self.h+hc,self.crr,self.h+hc,outline='white')
        
        self.segmentos = []

    def convertir(self, p):
        p = int((p/pow(2,24))*1040)
        return p

    def pintarSegmento(self, x, t):
        x = self.convertir(x)
        t = self.convertir(t)
        x = x+self.crr+1
        h = int(100)
        self.create_polygon(x,4,x+t+2,4,x+t+2,h-1,x,h-1,outline='red')
        
    
    def pintarSegmentos(self, t):
        t = int(t/1024)
        x = self.crr+1
        
        for j in range(16):
            for i in range(int(1024/t)):
                h = j*self.h
                self.create_polygon(x+(i*(t+1)),4+h,x+(i*(t+1))+t+1,4+h,x+(i*(t+1))+t+1,self.h-1+h,x+(i*(t+1)),self.h-1+h,outline='red')
                self.segmentos.append([x+(i*(t+1)), h])
                 

    def pintarProceso(self, i, t):
        
        t = int(t/1024)
        c = self.segmentos[i]
        self.create_polygon(1+c[0],5+c[1],t+1+c[0],5+c[1],t+1+c[0],self.h-1+c[1],1+c[0],self.h-1+c[1],fill='green')
