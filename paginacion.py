from math import floor
from gestor import Gestor

class Paginacion(Gestor):
    def __init__(self, ram):
        super().__init__(ram)
        self.tam_pag = 0x10000
        self.marcos=[]
        self.n_marcos = int(self.tam_ram/self.tam_pag)
        for i in range(self.n_marcos):
            self.marcos.append(0)
        self.hacer_marcos()
    
    def nuevo_proceso(self, tam):
        proceso = []
        n = floor(tam/self.tam_pag)
        if(tam%self.tam_pag != 0):
            n+=1
        for i in range(n):
            j = 0
            m = self.marcos[j]
            while m!=0:
                j+=1
                m = self.marcos[j]
            if(tam <= self.tam_pag):
                self.marcos[j] = tam
            else:
                tam = tam-self.tam_pag
                self.marcos[j] = self.tam_pag
            
            proceso.append(j)
            
        self.procesos.append([proceso, True])

        cl = self.RAM.colores[len(self.procesos)%len(self.RAM.colores)]
        for pag in proceso:
            self.RAM.pintar_proceso(pag, self.marcos[pag], cl)

    def terminar_proceso(self, i):
        proceso = self.procesos[i]
        for pag in proceso[0]:
            self.RAM.pintar_proceso(pag, self.marcos[pag], 'black')
            self.marcos[pag] = 0
        proceso[1] = False

    def hacer_marcos(self):
        for i in range(len(self.marcos)):
            self.RAM.pintar_division(i*self.tam_pag, self.tam_pag)