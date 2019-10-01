#Nusair Islam
#Converts Irradiance to Temperature values from a csv and writes it to a different csv
#Equation taken from CubeSAT manual
#Constands used by Kobe's MatLAB script
#LOTS OF ASSUMPTIONS MADE

from datetime import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt

x = []
y = []
appendToX = x.append
appendToY = y.append
#textfile1 = input("Enter name of file to read from: ")
#textfile2 = input("Enter name of file to write to: ")
#Ro = input("Enter radius of orbit: ")

sigma = 5.67 * (10**-8) #Boltzman Constant (w/(m^2 K^4))
alpha = (0.3*0.031) + (0.7*0.83) #Temporary absorbance value of outside surface
a = 0.3 #Average Earth albeido 
epsilon = 0.3*0.039 + 0.7*0.67 #Temporary emmitance value for outside surface (Same case as absorbance)
A_tot = 2*(0.1 + 2*0.0065)*(0.1 + 2*0.0085) + 2*(0.3405 - 0.0135) #Total Surface area of satellite (m^2)
Jp = 237 #Average Planetary Radiation (w/m^2)
F = 1 #View Factor
Re = 6371*1000 #Earth Radius (m)
q_gen = 10 #Heat generated inside the sattelite via electrical components (Assume 10 w for now))

Ro = 2000000

with open("nLowEarthIrr.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
  
    with open("nIrrToTemp.csv", "w") as f:
        next(csv_reader)
        f.write('Irradiance,Temperature\n')
        lineCount = 1
        for row in csv_reader:
            lineCount+=1
            try: 
                Js = float(row[4])
                As = float(row[3])
                Ae = A_tot - As

                Tsat = ((1/(sigma*A_tot))*((alpha/epsilon)*(Js*As + Ae*a*F*Js) + Ae*Jp*(float(Ro)/Re) + q_gen/epsilon))**(1/4)

                #print('Irradiance: {} | Temperature: {} | Line Number: {}'.format(Js, Tsat, lineCount))
                f.write(str(Js)+','+str(Tsat)+'\n')

                dt = datetime.strptime(row[0], '%M:%S.%w')
                t = dt.minute * 60 + dt.second
                
                appendToX(t)
                appendToY(Tsat)
            except ValueError:
                print('Value Error at line {}'.format(lineCount))

splitAtTheseTimes = []
timeDiff = np.diff(x)
for index,diffValue in enumerate(timeDiff):
    if diffValue < 0:
        splitAtTheseTimes.append(index+1)

numSplits = len(splitAtTheseTimes)

allTimes = []
allTemps = []
allTimes.append(x[0:splitAtTheseTimes[0]])
allTemps.append(y[0:splitAtTheseTimes[0]])
for i in range(1, numSplits):
    time = []    
    temp = []
    time = x[splitAtTheseTimes[i-1]:splitAtTheseTimes[i]]
    temp = y[splitAtTheseTimes[i-1]:splitAtTheseTimes[i]]
    allTimes.append(time)
    allTemps.append(temp)

for time, temp in zip(allTimes, allTemps):
    plt.plot(time, temp)

plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()





