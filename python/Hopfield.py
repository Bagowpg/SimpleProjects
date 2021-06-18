from PIL import Image
import numpy as np

import time
start_time = time.time()

image = Image.open('3.bmp')
pix_mat = image.load()

w = image.size[0]
h = image.size[1]
L = w*h

N = 10
VectorX = [0] * N
VectorY = [0] * N

D = []
#Mat_num = [0] * N

Sum_Mat = np.zeros((L, L))

for n in range (N):
    
    Vector[n] = []

    s = str(n)
    pattern = Image.open(s+'.bmp')

    pix_mat = pattern.load()
    #Mat_num[n] = np.zeros((L, L))

    for i in range (w):
        for j in range (h):
            if pix_mat[i,j][0] == 255: #i - столбец, j - строка
                VectorX[n].append(1)
            else:
                VectorX[n].append(-1)
            a=i*w+j+1
            for x in range(a):
                if x != a-1:
                #Mat_num[n][x][i*w+j]=Vector[n][x]*Vector[n][i*w+j]
                    Sum_Mat[x][a-1] += VectorX[n][x]*VectorX[n][a-1]
                    Sum_Mat[a-1][x] += VectorX[n][a-1]*VectorX[n][x]
                    #Check[a-1][0]+=int(Sum_Mat[x][a-1]*Vector[n][a-1])

while (time.time() - start_time) < 30:
    for n in range(N):

        Check = np.zeros((L, 1))
        #d = 0

        for i in range (L):
            for j in range (L):
                Check[i][0]+=int(Sum_Mat[i][j]*Vector[n][j])
            if Check[i][0] >= 0:
                Check[i][0] = 1
            else:
                Check[i][0] = -1
        #d += Check[i][0]*Vector[n][i]

    #D.append(0.5*(L-d))

    #print(D[n])

    #for i in range (L):
        #for j in range (L):
            #Check[i][0]+=int(Sum_Mat[i][j]*Vector[0][j])

    
    с = 0
    for i in range (L):
        if Check[i][0] == Vector[n][i]:
            с+= 1
    print(str(n)+': '+str(с/L*100)+'%')
    
print("--- %s seconds ---" % (time.time() - start_time))

    #for i in range (L):
        #for j in range (L):
            #Mat_num[n][i][j]=Vector[n][i]*Vector[n][j]

'''
Sum_Mat = np.zeros((L, L))

for n in range (N):
    for i in range (L):
        for j in range (L):
            if i != j:
                Sum_Mat[i][j]+=Mat_num[n][i][j]
'''
'''
Num = int(0)
#image = Image.open(Check+'.bmp')


for i in range (L):
    for j in range (L):
        Check[i][0]+=int(Sum_Mat[i][j]*Vector[Num][j])
'''
'''
fout=open('Matrix.txt','w')
for i in range (625):
    fout.write(str(Vector[3][i]))
    fout.write(' ')
    if (i+1) % 25 == 0:
        fout.write('\n')

fout2=open('Matrix2.txt','w')
for i in range (625):
    fout2.write(str(Check[i][0]))
    fout2.write(' ')
    if (i+1) % 25 == 0:
        fout2.write('\n')
'''