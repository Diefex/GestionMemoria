from math import floor

class Gestor():
    def __init__(self, ram):
        self.procesos = []
        self.RAM = ram
        
    
    def nuevo_proceso(self, tam):
        pass
    
    def terminar_proceso(self, i):
        pass

class Paginacion(Gestor):
    def __init__(self, ram):
        super().__init__(ram)
        self.tam_pag = 0x10000
        self.tam_ram = 0x1000000
        self.marcos=[]
        self.n_marcos = int(self.tam_ram/self.tam_pag)
        for i in range(self.n_marcos):
            self.marcos.append(0)
        self.hacer_marcos()
    
    def nuevo_proceso(self, tam):
        p = []
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
            
            p.append(j)
            
        self.procesos.append(p)

    def terminar_proceso(self, tbl):
        for pag in tbl:
            self.marcos[pag] = 0

    def hacer_marcos(self):
        for i in range(8):
            self.RAM.pintar_division(self.tam_pag)