import pylab

def makePlot(xVals, yVals, title, xLabel, yLabel, style, 
             newFig = False, logX = False, logY = False):
    """Plots xVals vs. yVals with supplied titles and labels."""
    if newFig:
        pylab.figure()
    pylab.title(title)
    pylab.xlabel(xLabel)
    pylab.ylabel(yLabel)
    ## add text
    xmin, xmax = pylab.xlim() # returns a tuple of the minimal and maximal
                              # vals of the x-axis of the current figure
    ymin, ymax = pylab.ylim()
    pylab.text(xmin + (xmax-xmin)*0.02, (ymax-ymin)/2, 
               'Mean = ' + str(0) + '\nSD = ' + str(1))
    ## if use log scaled axises
    if logX:
        pylab.semilogx()
    if logY:
        pylab.semilogy()        
    pylab.plot(xVals, yVals, style)
    pylab.legend(loc = 'lower left', numpoints = 1) # legend    