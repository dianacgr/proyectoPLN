 #!/usr/bin/env python
 # -*- coding: utf-8 -*-
#=====================================================================
#  File:      NLPlib.py
#  Summary:   part of speech tagger
#
#---------------------------------------------------------------------
#
#  Original Copyright (C) Mark Watson.  All rights reserved.
#  Python port by Jason Wiener (http://www.jasonwiener.com)
#
#THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY
#KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A
#PARTICULAR PURPOSE.
#=====================================================================

import os, sys
import pickle
import re

class NLPlib:
        lexHash = {}
        
        def __init__(self):
                if(len(self.lexHash) == 0):
                        try:
                                print("unpickle the dictionary")
                                #upkl = open('/home/raul/tageador1/pickledlexicon', 'rb')
                                upkl = open('/home/raul/tageador1/pickledlexicon', 'rb')
                                self.lexHash = pickle.load(upkl)
                                upkl.close()
                                print("Initialized lexHash from pickled data.")
                
#                               print "printing unpickled dictionary"
#                               i = 0
#                               for k,v in self.lexHash.iteritems():
#                                       if i == 100:
#                                               break
                                    #       print k, ":", v
#                                       i = i+1
                        
                        except Exception as inst:
                                print(type(inst))
                                print(inst.args)
        #finish - populatehash
################################################################################################
        #start  - DEF: tokenize
        def tokenize(self,s):
                v = []
                reg = re.compile('(\S+)')
                m = reg.findall(s);
                
                #print m
                for m2 in m:
                        #print m2
                        if len(m2) > 0:
                                 
                                       if  m2.endswith("."):
                                           v.append(m2[0:-1])
                                           v.append(".")
                                          # print "adding2: ",m2
                                       else:  
                                               if  m2.endswith(","):
                                                      v.append(m2[0:-1])
                                                      v.append(",")
                                           #           print "adding2: ",m2
                                               else:
                                                    
                                                      #v.append(m2[0:1])
                                                      v.append(m2)
                                            #          print "adding1: ",m2 
                      
                                 
                                      
                                                                             
                                                                                                                                                           
                #print "\t",v
                return v
        #finish - DEF: tokenize

        #start  - DEF: tag
        def tag(self,words):
                ret = []
                #begin tagging
                for i in range(len(words)):
                        ret.append("NN")                #the default entry
#                   print "hash_key:",words[i]

                        if words[i] in self.lexHash:
                                ret[i] = self.lexHash[words[i]]
                        else:
                                if words[i].lower() in self.lexHash:
                                        ret[i] = self.lexHash[words[i].lower()]
                
                #apply transformational rules
                for i in range(len(words)):
                        #rule 1 : DT, {VBD | VBP} --> DT, NN
                        if i > 0 and ret[i-1] == "DT":
                                if ret[i] == "VBD" or ret[i] == "VBP" or ret[i] == "VB":
                                        ret[i] = "NN"
                                        
                        #rule 2: convert a noun to a number (CD) if "." appears in the word
                        #if ret[i].startswith("N"):
                         #       if words[i].find(".") > -1:
                          #              ret[i] = "CD"
                        
                        # rule 3: convert a noun to a past participle if ((string)words[i]) ends with "ed"
                        if ret[i].startswith("N") and words[i].endswith("ed"):
                                ret[i] = "VBN"

                        # rule 4: convert any type to adverb if it ends in "ly"
                        if words[i].endswith("ly"):
                                ret[i] = "RB"
                                
                        # rule 5: convert a common noun (NN or NNS) to a adjective if it ends with "al"
                        if ret[i].startswith("NN") and words[i].endswith("al"):
                                ret[i] = "JJ"
                                
                        # rule 6: convert a noun to a verb if the preceeding work is "would"
                        if i > 0 and ret[i].startswith("NN") and words[i - 1].lower() == "would":
                                ret[i] = "VB"
                        
                        # rule 7: if a word has been categorized as a common noun and it ends with "s",
                        # then set its type to plural common noun (NNS)
                        if ret[i] == "NN" and words[i].endswith("s"):
                                ret[i] = "NNS-MP"
                        
                        # rule 8: convert a common noun to a present prticiple verb (i.e., a gerand)
                        if ret[i].startswith("NN") and words[i].endswith("ing"):
                                ret[i] = "VBG"
                        #rule 9: convert the word "por" "lo" "tanto" in por lo tanto
                        if words[i].startswith("Por") and words[i+1].startswith("lo") and words[i+2].startswith("tanto"):
                                l1=words[i]+ '_'+ words[i+1]+ '_' +words[i+2] 
                                #words[i]="Por_lo_tanto"  
                                words[i]=l1 
                                ret[i]="CONN"
                                words[i+1]= " "
                                words[i+2]= " " 
                                ret[i+1]= " "
                                ret[i+2]= " "                      
                         # rule 10 convert the word "Por lo tanto" a "Por_lo_tanto"
                        if words[i].startswith("por") and words[i+1].startswith("lo") and words[i+2].startswith("tanto"):
                                l1=words[i]+ '_'+ words[i+1]+ '_' +words[i+2] 
                                #words[i]="por_lo_tanto"  
                                words[i]=l1 
                                ret[i]="CONN"
                                words[i+1]= " "
                                words[i+2]= " " 
                                ret[i+1]= " "
                                ret[i+2]= " " 
                        #rule 11: convert the word debido a que
                        if ret[i].startswith("CONN") and words[i+1].startswith("a") and words[i+2].startswith("que"):
                                l1=words[i]+ '_'+ words[i+1]+ '_' +words[i+2]
                                #words[i]="debido_a"  
                                words[i]=l1
                                ret[i]="CONN"
                                words[i+1]= " "
                                words[i+2]= " " 
                                ret[i+1]= " "
                                ret[i+2]= " "
                         #rule 12: convert the word asi que 
                        if ret[i].startswith("RB") and words[i+1].startswith("que"):
                                #words[i]="Así"
                                l1=words[i]+ '_'+ words[i+1] 
                                words[i]=l1
                                ret[i]="CONN"
                                words[i+1]= " "
                                ret[i+1]= " "
                        #rule 13: convert the word de modo que
                        if ret[i].startswith("IN") and ret[i+1].startswith("NN-MS") and words[i+2].startswith("que"):
                                l1=words[i]+ '_'+ words[i+1]+ '_' +words[i+2] 
                                #words[i]="de modo que"  
                                words[i]=l1
                                ret[i]="CONN"
                                words[i+1]= " "
                                words[i+2]= " " 
                                ret[i+1]= " "
                                ret[i+2]= " " 
                        #rule 14: convert the word  en otras palabras
                        if ret[i].startswith("IN") and words[i+1].startswith("otras") and words[i+2].startswith("palabras"):
                                l1=words[i]+ '_'+ words[i+1]+ '_' +words[i+2] 
                                words[i]=l1
                                ret[i]="CONN_AFIR"
                                words[i+1]= " "
                                words[i+2]= " " 
                                ret[i+1]= " "
                                ret[i+2]= " " 
                        #rule 15: convert the word en particular
                        if words[i].startswith("En") and words[i+1].startswith("particular"):
                                l1=words[i]+ '_'+ words[i+1] 
                                #words[i]="debido_a"  
                                words[i]=l1
                                ret[i]="CONN"
                                words[i+1]= " "
                                ret[i+1]= " "
                        #rule 16: convert the word es decir
                        if words[i].startswith("es") and words[i+1].startswith("decir"):
                                l1=words[i]+ '_'+ words[i+1] 
                                #words[i]="debido_a"  
                                words[i]=l1
                                ret[i]="CONN"
                                words[i+1]= " "
                                ret[i+1]= " "
                        #rule 17: convert the word esto es 
                        if words[i].startswith("esto") and words[i+1].startswith("es"):
                                l1=words[i]+ '_'+ words[i+1] 
                                #words[i]="debido_a"  
                                words[i]=l1
                                ret[i]="CONN"
                                words[i+1]= " "
                                ret[i+1]= " "
                        #rule 18: convert the word Por consiguiente 
                        if words[i].startswith("Por") and words[i+1].startswith("consiguiente"):
                                l1=words[i]+ '_'+ words[i+1] 
                                #words[i]="debido_a"  
                                words[i]=l1
                                ret[i]="CONN"
                                words[i+1]= " "
                                ret[i+1]= " "
                        #rule 18: convert the word por consiguiente 
                        if words[i].startswith("por") and words[i+1].startswith("consiguiente"):
                                l1=words[i]+ '_'+ words[i+1] 
                                #words[i]="debido_a"  
                                words[i]=l1
                                ret[i]="CONN"
                                words[i+1]= " "
                                ret[i+1]= " "
                         #rule 19: convert the word en particular
                        if words[i].startswith("En") and words[i+1].startswith("consecuencia"):
                                l1=words[i]+ '_'+ words[i+1] 
                                #words[i]="en_consecuencia"  
                                words[i]=l1
                                ret[i]="CONN"
                                words[i+1]= " "
                                ret[i+1]= " "
                         #rule 20: convert the word en particular
                        if words[i].startswith("dado") and words[i+1].startswith("que"):
                                l1=words[i]+ '_'+ words[i+1] 
                                #words[i]="Dado_que"  
                                words[i]=l1
                                ret[i]="CONN"
                                words[i+1]= " "
                                ret[i+1]= " "
                         #rule 20:   ################# problema de ambiguiedad de y 
                        if words[i].startswith("X") and  ret[i+1].startswith("CC") and words[i+3].startswith("conjunto"):
                                #l1=words[i]+ '_'+ words[i+1]+ '_' +words[i+2] 
                                #words[i]="de modo que"  
                                #words[i]=l1
                                ret[i+1]="CONN-CC"
                         #rule 21:
                        if words[i].startswith("A") and  ret[i+1].startswith("CC") and words[i+3].startswith("conjunto") and words[i+4].startswith("X") :
                                #l1=words[i]+ '_'+ words[i+1]+ '_' +words[i+2] 
                                #words[i]="de modo que"  
                                #words[i]=l1
                                ret[i+1]="CONN-CC"
                         #rule 22:
                        if words[i].startswith("A") and  ret[i+1].startswith("CC") and words[i+3].startswith("elemento") and words[i+4].startswith("x") :
                                #l1=words[i]+ '_'+ words[i+1]+ '_' +words[i+2] 
                                #words[i]="de modo que"  
                                #words[i]=l1
                                ret[i+1]="CONN-CC"
                         #rule 23: # VBZ-PI con entonces, por tanto y por lo tanto
                        if words[i].startswith("Entonces") and words[i+3].startswith("x") and ret[i+4].startswith("VBZ-SI"):
                                #l1=words[i]+ '_'+ words[i+1]+ '_' +words[i+2] 
                                #words[i]="de modo que"  
                                #words[i]=l1
                                ret[i+4]="VBZ-PI"
                         #rule 24:
                        if words[i].startswith("Suponga") and words[i+1].startswith("que"):
                                #words[i]="Suponga que"
                                l1=words[i]+ '_'+ words[i+1] 
                                words[i]=l1
                                ret[i]="EXPRE"
                                words[i+1]= " "
                                ret[i+1]= " "        
                        if words[i].startswith("suponga") and words[i+1].startswith("que"):
                                #words[i]="Suponga que"
                                l1=words[i]+ '_'+ words[i+1] 
                                words[i]=l1
                                ret[i]="EXPRE"
                                words[i+1]= " "
                                ret[i+1]= " "   
                        if words[i].startswith("Sea") and words[i+1].startswith("que"):
                                #words[i]="Suponga que"
                                l1=words[i]+ '_'+ words[i+1] 
                                words[i]=l1
                                ret[i]="EXPRE"
                                words[i+1]= " "
                                ret[i+1]= " "   
######################################################################
#############En esta parte  se  modelan  el del y al insertano una nueva palabra en del la palabra el
# y en al la palabra el
                        #rule 23: convert the word del in de el: en este caso se debe insertar la segunda palabra 'el' eso se realiza con el
                        # insert(i,string) que adiciona el string en la posicin i. 
                        if words[i].startswith("del"):
                                #l1=words[i]+ ' '+ words[i+1]+ ' ' +words[i+2] 
                                #words[i]="de modo que"  
                                words[i]="de"
                                ret[i]="IN"
                                words.insert(i+1,"el")
                                ret.insert(i+1,"DA-MS")
                       #rule 24: convert the word al in a el: en este caso se debe insertar la segunda palabra 'a' eso se realiza con el
                        # insert(i,string) que adiciona el string en la posicion i. 
                        if words[i].startswith("al"):
                                #l1=words[i]+ ' '+ words[i+1]+ ' ' +words[i+2] 
                                #words[i]="de modo que"  
                                words[i]="a"
                                ret[i]="IN"
                                words.insert(i+1,"el")
                                ret.insert(i+1,"DA-MS") 
                        #rule 24: convert De manera que in De_manera_que
                        if ret[i].startswith("IN") and ret[i+1].startswith("MA") and words[i+2].startswith("que"):
                                l1=words[i]+ '_'+ words[i+1]+ '_' +words[i+2] 
                                #words[i]="de manera que"  
                                words[i]=l1
                                ret[i]="CONN"
                                words[i+1]= " "
                                words[i+2]= " " 
                                ret[i+1]= " "
                                ret[i+2]= " "
                        #rule 25: convert Por tanto en Por_tanto
                        if words[i].startswith("Por") and words[i+1].startswith("tanto"):
                                l1=words[i]+ '_'+ words[i+1] 
                                #words[i]="Por_lo_tanto"  Arg_120.mrg
                                words[i]=l1 
                                ret[i]="CONN"
                                words[i+1]= " "
                                ret[i+1]= " "
                         #rule 25: convert Por tanto en Por_tanto
                        if words[i].startswith("por") and words[i+1].startswith("tanto"):
                                l1=words[i]+ '_'+ words[i+1] 
                                #words[i]="Por_lo_tanto"  Arg_120.mrg
                                words[i]=l1 
                                ret[i]="CONN"
                                words[i+1]= " "
                                ret[i+1]= " " 
                        #rule 26: convert De igual modo 
                        if ret[i].startswith("IN") and words[i+1].startswith("igual") and words[i+2].startswith("modo"):
                                l1=words[i]+ '_'+ words[i+1]+ '_' +words[i+2] 
                                #words[i]="de modo que"  
                                words[i]=l1
                                ret[i]="CONN"
                                words[i+1]= " "
                                words[i+2]= " " 
                                ret[i+1]= " "
                                ret[i+2]= " " 
                        #rule 27: [DG-01] Identifica una asignación,  el operador de asignación                                
                        if ret[i-1].startswith("ASIG") and words[i].startswith("a"):
                                l1=words[i-1]+ '_'+ words[i] 
				words[i-1]=l1
				ret[i-1]="ASIG_A"
                                ret[i]=" "
                                words[i]= " "
                        #rule 28: [DG-02] Identifica una asignación, etiqueta el valor asignado si no es una variable                                
                        if ret[i-1].startswith("ASIG_A") and ret[i+3] != "VAR":
				ret[i+3]="VALUE"
                        #rule 29: [DG-03] Identifica una operación aritmetica, y etiqueta los operandos si no son variables
                        if ret[i].startswith("OPER")  and ret[i-1] != "VAR":
				ret[i-1]="VALUE"
                        #rule 30: [DG-04] Identifica una operación aritmetica, y etiqueta los operandos si no son variables
                        if ret[i].startswith("OPER")  and ret[i+1] != "VAR":
				ret[i+1]="VALUE"
                        #rule 31: [DG-05] Identifica una operación aritmetica división, y etiqueta los operandos si no son variables
			if words[i].startswith("dividido") and ret[i+2] != "VAR":
				ret[i+2]="VALUE"
                        #rule 32: [DG-06] Identifica una operación aritmetica división, y etiqueta la operación: dividido_por, dividido_entre
			if words[i].startswith("dividido"):
                                l1=words[i]+ '_'+ words[i+1] 
				words[i]=l1
                                ret[i+1]=" "
                                words[i+1]= " "
                        #rule 33: [DG-07] Identifica una comparación, y etiqueta la desigualdad: es_menor_que, es_mayor_que, es_igual_a, es_diferente_a
			if ret[i].startswith("COMP"):
                                l1=words[i-1]+ '_'+ words[i]+ '_'+ words[i+1] 
				words[i-1]=l1
                                ret[i-1]="COMP"
                                words[i]= " "
                                ret[i]=" "
                                words[i+1]= " "
                                ret[i+1]=" "
                        #rule 34: [DG-08] Identifica una comparación, y etiqueta los operandos si no son variables
			if ret[i-1].startswith("COMP") and ret[i+2] != "VAR":
                          	ret[i+2]="VALUE"
                        #rule 35: [DG-09] Identifica una condición de parada de ciclo, y la trasforma: hasta_que
			if ret[i].startswith("LOOP_COND") and words[i].startswith("Hasta"):
                                l1=words[i]+ '_'+ words[i+1]
				words[i]=l1
                                words[i+1]= " "
                                ret[i+1]=" "
                        #rule 36: [DG-10] Identifica una condición de selección multiple, y la trasforma: En_Caso_que
			if ret[i].startswith("COND_MULT"):
                                l1=words[i-1]+ '_'+ words[i]+ '_'+ words[i+1]
				words[i-1]=l1
                                ret[i-1]="COND_MULT"
                                words[i]= " "
                                ret[i]=" "
                                words[i+1]= " "
                                ret[i+1]=" "
                        #rule 37: [DG-11] Identifica una ciclo for, y lo etiqueta: Para desde hasta
			if ret[i].startswith("LOOP") and words[i].startswith("Para"):
                                ret[i+2]="LOOP_FROM"
                                ret[i+4]="LOOP_TO"

                return ret
        #finish - DEF: tag

print "beginning test"
#comment everything below when done testing
#o = NLPlib()
#s = "The mosquito bit the boy. "
#s = "Tiger Woods, finished the big. tournament at par "
#s = "el conjunto x es B, es decir, x es B."
#v = o.tokenize(s)
#t = o.tag(v)
#for i in range(len(v)):
 #     print v[i],"(",t[i],")"

