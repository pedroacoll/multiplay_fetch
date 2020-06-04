import csv
import math

filename= 'stringency_country_date.csv'
estructura_paises=[]
paises=[]

fechas=[]
estructura_fechas=[]
with open(filename, 'r') as f:   
    reader = csv.reader(f)     
    for indice, row in enumerate(reader):  
    	if indice == 0 :
    		for i in row:
    			estructura_paises.append('')
    			paises.append(i)
    	fechas.append(row[0])
    	estructura_fechas.append('')

#print(len(estructura_paises),paises,len(estructura_fechas))
    fechas=fechas[1:]
    #print(fechas)
    f.close()

for n in range(len(paises)):
	datos=[]
	datos2=''
	with open(filename, 'r') as fg:
		reader = csv.reader(fg)
		print('la n es ' + str(n))
		for row in reader:
			datos.append(row[n])
			datos2+=';'+row[n]
		print(datos2)
		#print(datos)
	fg.close()