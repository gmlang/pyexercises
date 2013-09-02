# Problem Set 11: Simulating robots

import math
import random
import pylab
import ps11_visualize
from styleIterator import * 

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real number indicating the y-coordinate
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1 and 2

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.tiles = {}
        for w in xrange(width):
            for h in xrange(height):
                self.tiles[(w, h)] = False # all tiles are dirty initially
        
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        self.tiles[(math.floor(pos.getX()), math.floor(pos.getY()))] = True
        
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned, otherwise returns False

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.tiles[(m, n)]
        
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return len(self.tiles)
        
    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len([tile for tile in self.tiles if self.tiles.get(tile) == True])
        
    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x, y = random.choice(self.tiles.keys())
        return Position(x, y) 
        
    def isPositionInRoom(self, pos):
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """
        return (math.floor(pos.getX()), math.floor(pos.getY())) in self.tiles

class BaseRobot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in
    the room.  The robot also has a fixed speed.

    Subclasses of BaseRobot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified
        room. The robot initially has a random direction d and a
        random position p in the room.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the robot's position.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.p = room.getRandomPosition()
        self.d = random.random() * 360
        
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.p
        
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.d
        
    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.p = position
        
    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.d = direction


class Robot(BaseRobot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        currPos = self.getRobotPosition()
        angle = self.getRobotDirection()
        speed = self.speed
        room = self.room
        room.cleanTileAtPosition(currPos) # clean current position
        newPos = currPos.getNewPosition(angle, speed) # move to a new position
        while not room.isPositionInRoom(newPos): # while the new position is not in room
            angle = random.random() * 360 # pick a random direction
            newPos = currPos.getNewPosition(angle, speed) # move to a new position
        # if the new position is in the room
        self.setRobotDirection(angle) # set the direction as the most recent direction
        self.setRobotPosition(newPos)
        
# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the room that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the room is clean.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE,
    each with speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: a boolean (True to turn on visualization)
    """
    results = []
    for i in xrange(num_trials):
        if visualize == True: 
            anim = ps11_visualize.RobotVisualization(num_robots, width, height, delay=0.5) # start an animation of the room
        room = RectangularRoom(width, height)
        num_tiles = room.getNumTiles()
        pct_cleaned = []
        while True:
            robots = []
            for n in xrange(num_robots):
                bot = robot_type(room, speed)
                robots.append(bot)
            if visualize == True: anim.update(room, robots) # update a new frame of the animation                
            for bot in robots: bot.updatePositionAndClean()    
            pct_cleaned_afterCurTimeStep = room.getNumCleanedTiles() * 1.0 / num_tiles
            if pct_cleaned_afterCurTimeStep < min_coverage:
                pct_cleaned.append(pct_cleaned_afterCurTimeStep)
            else: break
        results.append(pct_cleaned)
    if visualize == True: anim.done()
    return results

def test_Robot():
    num_of_robots = 1; num_of_trials = 30; speed = 3.0    

    temp = runSimulation(num_of_robots, speed, 5, 5, 1.0, 1, Robot, False)
    timeSteps = sum([len(item) for item in temp]) / len(temp)
    print 'One robot takes around', timeSteps, 'clock ticks to completely clean a 5x5 room.'

    temp = runSimulation(num_of_robots, speed, 10, 10, 0.75, num_of_trials, Robot, False)
    timeSteps = sum([len(item) for item in temp]) / len(temp)
    print 'One robot takes around', timeSteps, 'clock ticks to clean 75% of a 10x10 room.'

    temp = runSimulation(num_of_robots, speed, 10, 10, 0.9, num_of_trials, Robot, False)
    timeSteps = sum([len(item) for item in temp]) / len(temp)
    print 'One robot takes around', timeSteps, 'clock ticks to clean 90% of a 10x10 room.'

    temp = runSimulation(num_of_robots, speed, 20, 20, 1.0, num_of_trials, Robot, False)
    timeSteps = sum([len(item) for item in temp]) / len(temp)
    print 'One robot takes around', timeSteps, 'clock ticks to completely clean a 20x20 room.'
    
    
# === Provided function
def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = pylab.array(tots)
    # Compute means
    means = tots/float(len(list_of_lists))
    return means
    
# === Problem 4
def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    xVals, yVals = [], []; 
    num_of_robots = 1; speed = 1.0; min_coverage = 0.75; num_of_trials = 100;     
    for unit in range(5, 30, 5):
        w = h = unit
        temp = runSimulation(num_of_robots, speed, w, h, min_coverage, num_of_trials, Robot, False)
        xVals.append(w*h); yVals.append(sum([len(item) for item in temp]) / float(len(temp)))
    pylab.title('Time to clean 75% of a room with one robot, for various room sizes (' + str(num_of_trials) + 'trials)')
    pylab.xlabel('area of the room')
    pylab.ylabel('time')
    pylab.plot(xVals, yVals, 'bo')
    # pylab.legend('time', loc = 'best', numpoints=1)
    pylab.show()
    
def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    xVals, yVals = [], []; 
    speed = 1.0; min_coverage = 0.75; num_of_trials = 100;     
    for num_of_robots in range(1, 10, 1):
        temp = runSimulation(num_of_robots, speed, 25, 25, min_coverage, num_of_trials, Robot, False)
        xVals.append(num_of_robots); yVals.append(sum([len(item) for item in temp]) / float(len(temp)))
    pylab.title('Time to clean 75% of a 25x25 room with different number of robots (' + str(num_of_trials) + 'trials)')
    pylab.xlabel('num_of_robots')
    pylab.ylabel('time')
    pylab.plot(xVals, yVals, 'bo')
    # pylab.legend('time', loc = 'best', numpoints=1)
    pylab.show()
    

def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    xVals, yVals = [], []; 
    speed = 1.0; min_coverage = 0.75; num_of_trials = 500;     
    for item in [(20,20), (25,16), (40,10), (50,8), (80,5), (100,4)]:
        w, h = item
        temp = runSimulation(2, speed, w, h, min_coverage, num_of_trials, Robot, False)
        xVals.append(w*1.0/h); yVals.append(sum([len(item) for item in temp]) / float(len(temp)))
    pylab.title('Time to clean 75% of a room with two robots,\nfor same room size but different w/h ratios (' + str(num_of_trials) + 'trials)')
    pylab.xlabel('width/height ratio')
    pylab.ylabel('time')
    pylab.plot(xVals, yVals, 'bo')
    # pylab.legend('time', loc = 'best', numpoints=1)
    pylab.show()
    

def showPlot4():
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """
    xVals = [x/10.0 for x in range(1,11,1)] 
    speed = 1.0; num_of_trials = 100;     
    pylab.title('Time to clean various pct of a room with 1-5 robots, \nfor a 25x25 room (' + str(num_of_trials) + 'trials)')
    pylab.xlabel('pct to be cleaned')
    pylab.ylabel('time')
    pylab.semilogy()
    styleChoice = styleIterator(('b+', 'r^', 'go', 'm-', 'y*'))    
    for num_of_robots in range(1, 6, 1):
        yVals = []
        for min_coverage in xVals:
            temp = runSimulation(num_of_robots, speed, 25, 25, min_coverage, num_of_trials, Robot, False)
            yVals.append(sum([len(item) for item in temp]) / float(len(temp)))        
        curStyle = styleChoice.nextStyle()
        pylab.plot(xVals, yVals, curStyle, label='num_of_robots:'+str(num_of_robots))
        pylab.legend(loc = 'best', numpoints=1)
    pylab.show()

    


# === Problem 5

class RandomWalkRobot(BaseRobot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        currPos = self.getRobotPosition()
        speed = self.speed
        room = self.room
        room.cleanTileAtPosition(currPos) # clean current position
        angle = random.random() * 360 # pick a random direction
        newPos = currPos.getNewPosition(angle, speed) # move to a new position
        while not room.isPositionInRoom(newPos): # while the new position is not in room
            angle = random.random() * 360 # pick a random direction
            newPos = currPos.getNewPosition(angle, speed) # move to a new position
        # if the new position is in the room
        self.setRobotDirection(angle) # set the direction as the most recent direction
        self.setRobotPosition(newPos)

def test_RandomWalkRobot():
    num_of_robots = 1; num_of_trials = 30; speed = 3.0    

    temp = runSimulation(num_of_robots, speed, 5, 5, 1.0, 1, RandomWalkRobot, False)
    timeSteps = sum([len(item) for item in temp]) / len(temp)
    print 'One robot takes around', timeSteps, 'clock ticks to completely clean a 5x5 room.'

    temp = runSimulation(num_of_robots, speed, 10, 10, 0.75, num_of_trials, RandomWalkRobot, False)
    timeSteps = sum([len(item) for item in temp]) / len(temp)
    print 'One robot takes around', timeSteps, 'clock ticks to clean 75% of a 10x10 room.'

    temp = runSimulation(num_of_robots, speed, 10, 10, 0.9, num_of_trials, RandomWalkRobot, False)
    timeSteps = sum([len(item) for item in temp]) / len(temp)
    print 'One robot takes around', timeSteps, 'clock ticks to clean 90% of a 10x10 room.'

    temp = runSimulation(num_of_robots, speed, 20, 20, 1.0, num_of_trials, RandomWalkRobot, False)
    timeSteps = sum([len(item) for item in temp]) / len(temp)
    print 'One robot takes around', timeSteps, 'clock ticks to completely clean a 20x20 room.'


# === Problem 6

def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    The plot shows the two kinds of robots took about the same time.
    """
    xVals, Robot_yVals, RandomWalkRobot_yVals = [], [], []; 
    num_of_robots = 10; speed = 1.0; min_coverage = 1; num_of_trials = 100;     
    for unit in range(5, 60, 5):
        w = h = unit
        temp = runSimulation(num_of_robots, speed, w, h, min_coverage, num_of_trials, Robot, False)
        xVals.append(w*h); Robot_yVals.append(sum([len(item) for item in temp]) / float(len(temp)))
        temp = runSimulation(num_of_robots, speed, w, h, min_coverage, num_of_trials, RandomWalkRobot, False)
        RandomWalkRobot_yVals.append(sum([len(item) for item in temp]) / float(len(temp)))
    pylab.title('Time to clean a room completely with one robot, for various room sizes (' + str(num_of_trials) + 'trials)')
    pylab.xlabel('area of the room')
    pylab.ylabel('time')
    pylab.plot(xVals, Robot_yVals, 'bo', label='Robot')
    pylab.plot(xVals, RandomWalkRobot_yVals, 'ro', label='RandomWalkRobot')
    pylab.legend(loc = 'best', numpoints=1)
    pylab.show()


    
if __name__ == '__main__':
    # test_runSimulation()
    # showPlot1()
    # showPlot2()
    # showPlot3()
    # showPlot4()
    # test_Robot()
    # test_RandomWalkRobot()
    showPlot5()