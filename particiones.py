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
        if self.particiones[-1]!=0:
            return False
        
        if (tam>self.tam_par):
            return False
        else:
            for i in range(len(self.particiones)):
                if self.particiones[i] == 0:    
                    self.particiones[i] = tam
                    break
            proceso = i
            self.procesos.append([proceso, True])
            
            cl = self.RAM.colores[len(self.procesos)%len(self.RAM.colores)]
            self.RAM.pintar_proceso(proceso, self.particiones[proceso], cl)
            return True
        

    def terminar_proceso(self, i):
        proceso = self.procesos[i]
        self.RAM.pintar_proceso(proceso[0], self.particiones[proceso[0]], 'black')
        self.particiones[proceso[0]] = 0
        proceso[1] = False
        

    def hacer_particiones(self):
        for i in range(len(self.particiones)):
            self.RAM.pintar_division(i*self.tam_par,self.tam_par)

    def get_tabla_par(self):
        tabla = []
        tabla.append(["Particion", "Proceso", "Ocupación"])
        for i in range(len(self.particiones)):
            if self.particiones[i]!=0:
                tabla.append([str(i), 
                "Proceso_"+str(self.procesos.index([i, True])),
                str((self.particiones[i]/self.tam_par)*100)+"%"])
            else:
                tabla.append([str(i), 
                "Ninguno",
                "0%"])
        return tabla

class EstaticaVariable(Gestor):
    def __init__(self, ram):
        super().__init__(ram)
        
        self.particiones=[
            [0, 0x100000], [0, 0x100000], [0, 0x100000],
            [0, 0x80000], [0, 0x80000],
            [0, 0x80000], [0, 0x80000],
            [0, 0x80000], [0, 0x80000],
            [0, 0x40000], [0, 0x40000], [0, 0x40000], [0, 0x40000],
            [0, 0x40000], [0, 0x40000], [0, 0x40000], [0, 0x40000],
            [0, 0x40000], [0, 0x40000], [0, 0x40000], [0, 0x40000],
            [0, 0x20000], [0, 0x20000], [0, 0x20000], [0, 0x20000], [0, 0x20000], [0, 0x20000], [0, 0x20000], [0, 0x20000],
            [0, 0x20000], [0, 0x20000], [0, 0x20000], [0, 0x20000], [0, 0x20000], [0, 0x20000], [0, 0x20000], [0, 0x20000],
            [0, 0x20000], [0, 0x20000], [0, 0x20000], [0, 0x20000], [0, 0x20000], [0, 0x20000], [0, 0x20000], [0, 0x20000],
        ]
        for i in range(16*3):
            self.particiones.append([0, 0x10000])
        for i in range(32):
            self.particiones.append([0, 0x8000])

        self.hacer_particiones()
    
    def nuevo_proceso(self, tam):
        proceso = -1
        #Primer ajuste
        for i in range(len(self.particiones)):
            if (self.particiones[i][0] == 0) and (self.particiones[i][1]>=tam):    
                self.particiones[i][0] = tam
                proceso = i
                break
        
        if proceso == -1:
            return False
        self.procesos.append([proceso, True])
        
        cl = self.RAM.colores[len(self.procesos)%len(self.RAM.colores)]
        self.RAM.pintar_proceso(proceso, self.particiones[proceso][0], cl)
        return True
        

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

    def get_tabla_par(self):
        tabla = []
        tabla.append(["Particion","Capacidad", "Proceso", "Ocupación"])
        for i in range(len(self.particiones)):
            cap = floor(self.particiones[i][1]/1024)
            if self.particiones[i][0]!=0:
                tabla.append([str(i), 
                str(cap)+"Kb", 
                "Proceso_"+str(self.procesos.index([i, True])),
                str((self.particiones[i][0]/(cap*1024))*100)+"%"])
            else:
                tabla.append([str(i), 
                str(cap)+"Kb", 
                "Ninguno",
                "0%"])
        return tabla

class Dinamica(Gestor):
    def __init__(self, ram):
        super().__init__(ram)

        self.particiones = []
        self.espacios = [[0, self.tam_ram]]

    def nuevo_proceso(self, tam, ajuste):
        if ajuste == 1:
            #Primer ajuste
            es = False
            for i in range(len(self.espacios)):
                if self.espacios[i][1]>=tam:
                    es = True
                    break
            if not es:
                return False
        
        elif ajuste == 2:
            #Mejor ajuste
            op = []
            for i in range(len(self.espacios)):
                op.append(self.espacios[i][1]-tam)
            
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
                op.append(self.espacios[i][1]-tam)
            
            i = op.index(max(op))
            if op[i]<0:
                return False
        
        pos = self.espacios[i][0]
        self.espacios[i][0] += tam
        self.espacios[i][1] -= tam
        if self.espacios[i][1]<=0:
                self.espacios.pop(i)

        self.particiones.append([tam, pos])
        self.procesos.append([len(self.particiones)-1, True])

        self.RAM.pintar_division(pos, tam)
        cl = self.RAM.colores[len(self.procesos)%len(self.RAM.colores)]
        self.RAM.pintar_proceso(len(self.particiones)-1, tam, cl)
        return True

    def terminar_proceso(self, i):
        proceso = self.procesos[i]
        self.RAM.pintar_proceso(proceso[0], self.particiones[proceso[0]][0], 'black')
        self.RAM.borrar_division(proceso[0])
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
            def k(e):
                return e[0]
            self.espacios.sort(key=k)
            
        proceso[1] = False
    
    def get_tabla_par(self):
        tabla = []
        tabla.append(["Proceso","Dirección Base", "Capacidad"])
        for i in range(len(self.particiones)):
            if self.procesos[i][1]:
                cap = floor(self.particiones[i][0]/1024)

                tabla.append(["Proceso_"+str(self.procesos.index([i, True])),
                str(hex(self.particiones[i][1])), 
                str(cap)+"Kb"])
            
        return tabla

    def get_tabla_esp(self):
        tabla = []
        tabla.append(['Dirección Base', 'Capacidad'])
        for esp in self.espacios:
            tabla.append([str(hex(esp[0])), str(esp[1]/1024)+'Kb'])
        return tabla

    def compactar(self):
        espacio = self.espacios[0]
        c = 0
        while len(self.espacios)!=1 and c<100:

            for i in range(len(self.procesos)):
                if self.procesos[i][1] == True:
                    p=self.procesos[i][0]
                    if espacio[0]+espacio[1]==self.particiones[p][1]:
                        self.particiones.append([self.particiones[p][0], espacio[0]])
                        espacio[0] = espacio[0]+self.particiones[p][0]
                        self.procesos[i][0] = len(self.particiones)-1

                        self.RAM.pintar_proceso(p, self.particiones[p][0], 'black')
                        self.RAM.borrar_division(p)

                        self.RAM.pintar_division(self.particiones[-1][1], self.particiones[-1][0])
                        cl = self.RAM.colores[(i+1)%len(self.RAM.colores)]
                        self.RAM.pintar_proceso(len(self.particiones)-1, self.particiones[-1][0], cl)

            for i in range(1,len(self.espacios)):
                if espacio[0]+espacio[1]==self.espacios[i][0]:
                    self.espacios[i][0] = espacio[0]
                    self.espacios[i][1]+= espacio[1]
                    self.espacios.pop(0)
                    espacio = self.espacios[0]
                    break
            
            c+=1