# Check out:
# https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_law
# https://ocw.mit.edu/courses/aeronautics-and-astronautics/16-851-satellite-engineering-fall-2003/lecture-notes/l23thermalcontro.pdf
# https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19630001247.pdf

from datetime import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt

numOrbits = 20

percentAluminum = 0.3419
percentAluminumA = 0.1574
percentPanel = 0.0864
percentCell = 0.4142

absAluminum = 0.3
absAluminumA = 0.15
absPanel = 0.65
absCell = 0.65

emiAluminum = 0.07
emiAluminumA = 0.77
emiPanel = 0.95
emiCell = 0.95

absortivity = percentAluminum * absAluminum + \
              percentAluminumA * absAluminumA + \
              percentPanel * absPanel + \
              percentCell * absCell

emisivity = percentAluminum * emiAluminum + \
            percentAluminumA * emiAluminumA + \
            percentPanel * emiPanel + \
            percentCell * emiCell 

## absortivity = (0.3*0.031) + (0.7*0.83) #Temporary absorbance value of outside surface
## emisivity = 0.3*0.039 + 0.7*0.67 #Temporary emmitance value for outside surface (Same case as absorbance)
powerFromElectronics = 0 # watts
mass = 3 # Kg 
heatCapacity = 910 # j/(kg K)
deltaTime = 1 ## seconds 
initialTemp = 273.15  ## Kelvin
ambientTemp = 2.7 ## Kelvin
sigma = 5.67 * (10**-8) #Boltzman Constant (w/(m^2 K^4))

time = []
temperature = []
incommingRadiation = []
surfaceArea = []
appendToTime = time.append
appendToTemp = temperature.append
appendToRad  = incommingRadiation.append
appendToArea = surfaceArea.append

currentTime = deltaTime
currentTemp = initialTemp
appendToTime(currentTime)
appendToTemp(currentTemp)

## name = 'LowOrbitIR'
## name = 'RegularOrbitIR'
name = 'HighOrbitIR'

def calculateTemperatureDelta(flux, surfaceArea, initialTemp):
    powerFromRadiation = SA * fluxIn * absortivity
    powerIn = powerFromRadiation + powerFromElectronics
    powerOut = SA * emisivity * sigma * (np.power(currentTemp,4) - np.power(ambientTemp,4))
    powerDelta = powerIn - powerOut
   
    energyDelta = deltaTime * powerDelta
    temperatureDelta = energyDelta / (mass * heatCapacity)
    return temperatureDelta

with open('{}.csv'.format(name), 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
  
    next(csv_reader)
    next(csv_reader)
    for row in csv_reader:
        fluxIn = float(row[4]) ## watts per meter squared
        SA = float(row[3])
        appendToRad(fluxIn)
        appendToArea(SA)
        
        temperatureDelta = calculateTemperatureDelta(fluxIn, SA, currentTemp)
        currentTemp += temperatureDelta
    
        currentTime += deltaTime
        appendToTime(currentTime)
        appendToTemp(currentTemp)
    
for i in range(0,numOrbits):
    for flux,area in zip(incommingRadiation,surfaceArea):
        temperatureDelta = calculateTemperatureDelta(flux, area, currentTemp)
        currentTemp += temperatureDelta
    
        currentTime += deltaTime
        appendToTime(currentTime)
        appendToTemp(currentTemp)

plt.plot(time, temperature)
plt.xlabel('Time in Seconds')
plt.ylabel('Temperature in Kelvin')
plt.title('Temperature vs Time for {}'.format(name))
plt.show()





