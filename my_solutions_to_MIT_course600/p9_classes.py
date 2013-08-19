# 6.00 Problem Set 9
#

from string import *

class Shape(object):
    def area(self):
        raise AttributeException("Subclasses should override this method.")

class Square(Shape):
    def __init__(self, h):
        """
        h: length of side of the square
        """
        self.side = float(h)
    def area(self):
        """
        Returns area of the square
        """
        return self.side**2
    def __str__(self):
        return 'Square with side ' + str(self.side)
    def __eq__(self, other):
        """
        Two squares are equal if they have the same dimension.
        other: object to check for equality
        """
        return type(other) == Square and self.side == other.side

class Circle(Shape):
    def __init__(self, radius):
        """
        radius: radius of the circle
        """
        self.radius = float(radius)
    def area(self):
        """
        Returns approximate area of the circle
        """
        return 3.14159*(self.radius**2)
    def __str__(self):
        return 'Circle with radius ' + str(self.radius)
    def __eq__(self, other):
        """
        Two circles are equal if they have the same radius.
        other: object to check for equality
        """
        return type(other) == Circle and self.radius == other.radius

#
# Problem 1: Create the Triangle class
#
## TO DO: Implement the `Triangle` class, which also extends `Shape`.
class Triangle(Shape):
    def __init__(self, base, height):
        self.base = float(base)
        self.height = float(height)
    def area(self):
        """returns the area of the triangle"""
        return self.base * self.height / 2 
    def __str__(self):
        return 'Triangle with base ' + str(self.base) + ' and height ' + str(self.height)
    def __eq__(self, other):
        """Two triangles are equal if they have the same base and height.
        Other: object to check for equality"""
        return type(other) == Triangle and self.base == other.base and self.height == other.height

def test_Triangle():
    t1 = Triangle(3, 4)
    # t2 = Triangle(3, 4)
    t2 = Triangle(5, 6)
    print t1.area()
    print t2
    print t1 == t2
#   
# Problem 2: Create the ShapeSet class
#
## TO DO: Fill in the following code skeleton according to the
##    specifications.

class ShapeSet(object):
    def __init__(self):
        """
        Initialize any needed variables
        """
        self.members = []
        self.place = None
        
    def addShape(self, sh):
        """
        Add shape sh to the set; no two shapes in the set may be equal
        sh: shape to be added
        """
        if sh not in self.members: self.members.append(sh)
        
    def __iter__(self):
        """
        Return an iterator that allows you to iterate over the set of
        shapes, one shape at a time
        """
        self.place = 0
        return self
        
    def next(self):
        if self.place >= len(self.members):
            raise StopIteration
        self.place += 1
        return self.members[self.place-1]
        
    def __str__(self):
        """
        Return the string representation for a set, which consists of
        the string representation of each shape, categorized by type
        (circles, then squares, then triangles)
        """
        circles, squares, triangles = [], [], []
        for shape in self.members:
            if type(shape) == Circle:
                circles.append(shape)
            if type(shape) == Square:
                squares.append(shape)
            if type(shape) == Triangle:    
                triangles.append(shape)
        for circle in circles:
            print circle
        for square in squares:
            print square
        for triangle in triangles:
            print triangle
        return ''
        
def test_ShapeSet():
    set = ShapeSet()
    t1 = Triangle(2,3)
    t2 = Triangle(2,3)
    set.addShape(t2)
    set.addShape(t1)
    c1 = Circle(1)
    c2 = Circle(2.4)
    set.addShape(c1)
    set.addShape(c2)
    s1 = Square(4)
    s2 = Square(3)
    set.addShape(s1)
    set.addShape(s2)
    print set
    
#
# Problem 3: Find the largest shapes in a ShapeSet
#
def findLargest(shapes):
    """
    Returns a tuple containing the elements of ShapeSet with the
       largest area.
    shapes: ShapeSet
    """
    maxArea = max([shape.area() for shape in shapes])
    largest = [shape for shape in shapes if shape.area() == maxArea]
    return tuple(largest)

def test_findLargest():
    ss = ShapeSet()
    ss.addShape(Triangle(1.2, 2.5))
    ss.addShape(Circle(4))
    ss.addShape(Square(3.6))
    ss.addShape(Triangle(1.6, 6.4))
    ss.addShape(Circle(2.2))
    largest = findLargest(ss)
    print largest
    for e in largest: print e

    ss = ShapeSet()
    ss.addShape(Triangle(3, 8))
    ss.addShape(Circle(1))
    ss.addShape(Triangle(4, 6))
    largest = findLargest(ss)
    print largest
    for e in largest: print e

    t = Triangle(6, 6)
    c = Circle(1)
    ss = ShapeSet()
    ss.addShape(t)
    ss.addShape(c)
    largest = findLargest(ss)
    print largest[0] is t
    print largest[0] is c
    
    
#
# Problem 4: Read shapes from a file into a ShapeSet
#
def readShapesFromFile(filename):
    """
    Retrieves shape information from the given file.
    Creates and returns a ShapeSet with the shapes found.
    filename: string
    """
    ss = ShapeSet()
    with open(filename) as f:
        for line in f:
            if line.count(',') == 1:
                type, arg = line.strip().split(',')
                if type == 'circle':
                    ss.addShape(Circle(float(arg)))
                if type == 'square':
                    ss.addShape(Square(float(arg)))
            if line.count(',') == 2:
                type, base, height = line.strip().split(',')
                if type == 'triangle':
                    ss.addShape(Triangle(float(base), float(height)))
    return ss
    
if __name__ == '__main__':
    # test_Triangle()
    # test_ShapeSet()
    # test_findLargest()
    ss = readShapesFromFile("shapes.txt")
    print ss