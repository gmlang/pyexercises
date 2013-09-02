# 6.00 Problem Set 12
#

import numpy
import random
import pylab

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """    

#
# PROBLEM 1
#

class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        
    def doesClear(self):
        """
        Stochastically determines whether this virus is cleared from the
        patient's body at a time step. 

        returns: Using a random number generator (random.random()), this method
        returns True with probability self.clearProb and otherwise returns
        False.
        """
        return random.random() < self.clearProb
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if random.random() < self.maxBirthProb * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException("NoChildException")
            
class SimplePatient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """
    
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getTotalPop(self):
        """
        Gets the current total virus population. 

        returns: The total virus population (an integer)
        """
        return len(self.viruses)        

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
          of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update() 

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: the total virus population at the end of the update (an
        integer)
        """
        for virus in self.viruses[:]:
            if virus.doesClear():
                self.viruses.remove(virus)
        if self.getTotalPop() < self.maxPop:                
            popDensity = self.getTotalPop() * 1.0 / self.maxPop
            # print popDensity
            for virus in self.viruses[:]:
                try:
                    self.viruses.append(virus.reproduce(popDensity))
                except NoChildException:
                    # print "Good! This virus can't reproduce a child!"
                    pass
        return self.getTotalPop()
 
#
# PROBLEM 2
#

def problem2():
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    

    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    maxBirthProb = 0.1; clearProb = 0.05
    viruses = [SimpleVirus(maxBirthProb, clearProb) for i in range(100)]
    patient = SimplePatient(viruses, 1000)
    xVals = range(301); yVals = [patient.getTotalPop()]
    for i in xVals[:-1]:
        yVals.append(patient.update())
    print yVals    
    pylab.plot(xVals, yVals, 'bo', label='virus population')
    pylab.axvline(x=125,color='k',ls='dashed') # add a vertical black dashed line at x=120
    pylab.axhline(y=500,color='k',ls='dashed') # add a horizontal black dashed line at y=500
    pylab.title('virus population over time')
    pylab.xlabel('time steps')
    pylab.ylabel('virus population')
    pylab.legend(loc='best', numpoints=1)
    # pylab.show() # the plot shows an increasing trend that levels off and flactuate around virus population of 500 
#
# PROBLEM 3
#

class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """    
    
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.
        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        
        clearProb: Maximum clearance probability (a float between 0-1).
        
        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb
        
    def getResistance(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.        

        drug: the drug (a string).

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.resistances[drug]
        
    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        ## v1, logic is wrong
        # if activeDrugs == []: reproduce = True
        # else: 
            # reproduce = False
            # for drug in activeDrugs:
                # if self.getResistance(drug):
                    # reproduce = True
                    # break
        ## v2, logic is correct: a virus always reproduces unless there's at least one drug such that self.getResistance(drug)==False
        reproduce = True
        for drug in activeDrugs:
            if not self.getResistance(drug):
                reproduce = False
                break
        
        if reproduce and random.random() < self.maxBirthProb * (1 - popDensity):
            # print '!reproduce!' # comment off when running test_Patient()
            ## v1, assuming drug resistance mutations are completely dependent (with correlation = 1)
            # offspring_resistances = {}
            # if random.random() < self.mutProb:
                # for drug in self.resistances:
                    # # print 'parent resistant: ', self.resistances[drug] # comment off when running test_Patient()
                    # offspring_resistances[drug] = not self.resistances[drug] 
                    # # print 'children resistant: ', offspring_resistances[drug] # comment off when running test_Patient()
            # else: offspring_resistances = self.resistances
            ## v2, assuming drug resistance mutations are independent
            offspring_resistances = {}
            for drug in self.resistances:
                if random.random() < self.mutProb:
                    # print 'parent resistant: ', self.resistances[drug] # comment off when running test_Patient()
                    offspring_resistances[drug] = not self.resistances[drug] 
                    # print 'children resistant: ', offspring_resistances[drug] # comment off when running test_Patient()
                else: offspring_resistances[drug] = self.resistances[drug]            
                
            return ResistantVirus(self.maxBirthProb, self.clearProb, offspring_resistances, self.mutProb)
        else:
            raise NoChildException("NoChildException")

            
class Patient(SimplePatient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """
    
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        ResistantVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.drugs = []
        
    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)
            
    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.drugs
        
    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        if drugResist == []: # if no drugs are given
            return self.getTotalPop() # return total virus population
        num = 0
        for virus in self.viruses:
            resistToAll = True
            for drug in drugResist:
                # print virus.getResistance(drug)
                if not virus.getResistance(drug):
                    resistToAll = False
                    break
            if resistToAll: num += 1
        return num
                
    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly
          
        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        for virus in self.viruses[:]:
            if virus.doesClear():
                self.viruses.remove(virus)
        if self.getTotalPop() < self.maxPop:        
            popDensity = self.getTotalPop() * 1.0 / self.maxPop
            for virus in self.viruses[:]:
                try:
                    self.viruses.append(virus.reproduce(popDensity, self.getPrescriptions()))
                except NoChildException:
                    # print "Good! This virus can't reproduce a child!"
                    pass
        return self.getTotalPop()


######        
def plot_virusPop(resistances, delays, lag, naturalRun, drugs, makePlot=False):
    """a helper function for problem 4, 5, 6, 7"""
    ## initialize patient
    maxBirthProb = 0.1; clearProb = 0.05; mutProb = 0.005
    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for i in range(100)]
    patient = Patient(viruses, 1000)
    ## plot
    xVals = range(1+delays+lag+naturalRun); totPop = [patient.getTotalPop()]; resistPop = [patient.getResistPop(drugs)]
    ## initially, let viruses grow/die organically
    for i in range(delays):
        totPop.append(patient.update())
        resistPop.append(patient.getResistPop(drugs))
    ## treat patient with first drug, drug1
    patient.addPrescription(drugs[0])
    ## let viruses grow/die under the effect of drug1
    for i in range(lag):    
        totPop.append(patient.update())
        resistPop.append(patient.getResistPop(drugs))
    ## treat patient with second drug, drug2    
    if len(drugs) == 2: patient.addPrescription(drugs[1])
    ## let viruses grow/die under the effect of both drugs
    for i in range(naturalRun):    
        totPop.append(patient.update())
        resistPop.append(patient.getResistPop(drugs))    
    if makePlot:    
        pylab.figure()        
        pylab.plot(xVals, totPop, 'yo', label='total pop.')
        pylab.plot(xVals, resistPop, 'rx', label='drug resistant pop.')
        if len(drugs) == 1:
            pylab.title('virus population: %d timesteps, treated by %s, \nanother %d timesteps' %(delays, drugs[0], naturalRun))
        if len(drugs) == 2:
            pylab.title('virus population: %d timesteps, treated by %s, \nanother %d timesteps, treated by %s, another %d timesteps' %(delays, drugs[0], lag, drugs[1], naturalRun))
        pylab.xlabel('time steps')
        pylab.ylabel('population')
        pylab.legend(loc='best', numpoints=1)
        # pylab.show() 
    return totPop[-1]

def hist(num_of_trials, resistances, delays, lag, naturalRun, drugs):
    """a helper function for problem 4, 5, 6, 7"""
    finalVirusPop = []
    for i in range(num_of_trials):
        finalVirusPop.append(plot_virusPop(resistances, delays, lag, naturalRun, drugs))
    pylab.figure()
    pylab.hist(finalVirusPop)
    pylab.title('distribution of final virus population, \ndelay: %d timesteps, lag: %d timesteps, finalRun: %d timesteps' %(delays, lag, naturalRun))
    pylab.xlabel('final virus population')
    pylab.ylabel('num of patients')
    pct_cured = len([val for val in finalVirusPop if val <= 50]) * 1.0 / len(finalVirusPop)
    print 'delays: %d timesteps,'%delays, 'lag: %d timesteps,'%lag, 'naturalRun: %d timesteps,'%naturalRun, 'pct of patient cured: %f'%pct_cured

#
# PROBLEM 4
#

def problem4():
    """
    Runs simulations and plots graphs for problem 4.

    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.

    total virus population vs. time  and guttagonol-resistant virus population
    vs. time are plotted
    """
    resistances = {'guttagonol':False}
    drugsAdministered = ['guttagonol']
    plot_virusPop(resistances, 150, 0, 150, drugsAdministered, makePlot=True);

#
# PROBLEM 5
#

def problem5():
    """
    Runs simulations and make histograms for problem 5.

    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    resistances = {'guttagonol':False}
    drugsAdministered = ['guttagonol']

    plot_virusPop(resistances, 300, 0, 150, drugsAdministered, makePlot=True); 
    plot_virusPop(resistances, 150, 0, 150, drugsAdministered, makePlot=True);
    plot_virusPop(resistances, 75, 0, 150, drugsAdministered, makePlot=True); 
    plot_virusPop(resistances, 0, 0, 150, drugsAdministered, makePlot=True);
            
    num_of_trials = 100        
    hist(num_of_trials, resistances, 300, 0, 150, drugsAdministered); 
    hist(num_of_trials, resistances, 150, 0, 150, drugsAdministered);
    hist(num_of_trials, resistances, 75, 0, 150, drugsAdministered); 
    hist(num_of_trials, resistances, 0, 0, 150, drugsAdministered); 
    
#
# PROBLEM 6
#


def problem6():
    """
    Runs simulations and make histograms for problem 6.

    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
    
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    resistances = {'guttagonol':False, 'grimpex': False}
    drugsAdministered = ['guttagonol', 'grimpex']
    
    plot_virusPop(resistances, 150, 300, 150, drugsAdministered, makePlot=True); 
    plot_virusPop(resistances, 150, 150, 150, drugsAdministered, makePlot=True);
    plot_virusPop(resistances, 150, 75, 150, drugsAdministered, makePlot=True); 
    plot_virusPop(resistances, 150, 0, 150, drugsAdministered, makePlot=True);
            
    num_of_trials = 30        
    hist(num_of_trials, resistances, 150, 300, 150, drugsAdministered); 
    hist(num_of_trials, resistances, 150, 150, 150, drugsAdministered);
    hist(num_of_trials, resistances, 150, 75, 150, drugsAdministered); 
    hist(num_of_trials, resistances, 150, 0, 150, drugsAdministered); 
    
#
# PROBLEM 7
#
     
def problem7():
    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.

    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        
    """
    def plot_virusPop_p7(resistances, delays, lag, naturalRun, drugs, makePlot=False):
        """a helper function for problem 4, 5, 6, 7
           drugs: a list of two elements
        """
        ## initialize patient
        maxBirthProb = 0.1; clearProb = 0.05; mutProb = 0.005
        viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for i in range(100)]
        patient = Patient(viruses, 1000)
        ## plot
        xVals = range(1+delays+lag+naturalRun); totPop = [patient.getTotalPop()]; 
        resistPop = [patient.getResistPop(drugs)]; resistPop1 = [patient.getResistPop(drugs[:1])];
        resistPop2 = [patient.getResistPop(drugs[1:])]
        ## initially, let viruses grow/die organically
        for i in range(delays):
            totPop.append(patient.update())
            resistPop.append(patient.getResistPop(drugs))
            resistPop1.append(patient.getResistPop(drugs[:1]))
            resistPop2.append(patient.getResistPop(drugs[1:]))
        ## treat patient with first drug, drug1
        patient.addPrescription(drugs[0])
        ## let viruses grow/die under the effect of drug1
        for i in range(lag):    
            totPop.append(patient.update())
            resistPop.append(patient.getResistPop(drugs))
            resistPop1.append(patient.getResistPop(drugs[:1]))
            resistPop2.append(patient.getResistPop(drugs[1:]))        
        ## treat patient with second drug, drug2    
        patient.addPrescription(drugs[1])
        ## let viruses grow/die under the effect of both drugs
        for i in range(naturalRun):    
            totPop.append(patient.update())
            resistPop.append(patient.getResistPop(drugs))
            resistPop1.append(patient.getResistPop(drugs[:1]))
            resistPop2.append(patient.getResistPop(drugs[1:]))        
        if makePlot:    
            pylab.figure()        
            pylab.plot(xVals, totPop, 'yo', label='total pop.')
            pylab.plot(xVals, resistPop, 'rx', label='pop. resistant to both drugs')
            pylab.plot(xVals, resistPop1, 'g-', label='pop. resistant to %s'%drugs[0])
            pylab.plot(xVals, resistPop2, 'b-', label='pop. resistant to %s'%drugs[1])
            pylab.title('virus population: %d timesteps, treated by %s, \nanother %d timesteps, treated by %s, another %d timesteps' %(delays, drugs[0], lag, drugs[1], naturalRun))
            pylab.xlabel('time steps')
            pylab.ylabel('population')
            pylab.legend(loc='best', numpoints=1)
            # pylab.show() 
        return totPop[-1]
    
    resistances = {'guttagonol':False, 'grimpex': False}
    drugsAdministered = ['guttagonol', 'grimpex']        
    plot_virusPop_p7(resistances, 150, 300, 150, drugsAdministered, makePlot=True); 
    plot_virusPop_p7(resistances, 150, 0, 150, drugsAdministered, makePlot=True);
    
    

    
#
# Test
#

def f(prob, numTrials):
    cnt = 0
    for i in range(numTrials):
        if random.random() < prob: cnt += 1
    print str(cnt * 1.0 / numTrials)
    
def test_SimpleVirus():
    virus = SimpleVirus(0.2, 0.7)
    print virus.maxBirthProb, virus.clearProb
    print virus.doesClear()
    offspring = virus.reproduce(0.4)
    print offspring.maxBirthProb, offspring.clearProb
    
def test_SimplePatient():
    viruses = []
    for maxBirthProb in [0.1, 0.2, 0.3]:
        for clearProb in [0.3, 0.6]:
            viruses.append(SimpleVirus(maxBirthProb, clearProb))
    patient = SimplePatient(viruses, 200)
    print 'initial virus population:', patient.getTotalPop(), len(viruses)
    # print patient.update(), patient.getTotalPop()
    # print patient.update(), patient.getTotalPop()
    print patient.update()
    
def test_Patient():
    def compute_resistantPop(viruses):
        num_of_resistant_viruses = 0
        for virus in viruses:
            if virus.getResistance('guttagonol'):
                num_of_resistant_viruses += 1
        return num_of_resistant_viruses

    maxBirthProb = 0.1; clearProb = 0.05; 
    resistances = {'guttagonol':False}; mutProb = 1
    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for i in range(1)]
    print 'initial total virus pop:', len(viruses)
    print 'initial resistant virus pop:', compute_resistantPop(viruses)
    print
    patient = Patient(viruses, 1000)
    print 'after one step, total virus pop:', patient.update()
    print 'after one step, resistant virus pop:', patient.getResistPop(['guttagonol'])
    print 'after one step, resistant virus pop(bench):', compute_resistantPop(viruses)
    print
    print 'after two steps, total virus pop:', patient.update()
    print 'after two steps, resistant virus pop:', patient.getResistPop(['guttagonol'])
    print 'after two steps, resistant virus pop(bench):', compute_resistantPop(viruses)
    print
    print 'after three steps, total virus pop:', patient.update()
    print 'after three steps, resistant virus pop:', patient.getResistPop(['guttagonol'])
    print 'after three steps, resistant virus pop(bench):', compute_resistantPop(viruses)
    
if __name__ == '__main__':
    # f(0.7, 10000) # 0.6967
    # f(0.9, 10000) # 0.9002
    # test_SimpleVirus()
    # test_SimplePatient()
    # problem2()
    # test_Patient()
    # problem4()
    # problem5()
    # problem6()
    problem7()
    pylab.show()