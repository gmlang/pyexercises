def print_attributes(obj):
    for attr in obj.__dict__:
        print attr, getattr(obj, attr)
        
def find_defining_class(obj, meth_name):
    """obj: any object
       meth_name: string
       returns the class that provides the definition of the method
    """
    for ty in type(obj).mro(): #mro stands for method resolution order
        if meth_name in ty.__dict__:
            return ty
        