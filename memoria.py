from tkinter import Canvas
from math import floor


class canvasRAM(Canvas):
    def __init__(self, master=None, h=20):
        super().__init__(master, bg='black', width=1280, height=h*16)

        self.tcr = 1024
        self.crX = ((int(self['width'])-self.tcr)/2)-1
        self.crY = 5
        self.hcr = h-self.crY
        
        for i in range(16):
            hc = i*(self.crY+self.hcr)+self.crY
            p0 = i*0x100000
            p1 = p0+0xFFFFF
            self.create_text(self.crX-35, hc+self.hcr/2, text=hex(p0), fill="white", font="consolas 10")
            self.create_text(35+self.crX+self.tcr, hc+self.hcr/2, text=hex(p1), fill="white", font="consolas 10")

            x1 = self.crX
            x2 = self.crX+self.tcr+1
            y1 = hc
            y2 = hc+self.hcr
            self.create_polygon(x1, y1, x2, y1, x2, y2, x1, y2, outline='white')
        
        #Lista de divisiones
        self.divisiones = []
        #Lista de colores
        self.colores = ['violet red', 'green', 'orange', 'cyan', 'pink', 'blue violet', 'orchid', 'lawn green', "blue", "cyan", "magenta", "chocolate", "coral", "plum", "snow4", "gold", "peru", "maroon", "blue violet", "orchid", "firebrick", "wheat", "SkyBlue"]

    def pintar_division(self, pos, tam):
        tam = floor(tam/1024)
        pos = floor(pos/1024)
        
        self.divisiones.append([pos, tam])
        
        r = floor(pos/1024)
        x = self.crX+1+pos-(r*1024)
        y1 = r*(self.crY+self.hcr)+self.crY+(self.hcr/2)
        y2 = r*(self.crY+self.hcr)+self.crY+self.hcr+1
        self.create_line(x,y1,x,y2,fill='red')

        pos = pos + tam -1

        r = floor(pos/1024)
        x = self.crX+1+pos-(r*1024)
        y1 = r*(self.crY+self.hcr)+self.crY+(self.hcr/2)
        y2 = r*(self.crY+self.hcr)+self.crY+self.hcr+1
        self.create_line(x,y1,x,y2,fill='red')

    def borrar_division(self, i):
        pos = self.divisiones[i][0]
        r = floor(pos/1024)
        x = self.crX+1+pos-(r*1024)
        y1 = r*(self.crY+self.hcr)+self.crY+(self.hcr/2)
        y2 = r*(self.crY+self.hcr)+self.crY+self.hcr+1
        self.create_line(x,y1,x,y2,fill='black')
        self.create_line(x,y2-1,x,y2,fill='white')

        pos = pos + self.divisiones[i][1] -1
        r = floor(pos/1024)
        x = self.crX+1+pos-(r*1024)
        y1 = r*(self.crY+self.hcr)+self.crY+(self.hcr/2)
        y2 = r*(self.crY+self.hcr)+self.crY+self.hcr+1
        self.create_line(x,y1,x,y2,fill='black')
        self.create_line(x,y2-1,x,y2,fill='white')

    def pintar_proceso(self, i, tam, cl):      
        
        for t in range(int(tam/1024)):
            pos = self.divisiones[i][0]
            pos = pos+t
            r = floor(pos/1024)
            pos = self.crX+1+pos-(r*1024)
            x = pos
            y1 = r*(self.crY+self.hcr)+self.crY+1
            y2 = r*(self.crY+self.hcr)+self.crY+self.hcr
            self.create_line(x, y1, x, y2, fill=cl)

    
        pos = self.divisiones[i][0]
        r = floor(pos/1024)
        x = self.crX+1+pos-(r*1024)
        y1 = r*(self.crY+self.hcr)+self.crY+(self.hcr/2)
        y2 = r*(self.crY+self.hcr)+self.crY+self.hcr+1
        self.create_line(x,y1,x,y2,fill='red')

        pos = pos + self.divisiones[i][1] -1
        r = floor(pos/1024)
        x = self.crX+1+pos-(r*1024)
        y1 = r*(self.crY+self.hcr)+self.crY+(self.hcr/2)
        y2 = r*(self.crY+self.hcr)+self.crY+self.hcr+1
        self.create_line(x,y1,x,y2,fill='red')