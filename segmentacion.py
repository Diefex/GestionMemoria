from math import floor
from random import random, randint
from gestor import Gestor

class Segmentacion(Gestor):
    def __init__(self, ram):
        super().__init__(ram)
        
        self.segmentos = []
        self.espacios = [[0, self.tam_ram]]
        
    
    def nuevo_proceso(self, tam, ajuste):
        proceso = []
        
        segmentos = tam.split(',')
        
        for tam_seg in segmentos:
        
            tam_seg = int(tam_seg)*1024
        
            if ajuste == 1:
                #Primer ajuste
                es = False
                for i in range(len(self.espacios)):
                    if self.espacios[i][1]>=tam_seg:
                        es = True
                        break
                if not es:
                    return False
            
            elif ajuste == 2:
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
            
            elif ajuste == 3:
                #Peor ajuste
                op = []
                for i in range(len(self.espacios)):
                    op.append(self.espacios[i][1]-tam_seg)
                
                i = op.index(max(op))
                if op[i]<0:
                    return False
                    
            pos = self.espacios[i][0]
            self.espacios[i][0] += tam_seg
            self.espacios[i][1] -= tam_seg
            if self.espacios[i][1]<=0:
                self.espacios.pop(i)
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
            self.RAM.borrar_division(seg[0])
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
                def k(e):
                    return e[0]
                self.espacios.sort(key=k)
        for i in range(len(self.espacios)):
            for j in range(len(self.espacios)):
                if i!=j:
                    if self.espacios[i][0]+self.espacios[i][1] == self.espacios[j][0]:
                        self.espacios[j][0] = self.espacios[i][0]
                        self.espacios[j][1]+= self.espacios[i][1]
                        self.espacios[i][1] = 0
                        break

                    if self.espacios[i][0] == self.espacios[j][0]+self.espacios[j][1]:
                        self.espacios[j][1]+= self.espacios[i][1]
                        self.espacios[i][1] = 0
                        break
        empty = []
        for i in range(len(self.espacios)):
            if self.espacios[i][1] == 0:
                empty.append(i)
        for e in empty:
            self.espacios.pop(e)

        proceso[1] = False

    def get_tabla_seg(self, i):
        tabla = [['Segmento', 'Dirección Base', 'Capacidad']]
        proceso = self.procesos[i][0]
        tabla.append(['Código', str(hex(self.segmentos[proceso[0][0]][0])), str(self.segmentos[proceso[0][0]][1]/1024)+'Kb'])
        tabla.append(['Datos', str(hex(self.segmentos[proceso[1][0]][0])), str(self.segmentos[proceso[1][0]][1]/1024)+'Kb'])
        tabla.append(['Pila', str(hex(self.segmentos[proceso[2][0]][0])), str(self.segmentos[proceso[2][0]][1]/1024)+'Kb'])
        for i in range(3, len(proceso)):
            tabla.append(['Segmento_'+str(i), str(hex(self.segmentos[proceso[i][0]][0])), str(self.segmentos[proceso[i][0]][1]/1024)+'Kb'])
        return tabla

    def get_tabla_esp(self):
        tabla = []
        tabla.append(['Dirección Base', 'Capacidad'])
        for esp in self.espacios:
            tabla.append([str(hex(esp[0])), str(esp[1]/1024)+'Kb'])
        return tabla