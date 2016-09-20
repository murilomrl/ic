import json
from pprint import pprint
import csv
from nltk import word_tokenize as Tokenize
from nltk import pos_tag as Tag
from nltk.stem.snowball import SnowballStemmer

import re, collections

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(open('big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)
listaTotal=[]
def percorreCSV():
	#lista que contem dicionarios com nome e atributos da classe, formato [{nome: "", atributo: ""}]
	listaDeRelationships=[]
	with open('arquivoFormatoParRadical1909.csv', 'r') as csvfile:
		arquivo = csv.reader(csvfile, delimiter=',')
		for row in arquivo:
			listaTotal.append(row)
			listaDeRelationships+=[row[0]]
	tiraPreposicoes(listaDeRelationships)

def tiraPreposicoes(listaDicionario):

	#lista que vai "abrigar as palavras limpas"
	listaResultado = []

	listaDeNomes = []
	listaOccur = []
	indiceDaRelacao=0
	#loop que percorre os nomes das classes, pega apenas os substantivos e os guarda como nome da classe
	for j in listaDicionario:
		j = j.split()
		for certo in j:
			j[j.index(certo)]=correct(certo)
		espaco=" "
		j=espaco.join(j)
		#inicializacao das variaveis que abrigam os returns das funcoes da biblioteca nltk que separam as palavras com tags classificando-as sintaticamente
		tokens = Tokenize(j)
		tagged = Tag(tokens)
		maiorPalavra=""
		check=False
		#loop que percorre as tags e suas palavras correspondentes procurando por substantivos, que sao denotados na nltk como 'NN', 'NNP' ou 'NNS'
		for i in tagged:
			k=0
			if(i[k+1] == 'NN' or i[k+1] == 'NNP' or i[k+1] == 'NNS' or i[k+1] == 'VB' or i[k+1] == 'JJ'):
				check=True
				if(len(i[k])>len(maiorPalavra)):
					maiorPalavra=i[k]
			if(check==False):
				if(len(i[k])>len(maiorPalavra)):
					maiorPalavra=i[k]
		listaTotal[indiceDaRelacao][0]=maiorPalavra
		if(indiceDaRelacao%10000==0):
			print(indiceDaRelacao)
		indiceDaRelacao+=1
	print("Limpeza de preposicoes terminada.\n")
	criaSemelhanteCSV(listaTotal, 'arquivoFINALFormatoParPrep1909')
	comparaRadical(listaTotal)
	
#Funcao que utiliza a saida de tiraPreposicoes e compara palavra a palavra pelo radical utilizando stemmer
def comparaRadical(listaDeNomesLimpos):

	#tecnica da biblioteca nltk que possui a funcao de comparar palavras segundo seu radical
	stemmer=SnowballStemmer("english")
	i=0
	while(i<len(listaTotal)):
		listaTotal[i][0]=stemmer.stem(listaTotal[i][0])
		i+=1
	criaSemelhanteCSV(listaTotal,"arquivoFINALFormatoParRadical1909")



#########################################
#										#
#	BLOCO DE ESCRITA NO ARQUIVO			#
#										#
#########################################

def criaSemelhanteCSV(listaSemelhantes, nomeArquivo):
	arquivoSemelhantes=csv.writer(open(nomeArquivo+".csv","w"))
	i=0
	for dicionario in listaSemelhantes:
		#if nomeArquivo=="semelhanteRadical":
		#	arquivoSemelhantes.writerow([dicionario["nome"], dicionario["ocorrencia"]])#, dicionario["atributos"]])
		#else:
		arquivoSemelhantes.writerow(dicionario)
		i+=1


percorreCSV()