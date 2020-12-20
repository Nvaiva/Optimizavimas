from sympy import *
import laboratorinis_2 as op

def createFunctionF():
    x, y, z = symbols('x y z')
    expr = -x*y*z
    func = sympify(expr)
    return func

def createFunctionG():
    x, y, z = symbols('x y z')
    eq = (2*x*y+ 2*x*z + 2*y*z) - 1
    return eq

def createFunctionH():
    x = symbols('x')
    expr = -x
    return expr

def powMaxHSum():
    x, y, z = symbols('x y z')
    expr = Pow(Max(0, -x), 2) + Pow(Max(0, -y), 2) + Pow(Max(0, -z), 2)
    return expr
    

def createGoalFunction(r = 2):
    expr = createFunctionF() + (powMaxHSum() + Pow(createFunctionG(),2))*1/r
    return expr
    
def getAnswer(startingPoint,accuracy = 0.00001, r = 10):
    
    rd = r
    f = startingPoint
    newf =  op.simplexMethod(createGoalFunction(rd), f)
    
    while (True):
        rd = rd/10
        f = newf[0]
        newf =  op.simplexMethod(createGoalFunction(rd), f)
        if (op.distanceBeetweenVectors(newf[0], f) < accuracy):return f
        
    return f

        