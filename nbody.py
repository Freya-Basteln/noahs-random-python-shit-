import numpy as np
import random


def treed(tree,indices):
    LIST=tree
    for i in range(len(indices)):
        LIST=LIST[indices[i]]
    return LIST

def treewrite(tree,indices,leaf):
    LIST=leaf
    RANGE=len(indices)
    for i in range(RANGE):
        place=indices.pop(-1)
        LIST1=treed(tree,indices)
        LIST1[place]=LIST
        LIST=LIST1
    tree=LIST    


def find(points,indices):
    center=np.array([0,0])
    squarevector=[np.array([1,1]),np.array([-1,1]),np.array([-1,-1]),np.array([1,-1])]
    for i in range(len(indices)):
        center+=squarevector[indices[-i-1]]
        center=np.multiply(center,.5)
    center=np.multiply(center,.5)
    center+=np.multiply(squarevector[0],.5)
    POINTS=[]
    for i in range(len(points)):
        distance=center-np.array(points[i][0])
        if abs(distance[0])<0.5**(len(indices)+1) and  abs(distance[1])<0.5**(len(indices)+1): 
            POINTS.append(points[i])
    return POINTS

import matplotlib.pyplot as plt
def squarecoords(x,y,s):
    return[[x+s,x-s,x-s,x+s,x+s],[y+s,y+s,y-s,y-s,y+s]]
def plotsquare(x,y,s):
    p=squarecoords(x,y,s)
    x=p[0]
    y=p[1]
    plt.plot(x,y,linewidth=1,marker='',markersize=1)
def square(indices):
    center=np.array([0,0])
    squarevector=[np.array([1,1]),np.array([-1,1]),np.array([-1,-1]),np.array([1,-1])]
    for i in range(len(indices)):
        center+=squarevector[indices[-i-1]]
        center=np.multiply(center,.5)
    center=np.multiply(center,.5)
    center+=np.multiply(squarevector[0],.5)
    plotsquare(center[0],center[1],0.5**(len(indices)+1))
def plotpoint(x,y):
    plt.plot(x,y,linewidth=3,marker='o',markersize=3)

allpoints=[]
for i in range(10):
    allpoints.append([[random.random(),random.random()],random.random(),i])
Points=[]
def addpoints(indices):
    s=square(indices)
    return find(allpoints,indices)
Points+=addpoints([])

#print(allpoints)
indices=np.empty(len(allpoints))
maxpoints=1
def divide(points,indices):
    points=find(points,indices)
    avgp=np.array([0.0,0.0])
    for p in points:
        #print(np.multiply(p[0],p[1]))
        avgp+=np.multiply(p[0],p[1])
    totalmass=sum([p[1] for p in points])
    if totalmass != 0:
        avgp=np.multiply(avgp,1/totalmass)
    if len(points)>maxpoints:
        square(indices)
        branches=[divide(points,indices+[index]) for index in range(4)]
        branches+= [[avgp,totalmass]]
        return branches
    else:
        print(points,indices,len(points),len(places))
        if len(points)>0:
            places[points[0][2]]=indices
        square(indices)
        return points+[[avgp,totalmass]]

G=.001
def gravity(tree,indices,Indices):
    #print("I",treed(tree,Indices),"i",treed(tree,indices))
    M=np.array(treed(tree,Indices)[-1])
    m=np.array(treed(tree,indices)[-1])
    dist=np.array([m[0][i]-M[0][i] for i in range(len(M[0]))])
   # print(dist)
    r2=sum(i**2 for i in dist)
    r3=r2**3/2
   # print(r3)
    return G*M[1]*m[1]*dist/r3
v=np.zeros(2*len(allpoints)).reshape(len(allpoints),2)
a=np.zeros(2*len(allpoints)).reshape(len(allpoints),2)

dt=0.01

#
while True:
    places=[[]for i in range(len(allpoints))]
    #print(places)
    tree=(divide(allpoints,[]))
    #print(places)
    #print(tree)
    #print(allpoints[1])
    #print(treed(tree,places[1]))
    for I in range(len(places)):
        indices=places[I]
        #print(indices)
        for n in indices:
            me=indices.pop()
            a[I]+=np.array(sum(list(np.array(gravity(tree,indices+[i],places[I])) for i in range(4) if i != me)))
            v[I]+=dt*a[I]
        #print("a",a)
        #print("v",v)
           # print(tree)
    for I in range(len(places)):
        print("e",np.array(treed(tree,places[I])))
        treewrite(tree,places[I],np.array(treed(tree,places[I])[-1][0])+dt*v[I])
        print()
    for points in allpoints:
        plotpoint(points[0][0],points[0][1])
    #plt.show()


