from math import floor
from gestor import Gestor

class EstaticaFija(Gestor):
    def __init__(self, ram):
        super().__init__(ram)
        self.tam_par = 256*1024
        self.particiones=[]
        self.n_particiones = int(self.tam_ram/self.tam_par)
        self.n_proceso = 0
        for i in range(self.n_particiones):
            self.particiones.append(0)
        self.hacer_particiones(self.n_particiones)
    
    def nuevo_proceso(self, tam):
        
        if (tam>self.tam_par):
            print("El tamano del proceso exede la particion")
        else:
            for i in range(self.n_particiones):
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
        

    def hacer_particiones(self, n):
        for i in range(n):
            self.RAM.pintar_division(self.tam_par)