from math import floor
from random import random, randint
from gestor import Gestor

class Segmentacion(Gestor):
    def __init__(self, ram):
        super().__init__(ram)
        
        self.segmentos = []
        self.espacios = [[0, self.tam_ram]]
        
    
    def nuevo_proceso(self, tam):
        proceso = []
        
        n_segmentos = randint(2,5)
        tam_ac = 0
        for i in range(n_segmentos):
            if i==n_segmentos-1:
                tam_seg = tam-tam_ac
            else:
                t = floor((tam-tam_ac)*randint(3,7)*(0.1))
                tam_seg = t-(t%1024)
                tam_ac += tam_seg
            
            #Mejor ajuste
            op = []
            for i in range(len(self.espacios)):
                op.append(self.espacios[i][1]-tam_seg)
            
            for i in range(len(op)):
                if op[i]<0:
                    op[i]=self.tam_ram+1
            i = op.index(min(op))
            pos = self.espacios[i][0]
            self.espacios[i][0] += tam_seg
            self.espacios[i][1] -= tam_seg

            self.segmentos.append([pos, tam_seg])
            proceso.append([len(self.segmentos)-1, tam_seg])
        
        self.procesos.append([proceso, True])
        
        
        cl = self.RAM.colores[len(self.procesos)%len(self.RAM.colores)]
        for seg in proceso:
            self.RAM.pintar_division(self.segmentos[seg[0]][0], self.segmentos[seg[0]][1])
            self.RAM.pintar_proceso(seg[0], seg[1], cl)

    def terminar_proceso(self, i):
        proceso = self.procesos[i]
        for seg in proceso[0]:
            self.RAM.pintar_proceso(seg[0], seg[1], 'black')
            espacio = [self.segmentos[seg[0]][0], self.segmentos[seg[0]][1]]
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
