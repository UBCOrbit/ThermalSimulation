# Check out:
# https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_law
# https://ocw.mit.edu/courses/aeronautics-and-astronautics/16-851-satellite-engineering-fall-2003/lecture-notes/l23thermalcontro.pdf
# https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19630001247.pdf

from datetime import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt

numOrbits = 6

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

surfaceAreaTot = 0.153 # m^2
surfaceAreaSun = surfaceAreaTot / 2
surfaceAreaEarth = surfaceAreaTot / 2

## absortivity = (0.3*0.031) + (0.7*0.83) #Temporary absorbance value of outside surface
## emisivity = 0.3*0.039 + 0.7*0.67 #Temporary emmitance value for outside surface (Same case as absorbance)
powerFromElectronics = 0 # watts
mass = 3 # Kg 
heatCapacity = 910 # j/(kg K)
deltaTime = 1 ## seconds 
initialTemp = 273.15  ## Kelvin
ambientTemp = 2.7 ## Kelvin
sigma = 5.67 * (10**-8) #Boltzman Constant (w/(m^2 K^4))
radiusEarth = 63781000 #meters
fluxEarth = 273
albedo = 0.3

time = []
temperature = []
incomingRadiation = []
appendToTime = time.append
appendToTemp = temperature.append
appendToRad  = incomingRadiation.append

currentTime = deltaTime
currentTemp = initialTemp
appendToTime(currentTime)
appendToTemp(currentTemp)

## name = 'LowOrbitIR'
## name = 'RegularOrbitIR'
name = 'HighOrbitIR'

## altitude = 400 #meters
## altitude = 600 #meters
altitude = 800 #meters

def sineRhoSquared():
    return radiusEarth**2 / ((altitude + radiusEarth)**2)

def ka():
    return 0.664 + 0.521*np.arcsin((sineRhoSquared()**(1/2))) + 0.203*(np.arcsin((sineRhoSquared()**(1/2)))**2)

def calculateTemperatureDelta(fluxSun, initialTemp):
    powerOut = -surfaceAreaTot * emisivity * sigma * (np.power(currentTemp,4) - np.power(ambientTemp,4))
    powerInSun = surfaceAreaSun * absortivity * fluxSun
    powerInEarth = surfaceAreaEarth * emisivity * fluxEarth * sineRhoSquared()
    powerInAlbedo = surfaceAreaEarth * absortivity * albedo * fluxSun * ka() * sineRhoSquared()
    powerInElectronics = powerFromElectronics

    powerDelta = powerOut + powerInSun + powerInEarth + powerInAlbedo + powerInElectronics
   
    energyDelta = deltaTime * powerDelta
    temperatureDelta = energyDelta / (mass * heatCapacity)
    return temperatureDelta

with open('{}.csv'.format(name), 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
  
    next(csv_reader)
    next(csv_reader)
    for row in csv_reader:
        fluxSun = float(row[4]) ## watts per meter squared
        appendToRad(fluxSun)
        
        temperatureDelta = calculateTemperatureDelta(fluxSun, currentTemp)
        currentTemp += temperatureDelta
    
        currentTime += deltaTime
        appendToTime(currentTime)
        appendToTemp(currentTemp)
    
for i in range(0,numOrbits):
    for fluxSun in incomingRadiation:
        temperatureDelta = calculateTemperatureDelta(fluxSun, currentTemp)
        currentTemp += temperatureDelta
    
        currentTime += deltaTime
        appendToTime(currentTime)
        appendToTemp(currentTemp)

plt.plot(time, temperature)
plt.xlabel('Time in Seconds')
plt.ylabel('Temperature in Kelvin')
plt.title('Temperature vs Time for {}'.format(name))
plt.show()





