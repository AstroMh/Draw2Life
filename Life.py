import numpy as np
import tkinter
import pdb
import time
import os
from IPython.display import clear_output
print('good')
width=10
length=10
field=np.full((length,width),False)

def initialize():
    field[0][1]=True
    field[1][2]=True
    field[2][0]=True
    field[2][1]=True
    field[2][2]=True

def show():
    for i in range(10):
        print()
    for i in range(width):
        for j in range(length):
            if field[i][j]:
                print('*',end='')
            else:
                print('-',end='')
        print()

def cn(i,j):
    ans=0
    if field[i][j]:
        ans-=1
    for i1 in range(max(i-1,0),min(i+1,length-1)+1):
        for j1 in range(max(j-1,0),min(j+1,width-1)+1):
            if field[i1][j1]:
                ans+=1
    return ans

def simulate(n):
    global field
    while n>0:
        field2=np.full((length,width),False)
        for i in range(width):
            for j in range(length):
                cnt=cn(i,j)
                if field[i][j]:
                    if cnt==2 or cnt==3:
                        field2[i][j]=True
                    else:
                        field2[i][j]=False
                else:
                    if cnt==3:
                        field2[i][j]=True
                    else:
                        field2[i][j]=False
                
        field=field2
        n-=1
        

initialize()
show()
for i in range(100):
    simulate(1) 
    clear_output()
    show()
    time.sleep(1)
