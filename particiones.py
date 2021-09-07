from math import floor
from gestor import Gestor

class EstaticaFija(Gestor):
    def __init__(self, ram):
        super().__init__(ram)
        self.tam_par = 0x40000
        self.particiones=[]
        for i in range(int(self.tam_ram/self.tam_par)):
            self.particiones.append(0)
        self.hacer_particiones()
    
    def nuevo_proceso(self, tam):
        
        if (tam>self.tam_par):
            print("El tamano del proceso exede la particion")
        else:
            for i in range(len(self.particiones)):
                if self.particiones[i] == 0:    
                    self.particiones[i] = tam
                    break
            proceso = i
            self.procesos.append([proceso, True])
            
            cl = self.RAM.colores[len(self.procesos)%len(self.RAM.colores)]
            self.RAM.pintar_proceso(proceso, self.particiones[proceso], cl)
        

    def terminar_proceso(self, i):
        proceso = self.procesos[i]
        self.RAM.pintar_proceso(proceso[0], self.particiones[proceso[0]], 'black')
        self.particiones[proceso[0]] = 0
        proceso[1] = False
        

    def hacer_particiones(self):
        for i in range(len(self.particiones)):
            self.RAM.pintar_division(i*self.tam_par,self.tam_par)

class EstaticaVariable(Gestor):
    def __init__(self, ram):
        super().__init__(ram)
        
        self.particiones=[
            [0, 0x100000],
            [0, 0x80000],
            [0, 0x80000],
            [0, 0x40000],
            [0, 0x40000],
            [0, 0x40000],
            [0, 0x40000]
        ]
        self.hacer_particiones()
    
    def nuevo_proceso(self, tam):
        #Primer ajuste
        for i in range(len(self.particiones)):
            if self.particiones[i][0] == 0:    
                self.particiones[i][0] = tam
                proceso = i
                break
        
        self.procesos.append([proceso, True])
        
        cl = self.RAM.colores[len(self.procesos)%len(self.RAM.colores)]
        self.RAM.pintar_proceso(proceso, self.particiones[proceso][0], cl)
        

    def terminar_proceso(self, i):
        proceso = self.procesos[i]
        self.RAM.pintar_proceso(proceso[0], self.particiones[proceso[0]][0], 'black')
        self.particiones[proceso[0]][0] = 0
        proceso[1] = False
        

    def hacer_particiones(self):
        pos = 0
        for i in range(len(self.particiones)):
            self.RAM.pintar_division(pos, self.particiones[i][1])
            pos += self.particiones[i][1]

class Dinamica(Gestor):
    def __init__(self, ram):
        super().__init__(ram)

        self.particiones = []
        self.espacios = [[0, self.tam_ram]]

    def nuevo_proceso(self, tam):
        #Mejor ajuste
        op = []
        for i in range(len(self.espacios)):
            op.append(self.espacios[i][1]-tam)
        
        for i in range(len(op)):
            if op[i]<0:
                op[i]=self.tam_ram+1
        i = op.index(min(op))
        pos = self.espacios[i][0]
        self.espacios[i][0] += tam
        self.espacios[i][1] -= tam

        self.particiones.append([tam, pos])
        self.procesos.append([len(self.particiones)-1, True])
        self.RAM.pintar_division(pos, tam)

        cl = self.RAM.colores[len(self.procesos)%len(self.RAM.colores)]
        self.RAM.pintar_proceso(len(self.particiones)-1, tam, cl)

    def terminar_proceso(self, i):
        proceso = self.procesos[i]
        self.RAM.pintar_proceso(proceso[0], self.particiones[proceso[0]][0], 'black')
        espacio = [self.particiones[proceso[0]][1], self.particiones[proceso[0]][0]]
        for i in range(len(self.espacios)):
            if espacio[0]+espacio[1] == self.espacios[i][0]:
                self.espacios[i][0]  = espacio[0]
                self.espacios[i][1] += espacio[1]
                espacio[1] = 0
                break

            if espacio[0] == self.espacios[i][0]+self.espacios[i][1]:
                self.espacios[i][1] += espacio[1]
                espacio[1] = 0
                break
        if espacio[1]>0:
            self.espacios.append(espacio)
            
        proceso[1] = False