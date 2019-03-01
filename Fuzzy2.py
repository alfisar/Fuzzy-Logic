import numpy
import csv
import matplotlib.pyplot as graph

def checkPendapatan(x):
    pLow, pMedium, pHigh = 0,0,0

    if x >= 0 and x <= 0.3340375:
        pLow    = 1

    elif x > 0.3340375 and x < 0.556075:
        pLow    = (-1*((x-0.556075)/(0.556075-0.2780375)))
        pMedium = ((x-0.3340375)/(0.556075-0.3340375))

    elif x >= 0.556075 and x <= 1.11215:
        pMedium = 1

    elif x > 1.11215 and x <1.3091125:
        pMedium = (-1*((x-1.3091125)/(1.3091125-1.11215)))
        pHigh   = ((x-1.11215)/(1.3091125-1.11215))

    elif x >= 1.3091125:
        pHigh   = 1

    return pLow, pMedium, pHigh


def checkHutang(x):
    hLow, hMedium, hHigh = 0,0,0

    if x >= 0 and x <= 16.7797575:
        hLow    = 1

    elif x > 16.7797575 and x < 21.557515:
        hLow    = (-1*(x-21.557515)/(21.557515-16.7797575))
        hMedium = ((x-16.7797575)/(21.557515-16.7797575))

    elif x >= 21.557515 and x <= 49.11903 :
        hMedium = 1

    elif x > 49.11903 and x < 56.8392725:
        hMedium = (-1*(x-56.8392725)/(56.8392725-49.11903))
        hHigh   = ((x-49.11903)/(56.8392725-49.11903))

    elif x >= 56.8392725:
        hHigh   = 1

    return hLow, hMedium, hHigh

def inference(pLow, pMedium, pHigh, hLow, hMedium, hHigh):
    Y1,Y2,Y3= 0,0,0
    N1,N2,N3,N4,N5,N6 = 0,0,0,0,0,0
    Y,N = 0,0

    if pHigh != 0 and hHigh != 0:
        N1 = min(pHigh,hHigh)

    if pHigh != 0 and hMedium != 0:
        N2 = min(pHigh,hMedium)

    if pHigh != 0 and hLow != 0:
        N3 = min(pHigh,hLow)

    if pMedium != 0 and hHigh !=0:
        Y1 = min(pMedium,hHigh)

    if pMedium != 0 and hMedium != 0:
        N4 = min(pMedium,hMedium)

    if pMedium != 0 and hLow != 0:
        N5 = min(pMedium,hLow)

    if pLow != 0 and hHigh != 0:
        Y2 = min(pLow,hHigh)

    if pLow != 0 and hMedium != 0:
        Y3 = min(pLow,hMedium)

    if pLow != 0 and hLow != 0:
        N6 = min(pLow,hLow)

    Y = max(Y1,Y2,Y3)
    N = max(N1,N2,N3,N4,N5,N6)
    return Y,N


def defuzzification(Y,N):
    if Y != 0 and N != 0:
        return ((Y*60)+(N*40))/(Y+N)
    elif Y != 0:
        return (Y*60)/Y
    elif N != 0:
        return (N*40)/N

def takeSecond1(elem):
    return elem[3]

def takeSecond2(elem):
    return elem[0]

# membaca dan menulis file csv
f = open("DataTugas2.csv","r")
reader = csv.reader(f)
next(reader)
g = open("TebakanTugas2.csv","w")
w = csv.writer(g)
w.writerow(("No","No Yang Dapat BLT"))

# pendeklarasian variable
i = 1
j = 0
lis1 = []
lis2 = []
sx=[]
sy=[]
si=[]

# melakukan perhitungan fuzzi logic
for d in reader :
    pLow,pMedium,pHigh = checkPendapatan(float(d[1]))
    hLow,hMedium,hHigh = checkHutang(float(d[2]))
    Ya,Tidak = inference(pLow,pMedium,pHigh,hLow,hMedium,hHigh)
    hasil = defuzzification(Ya,Tidak)
    if hasil > 40 :
        lis1.append((d[0],d[1],d[2],hasil))

# mengurutkan dan membalik data yang keterima menurut score yang di dapatkan 
lis1.sort(key=takeSecond1)
lis1.reverse()

#memfilter 20 data yang mendapatkan BLT dari nilai score yang tertinggi
for row in lis1 :
    if j < 20 :
        lis2.append((int(row[0])))
        sx.append(float(row[1]))
        sy.append(float(row[2]))
        si.append(row[0])
        j += 1

# mengurutkan data berdasarkan nonya
lis2.sort()
print("No","No Yang Dapat BLT")
# menampilkan final data yang berhasil menerima BLT
for row in lis2 :
    print(i,row)
    w.writerow((i,str(row)))
    i+=1
f.close()
g.close()

# menampilkan scatter graph 
# sx=numpy.asarray(sx)
# sy=numpy.asarray(sy)
# graph.scatter(sx,sy)
# graph.xlim([0,2])
# graph.ylim([0,100])
# graph.xlabel("Pendapatan")
# graph.ylabel("Hutang")
# for i in range(len(si)):
#     graph.annotate(si[i],(sx[i],sy[i]))
# graph.show()
