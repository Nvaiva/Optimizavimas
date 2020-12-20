import numpy as np
from sympy import *
from sympy import symbols
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
from collections import OrderedDict
import operator
import csv
import interval as inte
def createVolumeFunction():
    x, y, z = symbols('x y z')
    expr = -(x*y*z)/8
    func = sympify(expr)
    return func

def rectangularSurfaceArea():
    x, y, z = symbols('x y z')
    eq = Eq(x+ y + z, 1)
    return eq

def writeToCsv(row, fileName):
    with open(fileName, mode='w') as data1:
        data1_writer = csv.writer(data1, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data1_writer.writerow(["x","y","z","tiksloFunkcija"])
        for r in row:
            data1_writer.writerow(r)

def diffX (func): return diff(func, Symbol('x'))

def diffY (func): return diff(func, Symbol('y'))

def diffZ (func): return diff(func, Symbol('z'))

def solveFunc(func, X): return N(func.subs({Symbol('x'):X[0], Symbol('y'): X[1], Symbol('z'): X[2]}))

def plotFunc3D(func):

    p4 = plot3d(func,(Symbol('x'), 0, 1), (Symbol('y'), 0, 1))
    p4 = plot3d((0,1))

def distanceBeetweenVectors(p1, p2): return math.sqrt(((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2))

def gradientDescentMethod (func, startingPoint, alpha = 0.1,r = 0.1, accuracy = 0.01, printDiff = False, printPoints = False):
    print(startingPoint, "R", r)
    writerToCsv = []
    descendMore = true
    functionsCounter = 0
    stepsCounter = 0
    maxI = 100
    while (maxI > 0):
        stepsCounter = stepsCounter + 1
        # Gradient
        solvedDiffX = solveFunc(diffX(func), startingPoint)
        print(solvedDiffX, maxI)
        solvedDiffY = solveFunc(diffY(func), startingPoint)
        solvedDiffZ = solveFunc(diffZ(func), startingPoint)
        functionsCounter = functionsCounter + 2
            
        # New values 
        X0 = startingPoint[0] - alpha * solvedDiffX
        X1 = startingPoint[1] - alpha * solvedDiffY
        X2 = startingPoint[2] - alpha * solvedDiffZ
        
        # Wanted accuracy has been reached. No need to continue calculations
        if (distanceBeetweenVectors(startingPoint, (X0,X1,X2)) <= accuracy): descendMore = false  
            
        if printPoints and printDiff: print(startingPoint, solvedDiffX, solvedDiffY)
        elif printPoints: print(startingPoint)
        elif printDiff: print(solvedDiffX, solvedDiffY)
            
        startingPoint = (X0,X1,X2)
        writerToCsv.append([X0, X1, solveFunc(func, startingPoint)])
        maxI = maxI - 1
        
    writeToCsv(writerToCsv, "GradientDescent.csv")  
    print("Functions counter - ", functionsCounter)
    print("Steps - ", stepsCounter)
    result = solveFunc(func, startingPoint)
    return startingPoint, result

def fastestGradientDescentMethod(func, startingPoint, accuracy = 0.0001, printDiff = False, printPoints = False):
    
    writerToCsv = []
    # New symbol a = alpha 
    a = symbols('a')
    functionsCounter = 0
    functionsGoldenCut = 0
    stepsCounter = 0
    stepsGoldenCut = 0
    
    descendMore = true
    while (descendMore):
        stepsCounter = stepsCounter + 1
        
        # Gradient
        solvedDiffX = solveFunc(diffX(func), startingPoint)
        solvedDiffY = solveFunc(diffY(func), startingPoint)
        functionsCounter = functionsCounter + 2

        # New values with alpha 
        X0 = startingPoint[0] - a * solvedDiffX
        X1 = startingPoint[1] - a * solvedDiffY

        # Put X0 and X1 accordingly to goal function
        newFunc = func.subs({Symbol('x'):X0, Symbol('y'): X1})

        # Put given values to x and y variables
        result = newFunc.subs({Symbol('x'):startingPoint[0], Symbol('y'): startingPoint[1]})

        result = result.subs({Symbol('a'):Symbol('x')})
        # Express alpha and we add steps and functions number which was calculated in golden cut method
        functions = 0
        steps = 0
        alpha, functions, steps = inte.goldenCut(result, 0,3)
        
        functionsGoldenCut = functionsGoldenCut + functions
        stepsGoldenCut = stepsGoldenCut + steps
        # Calculate values with new alpha
        for i in alpha:
            X0 = startingPoint[0] -  i * solvedDiffX
            X1 = startingPoint[1] -  i * solvedDiffY
            break
        
        # Wanted accuracy has been reached. No need to continue calculations
        if (distanceBeetweenVectors(startingPoint, (X0,X1)) <= accuracy): descendMore = false 
            
        if printDiff and printPoints: print(startingPoint, solvedDiffX, solvedDiffY)
        elif printDiff: print(solvedDiffX, solvedDiffY)
        elif printPoints: print(startingPoint)    
        
        startingPoint = (X0,X1)
        writerToCsv.append([X0, X1, solveFunc(func, startingPoint)])
    
    writeToCsv(writerToCsv, "FastestGradientDescentXm.csv")
    print("Functions - ", functionsCounter)
    print("Steps - ", stepsCounter)
    print("Functions g - ", functionsGoldenCut)
    print("Steps g- ", stepsGoldenCut)
    return startingPoint, solveFunc(func, startingPoint)
    
def getDelta1 (n, alpha): return ((math.sqrt(n + 1) + n - 1)/(n*math.sqrt(2)))*alpha

def getDelta2 (n, alpha): return ((math.sqrt(n + 1) - 1)/(n*math.sqrt(2)))*alpha
        
def getTriangeVertexes (X0, alpha):
    
    vertexes = []
    # Triange vertexes
    vertexes.append(X0)
    vertexes.append((X0[0] + getDelta2(len(X0), alpha), X0[1] + getDelta1(len(X0), alpha), X0[2] + getDelta1(len(X0), alpha)))
    vertexes.append((X0[0] + getDelta1(len(X0), alpha), X0[1] + getDelta2(len(X0), alpha), X0[2] + getDelta1(len(X0), alpha)))
    vertexes.append((X0[0] + getDelta1(len(X0), alpha), X0[1] + getDelta1(len(X0), alpha), X0[2] + getDelta2(len(X0), alpha)))
    return vertexes

def getVertexValues (func, vertexes):
    
    fVertexes = []
    
    for vertex in vertexes:
        fVertexes.append(solveFunc(func, vertex))
        
    return fVertexes

def getWeightCenter (vertexes):
    
    vectorSum = (0,0,0)
    
    for x, y, z in list(vertexes.keys())[:-1]:
        vectorSum = (vectorSum[0] + x , vectorSum[1] + y, vectorSum[2] + z)
        
    weightCenter = (1/3 * vectorSum[0], 1/3 * vectorSum[1], 1/3 * vectorSum[2])

    return weightCenter

def getNewVertex (weightCenter, maxX, teta):
   
    a = (weightCenter[0] - maxX[0], weightCenter[1] - maxX[1], weightCenter[2] - maxX[2])
    b = ((1 + teta) * a[0], ((1 + teta) * a[1]), ((1 + teta) * a[2]))
    newVertex = (maxX[0] + b[0], maxX[1] + b[1], maxX[2] + b[2])
    
    return newVertex
        
def getVerticesWithFunctionValues(func, X0, alpha):
    fVertexes = []
    vertexes = []
    verteces = {}
    
    # Triange vertexes
    vertexes = getTriangeVertexes(X0, alpha)
    
    # get Function values 
    fVertexes = getVertexValues(func, vertexes)
    for i in range (len(vertexes)):
        verteces[vertexes[i]] =  fVertexes[i]
    return dict(sorted(verteces.items(), key=operator.itemgetter(1)))

def isAccurate(vertices, accuracy):
    values = []
    for x in vertices.values():
        values.append(x)
    
    if (abs(values[0] - values[1]) <= accuracy):
        if (abs(values[0] - values[2]) <= accuracy):
            if (abs(values[0] - values[3]) <= accuracy): 
                if (abs(values[1] - values[2]) <= accuracy): 
                     if (abs(values[1] - values[3]) <= accuracy): 
                        if (abs(values[2] - values[3]) <= accuracy): 
                             return True
    return False
    
def simplexMethod (func, X0, alpha = 0.5 , teta = 1, gamma = 2, beta = 0.5, eta = -0.5, accuracy = 0.0000000001, printX = false, printDict = false):
    
    """
    func - goal function
    alpha - simplex edge length
    teta - the length of the simplex line passing through the weight center
    gamma - (gamma > 1) simplex expansion factor
    beta - (0 < beta < 1) simplex compression factor
    eta - (−1 < eta < 0) simplex compression factor
    printX - print new coordinates and values of the triangle
    printDict - print coordinates of all vertices and their values
    """
    writerToCsv = []
    verteces = getVerticesWithFunctionValues(func, X0, alpha)
    maximum = 300 # max number of iterations
    stepsCounter = 0 
    functionsCounter = 0
    
    for i in range(maximum):
      
        stepsCounter = stepsCounter + 1
        
        weightCenter = getWeightCenter(verteces)
        newVertec = getNewVertex(weightCenter, (list(verteces.keys())[-1]), teta)
        newFVertec = solveFunc(func, newVertec)
        functionsCounter = functionsCounter + 1
      
        smallest = list(verteces.values())[0]
        middle = list(verteces.values())[2]
        greatest = list(verteces.values())[3]

        # Compression
        if (newVertec[0] <= 0 or newVertec[1] <= 0 or newVertec[2] <= 0):
            newVertec = getNewVertex(weightCenter, (list(verteces.keys())[-1]), eta)
            newFVertec = solveFunc(func, newVertec) 
            functionsCounter = functionsCounter + 1
            
        # Nothing changes
        if (smallest < newFVertec and newFVertec < middle):
            teta = 1   
    
        # Expansion
        elif (smallest > newFVertec):
            
            newVertec1 = getNewVertex(weightCenter, (list(verteces.keys())[-1]), gamma)
            newFVertec1 = solveFunc(func, newVertec1) 
            functionsCounter = functionsCounter + 1
            if (newFVertec1 < newFVertec):
                newVertec = newVertec1
                newFVertec = newFVertec1
                functionsCounter = functionsCounter + 1
            
        # Compression
        elif (newFVertec > greatest) :
        
            newVertec = getNewVertex(weightCenter, (list(verteces.keys())[-1]), eta)
            newFVertec = solveFunc(func, newVertec)
            functionsCounter = functionsCounter + 1
        
        # Compression
        elif (middle < newFVertec and newFVertec < greatest):
            
            newVertec = getNewVertex(weightCenter, (list(verteces.keys())[-1]), beta)
            newFVertec = solveFunc(func, newVertec)
            functionsCounter = functionsCounter + 1
            
        # Verteces dictionary is sorted by function values. Delete last value because it hodls biggest function value
        verteces.popitem()
        
        # Add new item to the vertices dictionary
        verteces[newVertec] = newFVertec
        
        # Sorting new vector
        verteces = dict(sorted(verteces.items(), key=operator.itemgetter(1)))
        for key, value in verteces.items():
            writerToCsv.append([key[0],key[1], key[2], value])
        
        if printX: print("New vertex - ", newVertec, "vertex value - ", newFVertec)
        if printDict: print(verteces)
        
        if (isAccurate(verteces, accuracy)):
            writeToCsv(writerToCsv, "SimplexX0.csv")
           # print("Functions - ", functionsCounter)
           # print("Steps - ", stepsCounter)
            return newVertec,newFVertec
        
    print("Functions - ", functionsCounter)
    print("Steps - ", stepsCounter)
    writeToCsv(writerToCsv, "SimplexX0.csv")
    return newVertec, newFVertec