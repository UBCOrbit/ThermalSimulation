import csv

#textfile = input("Enter name of file: ")

sigma = 5.67 * 10**8 #Boltzman Constant (w/(m^2 K^4))
a = (0.3*0.031) + (0.7*0.83) #Temporary absorbance value of outside surface
albedo = 0.3 #Average Earth albeido 
e = 0.3*0.039 + 0.7*0.67 #Temporary emmitance value for outside surface (Same case as absorbance)
Atot = 2*(0.1 + 2*0.0065)*(0.1 + 2*0.0085) + 2*(0.3405 - 0.0135) #Total Surface area of satellite (m^2)
Jp = 237 #Average Planetary Radiation (w/m^2)
F = 1 #View Factor
Re = 6371*1000 #Earth Radius (m)
q_gen = 10 #Heat generated inside the sattelite via electrical components (Assume 10 w for now))

Ro = input("Input orbit radius")

with open ('LowEarthIR.csv') as csv file:
  csv_reader = csv_reader(csv_file, delimiter = ',')
  line_count = 1
  with open('IrradianceToTemperature.csv', mode = 'w') as IrradianceTemperature_file:
    
  for row in csv_reader:
      Js = row[4]
      As = row[3]
      Ae = Atot - As



