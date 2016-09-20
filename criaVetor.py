import csv
with open('arquivoFormatoParRadical.csv','r') as csvfile:
	filereader = csv.reader(csvfile, delimiter=',')
	lista=[]
	for row in filereader:
		lista.append(row)
vetorId=[]
vetorRel=[]
vetorBooleano=[]
vetorClass=[]
listaLimpa=[]
print "\nVetor Relacao\n"
for tupla in lista:
	if((tupla[0] == "woman" and tupla[2] == "man") or (tupla[2] == "woman" and tupla[0] == "man")):
		try:
			vetorId.index(tupla[3])
		except ValueError:
			vetorId.append(tupla[3])
		vetorRel.append(tupla[1])
for imageId in vetorId:
	listaClasseTemporaria=[]
	for tupla in lista:
		if(imageId==tupla[3]):
			listaLimpa.append(tupla)
			vetorClass.append(tupla[0])
			vetorClass.append(tupla[2])
			# print listaClasseTemporaria
vetorClass = list(set(vetorClass))
print vetorRel[1]
print "\nVetor de Classes\n"
print vetorClass
listaZerada=[]
i=0
# count=0
while i<len(vetorClass):
	listaZerada.append(0)
	i+=1
print "\nVetor booleano\n"
for imageId in vetorId:
	listaBooleanaTemporaria=listaZerada[:]
	i=0
	for classe in vetorClass:
		for tupla in listaLimpa:
			if(imageId==tupla[3]):
				if(classe==tupla[0] or classe ==tupla[2]):
					listaBooleanaTemporaria[i]=1
					print "\n"
					print vetorClass[i]
		i+=1
	vetorBooleano.append(listaBooleanaTemporaria)
	break
	# count+=1
print "\n"
print vetorBooleano