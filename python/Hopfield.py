from PIL import Image
import numpy as np
import time
import PySimpleGUI as sg

N = 7
w, h, L = 0,0,0

VectorY = []
VectorX = [0] * N

for n in range (N):
    VectorX[n] = []

layout = [
    [sg.Text('Образцы'), sg.InputText(), sg.FolderBrowse()],
    [sg.Text('Тесты     '), sg.InputText(), sg.FolderBrowse()],
    [sg.Button('Запустить'), sg.Button('Закончить')],
    [sg.Output(size=(88, 20))]
]
window = sg.Window('Сеть Хопфильда', layout)

def ReadTest():
    image = Image.open(tests[1]+'/x.bmp')
    pix_mat = image.load()
    global w, h, l, VectorY
    w = image.size[0]
    h = image.size[1]
    L = w*h
    for i in range (w):
        for j in range (h):
            if pix_mat[i,j][0] == 255: 
                VectorY.append(1)
            else:
                VectorY.append(-1)
    print('Тесты считаны')

def Learning():
    global VectorX
    MatrixW = np.zeros((L, L))
    for n in range (N):
        s = str(n)
        pattern = Image.open(tests[0]+'/'+s+'.bmp')
        pix_mat = pattern.load()
        for i in range (w):
            for j in range (h):
                if pix_mat[i,j][0] == 255: #i - столбец, j - строка
                    VectorX[n].append(1)
                else:
                    VectorX[n].append(-1)
                a = i*w+j+1
                for x in range(a):
                    if x != a-1:
                        MatrixW[x][a-1] += VectorX[n][x]*VectorX[n][a-1]
                        MatrixW[a-1][x] += VectorX[n][a-1]*VectorX[n][x]
    return MatrixW
    print('Образцы считаны')

def Classification():
    global VectorY
    start_time = time.time()
    e = 0.001
    Hamming = L
    while (time.time() - start_time) < 10:
        Result = np.zeros((1, L))
        for i in range (L):
            for j in range (L):
                Result[0][i]+=int(MatrixW[i][j]*VectorY[j])
            if Result[0][i] >= 0:
                Result[0][i] = 1
            else:
                Result[0][i] = -1

        d = 0
        for i in range (L):
            d += Result[0][i]*VectorY[i] 
        D = (0.5*(L-d))

        for i in range (L):
            VectorY[i] = Result[0][i]
        
        if Hamming - D <= e:
            break

        Hamming = D



def PrintResult():
    R = []
    for n in range(N):
        c = 0
        for i in range (L):
            if VectorY[i] == VectorX[n][i]:
                c += 1
        R.append(c/L*100)

        print(str(n)+": "+str(R[n]))

while True:                            
    event, tests = window.read()
    if event == 'Закончить':
        break
    if event == 'Запустить':
        ReadTest()
        Learning()
        Classification()
        PrintResult()

#print("--- %s seconds ---" % (time.time() - start_time))
