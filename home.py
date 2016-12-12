#! /usr/bin/python2.7
# -*- coding: utf-8 -*-
import nltk
import os
import shlex, subprocess
from stanfordnlp import StanfordCoreNLP
from nltk.parse import stanford
from parseval import Modelo
from nltk.tree import Tree
from nltk.draw.tree import TreeView

import sys
reload(sys)  
sys.setdefaultencoding('utf8')


def createStanfordTree(entrada):
	stanford_tree=coreStanfordNLP.raw_parse(entrada)['sentences'][0]['parsetree']
	#print stanford_tree
	if "(S" in  stanford_tree:
        	stanford_tree=stanford_tree[stanford_tree.index("(S"):stanford_tree.rindex(")")]
	return stanford_tree

def createBikelTree(entrada):
	#tokenizacion con nltk 
	tokens = nltk.word_tokenize(entrada)
	#pos tag
	textoPostag = nltk.pos_tag(tokens)
	#convertir formato para que sea aceptado
	textoPreprocesado = "("
	for index in range(len(textoPostag)):
		textoPreprocesado +=  "( " + textoPostag[index][0] + " ( " + textoPostag[index][1]+ " ) )"
	textoPreprocesado += ")"
	#se escribe el texto preprocesado en un archivo llamado entradaBikel y este es el que se utiliza para el analisis sintactico
	f = open('entradaBikel', 'w')
	f.write(textoPreprocesado)
	f.close()
	#se crea args....? 
	args = shlex.split("tcsh ../dbparser/bin/parse 400 ../dbparser/settings/collins.properties ../wsj-02-21.obj.gz entradaBikel")	
	#
	p = subprocess.Popen(args,stderr=subprocess.STDOUT)	
	p.wait()
	f2 = open('entradaBikel.parsed', 'r')
	BikelTree = f2.read()
	return BikelTree

def obtenerMedidas(arbolCreado, arbolReferencia):
	model = Modelo()
	medidas = model.parseval(arbolCreado, arbolReferencia, "-i")	
	return medidas

def generarArbol(arbol,analizador):
	nombre = analizador+"tree"
	t = Tree.fromstring(arbol)
	TreeView(t)._cframe.print_to_file(nombre+".ps")
	os.system("convert "+nombre+".ps "+nombre+".png")

if __name__ == "__main__":
	print "corenlp path"
	corenlp_dir = "../stanford-corenlp-full-2015-04-20/"
	print "load stanford"
	coreStanfordNLP = StanfordCoreNLP(corenlp_dir) 
	arbol = createStanfordTree("PS of New Hampshire shares closed yesterday at $3.75, off 25 cents, in New York Stock Exchange composite trading.")
	print arbol
	arbol2 = createBikelTree("PS of New Hampshire shares closed yesterday at $3.75, off 25 cents, in New York Stock Exchange composite trading.")
	print arbol2
	arbolRef = "( (S (NP-SBJ (NAC (NNP PS) (PP (IN of) (NP (NNP New) (NNP Hampshire) ))) (NNS shares) ) (VP (VBD closed) (NP-TMP (NN yesterday) ) (PP-CLR (IN at) (NP (NP ($ $) (CD 3.75) (-NONE- *U*) ) (, ,) (PP-DIR (IN off) (NP (CD 25) (NNS cents) )) (, ,) )) (PP-LOC (IN in) (NP (NNP New) (NNP York) (NNP Stock) (NNP Exchange) (JJ composite) (NN trading) )))(. .) ))"
	print arbol
	medidasStanford = obtenerMedidas(arbol, arbolRef)
	print medidasStanford
	medidasBikel = obtenerMedidas(arbol2, arbolRef)
	print medidasBikel
	generarArbol(arbol, "stanford")
	generarArbol(arbol2, "bikel")
