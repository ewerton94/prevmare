from numpy import cos,radians,pi,mean,arange
from datetime import datetime,timedelta
from matplotlib import pyplot as plt

class Mare(object):
    def __init__(self, H,w,G,data_inicial,niv_medio):
        self.H = H
        self.w = w
        self.G = G
        self.data_inicial = data_inicial
        self.niv_medio = niv_medio
        
    def cota(self,t):
        s = 0
        for i in range(len(H)):
            s+=2*self.H[i]*cos(2*pi/self.w[i]*t + self.G[i]*pi/180)
        return s

    def erros_e_cotas(self,j,horas,cs):
        cs2 = [self.cota(h.days*24 + h.seconds/3600 + j)+niv_medio for h in horas]
        erros = list(zip(cs,cs2))
        erro = [abs((erros[i][0]-erros[i][1])/niv_medio) for i in range(len(cs))]
        return (j,mean(erro)),cs2

#    M2    S2    N2   K2     K1    P1    Q1     L2  M1 
H = [0.809,0.279,0.166,0.079,0.048,0.016,.013,.024,.006]
w = [12.42,12,12.66,11.98,23.93,24.07,26.88,12.19,24.84]
G = [124,142,114,137,235,228,123,120,275]
data_inicial = (1977,7,1)
niv_medio = 1.40
'''
w = [12.42,12,12.66,11.98]
H = [0.738,.281,.151,.076]
G = [116,131,106,132]
data_inicial = (1983,1,2)
niv_medio = 1.24
'''
prev_mare = Mare(H,w,G,data_inicial,niv_medio)

tempos,cotas=[],[]
with open("natal.ewe","r") as arq:
    for linha in arq.readlines():
        linha = linha.split()
        if linha:
            if len(linha)>2:
                data = linha[1]
            tempos.append(datetime.strptime("%s %s"%(data,linha[-2]),"%d/%m/%Y %H:%M"))
            cotas.append(float(linha[-1]))

et = []
horas = list(map(lambda x:x-datetime(*data_inicial),tempos))

for j in range(0,2000):
    indice_e_erro = prev_mare.erros_e_cotas(j,horas,cotas)
    et.append(indice_e_erro[0])
menor_erro = min(et,key= lambda x:x[1])
indice_e_erro,cs2 = prev_mare.erros_e_cotas(menor_erro[0],horas,cotas)
delta = timedelta(indice_e_erro[0]/24)
print(tempos[0]+delta)
print("Melhor Tempo: " + str(menor_erro[0]))
print("Erro: " + str(menor_erro[1]))
errros = [abs(e[0]-e[1]) for e in zip(cotas,cs2)]
plt.plot(tempos,cotas,tempos,cs2 )
plt.title("Cota observada X Cota Calculada")
plt.ylabel("cota (h)")
plt.xlabel("data")
plt.show()
