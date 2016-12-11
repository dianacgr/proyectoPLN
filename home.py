#! /usr/bin/python2.7
# -*- coding: utf-8 -*-
import nltk
import os
import shlex, subprocess
from stanfordnlp import StanfordCoreNLP
from nltk.parse import stanford
#from parseval import parseval

import sys
reload(sys)  
sys.setdefaultencoding('utf8')


def createStanfordTree(entrada):
	stanford_tree=coreStanfordNLP.raw_parse(entrada)['sentences'][0]['parsetree']
	#print stanford_tree
	if "(S" in  stanford_tree:
        	stanford_tree=stanford_tree[stanford_tree.index("(S"):stanford_tree.rindex(")")-1]
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

def obtenerMedidas(arbolReferencia, arbolCreado):
	medidas = parseval(arbolReferencia, arbolCreado)	
	return medidas

if __name__ == "__main__":
	print "corenlp path"
	corenlp_dir = "../stanford-corenlp-full-2015-04-20/"
	print "load stanford"
	coreStanfordNLP = StanfordCoreNLP(corenlp_dir) 
	arbol = createStanfordTree("The thrift holding company said it expects to obtain regulatory approval and complete the transaction by year-end.")
	print arbol
	arbol2 = createBikelTree("The thrift holding company said it expects to obtain regulatory approval and complete the transaction by year-end.")
	print arbol2
	#arbolRef = "( (S (NP-SBJ (DT The) (NN thrift) (VBG holding) (NN company) ) (VP (VBD said) (SBAR (-NONE- 0) (S (NP-SBJ-1 (PRP it) ) (VP (VBZ expects) (S (NP-SBJ (-NONE- *-1) ) (VP (TO to) (VP (VP (VB obtain) (NP (JJ regulatory) (NN approval) )) (CC and) (VP (VB complete) (NP (DT the) (NN transaction) ))(PP-TMP (IN by) (NP (NN year-end) ))))))))) (. .) ))"
	#medidasStanford = obtenerMedidas(arbolRef, arbol)
	#print medidasStanford
