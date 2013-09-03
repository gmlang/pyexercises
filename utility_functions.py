def print_attributes(obj):
    """prints the attributes of an instance of a class"""
    for attr in obj.__dict__:
        print attr, getattr(obj, attr)
        
def find_defining_class(obj, meth_name):
    """
    obj: any object
    meth_name: string
    returns the class that provides the definition of the method
    """
    for ty in type(obj).mro(): #mro stands for method resolution order
        if meth_name in ty.__dict__:
            return ty

def stdDev(X):
    """
    Assumes that X is a list of numbers.
    Returns the standard deviation of X
    """
    mean = float(sum(X))/len(X)
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    return (tot/len(X))**0.5 
    
def coefVar(X):
    """
    Assumes X is a list of numbers.
    Returns the coefficient of variation of X
    """
    mean = sum(X)/float(len(X))
    try:
        return stdDev(X)/mean
    except ZeroDivisionError:
        return float('NaN')
            
def rSquare(measured, estimated):
    """
    measured: one dimensional array of measured values
    estimate: one dimensional array of predicted values
    """
    EE = ((estimated - measured)**2).sum()
    mMean = measured.sum()/float(len(measured))
    MV = ((mMean - measured)**2).sum()
    return 1 - EE/MV