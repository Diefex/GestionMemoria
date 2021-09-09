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
        
        segmentos = tam.split(',')
        
        for tam_seg in segmentos:
        
            tam_seg = int(tam_seg)*1024
        
            #Mejor ajuste
            op = []
            for i in range(len(self.espacios)):
                op.append(self.espacios[i][1]-tam_seg)
            
            for i in range(len(op)):
                if op[i]<0:
                    op[i]=self.tam_ram+1
            i = op.index(min(op))
            if op[i]>self.tam_ram:
                return False
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
        return True

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
