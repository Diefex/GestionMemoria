from tkinter import Tk, Canvas, Button, Label

def pintarSegmento(x, t):
    canvas.create_polygon(x,0,x+t,0,x+t,canvas['height'],x,canvas['height'],outline='blue')
def cuadroC(x, y, w, h, c):
    canvas.create_polygon(x,y,x+w,y,x+w,y+h,x,y+h,outline=c)

def pintarPos(p):
    canvas.create_line(p, 3, p, int(canvas['height']), fill='green')
def convertirPos(p):
    p = int((p/pow(2,24))*int(canvas['width']))
    return p



ventana = Tk()

Label(ventana, text="RAM").pack()


#canvas
canvas = Canvas(ventana, bg='black', width=1280, height=100)
canvas.pack()




pintarSegmento(convertirPos(0x0FFFF0), convertirPos(0x0FFF0F))
        

for i in range(convertirPos(0x0FFFF0), convertirPos(0xF00000)):
    pintarPos(i)




ventana.hi_there.pack(side="top")


ventana.mainloop()

