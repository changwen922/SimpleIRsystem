#from pprint import pprint
import argparse
import csv
import os
from pprint import pprint

import numpy as np
from numpy.linalg import norm
from textblob import TextBlob as tb

import util
from chi_VectorSpace import chi_VectorSpace
from Parser import Parser
from tfidf import *


def parse_args():
    argparser = argparse.ArgumentParser() 
    argparser.add_argument('--query', default = "Taiwan YouTube COVID-19", help='請輸入英文關鍵字')
    argparser.add_argument('--query2', default = "烏克蘭 大選", help='請輸入中文關鍵字')

    return argparser.parse_args()

class VectorSpace:
    documentVectors = []
    vectorKeywordIndex=[]
    data = []
    parser=None
    

    def __init__(self, documents = [] ):
        self.documentVectors = []
        self.parser = Parser()
        self.data = []
        self.Bloblist = self.getbloblist(documents)
        if(len(documents)>0):
            self.build(documents)

    def getbloblist(self, documents):
        bloblist = []
        for doc in documents:
            wordlist = self.parser.tokenise(doc)
            wordlist = self.parser.removeStopWords(wordlist)
            bloblist.append(tb(" ".join(wordlist)))
        return bloblist

    def build(self,documents):
        self.vectorKeywordIndex = self.getVectorKeywordIndex(documents)
        self.documentVectors = [self.makeVector(document) for document in documents]

        #print(self.vectorKeywordIndex)
        #print(self.documentVectors)


    def getVectorKeywordIndex(self, documentList):

        #Mapped documents into a single word string	
        vocabularyString = " ".join(documentList)
        vocabularyList = self.parser.tokenise(vocabularyString)
        #Remove common words which have no search value
        vocabularyList = self.parser.removeStopWords(vocabularyList)
        uniqueVocabularyList = util.removeDuplicates(vocabularyList)

        vectorIndex={}
        offset=0
        #Associate a position with the keywords which maps to the dimension on the vector used to represent this word
        for word in uniqueVocabularyList:
            vectorIndex[word]=offset
            offset+=1
        return vectorIndex  #(keyword:position)


    def makeVector(self, wordString):
    
        #Initialise vector with 0's
        vector = [0] * len(self.vectorKeywordIndex)
        wordList = self.parser.tokenise(wordString)
        wordList = self.parser.removeStopWords(wordList)
        tbstring = tb(" ".join(wordList))
        for word in list(set(wordList)):
            if word in self.vectorKeywordIndex:
                vector[self.vectorKeywordIndex[word]] = tfidf(word, tbstring , self.Bloblist) 
        return vector


    def buildQueryVector(self, termList):
        """ convert query string into a term vector """
        query = self.makeVector(" ".join(termList))
        return query


    def related(self,documentId):
        """ find documents that are related to the document indexed by passed Id within the document Vectors"""
        ratings = [util.cosine(self.documentVectors[documentId], documentVector) for documentVector in self.documentVectors]
        #ratings.sort(reverse=True)
        return ratings


    def search(self,searchList, mode = 'cos'):
        """ search for documents that match based on a list of terms """
        if type(searchList[0]) == str:
            queryVector = self.buildQueryVector(searchList)
        else:
            queryVector = searchList
        
        if mode == 'cos':
            ratings = [util.cosine(queryVector, documentVector) for documentVector in self.documentVectors]
            #ratings.sort(reverse=True)
            return ratings
        if mode == 'euc':
            ratings = [util.Euclidean(queryVector, documentVector) for documentVector in self.documentVectors]
            #ratings.sort(reverse=True)
            return ratings
    
    def getQ1answer(self, searchlist, files, n, mode = 'cos'):
        answer = self.search(searchlist, mode = mode)
        print( 'NewsID' ,'         ','score')
        for i in np.flip(np.argsort(answer))[:n]:
            print(files[i],'    ' ,round(answer[i],6))
        print('--------------------------------------')
        return np.flip(np.argsort(answer))[:n]
    
    def getQ2query(self, searchlist, q1answer):
        queryvector = self.buildQueryVector(searchlist)
        feedbackvector = self.buildQueryVector(q1answer)
        qarray = np.array(queryvector)
        frray = np.array(feedbackvector)
        newvector = list(qarray + 0.5 * frray)
        return newvector

    def getQ4answer(self,searchlist, files,n, mode='cos', h = int):
        answer2 = self.search(searchlist, mode = mode)
        self.data = [] #哪幾個檔案被搜尋到
        d1 = []
        for i in np.flip(np.argsort(answer2))[:n]:
            d1.append(files[i])
        for j in d1:
            a = j[1:]
            self.data.append(a)
        #print(self.data)
        
        TP = [x for x in self.data if x in fin_rel[h]]
        tp_count = len(TP)
        recall = tp_count/len(fin_rel[h])
        map = tp_count/10

        for b in range(10):
            if self.data[b] in fin_rel[h]:
                mrr = 1/(b+1)
            else:
                mrr = 0
        finn = list([recall, map, mrr])
        return finn
    
   
        

if __name__ == '__main__': 
    args = parse_args()

    #Q1
    #讀檔
    documents = []
    filenames = []
    for file in os.listdir('EnglishNews'):
        path = os.path.join('EnglishNews', file)
        filenames.append(file)
        with open(path, encoding='utf-8') as f:
            if file.endswith('.txt'):
                lines = f.readlines()
                doc = ' '.join(lines)
                doc1 = doc.replace("\n", "")
                documents.append(doc1)

    query = [args.query]
    #做TF-IDF Weighting+Cosine Similarity
    vectorSpace = VectorSpace(documents)
    print('Question1-1\nTF-IDF Weighting (Raw TF in course PPT) + Cosine Similarity:\n')
    cosans = vectorSpace.getQ1answer(query,filenames, 10,'cos')
    #做TF-IDF Weighting+Euclidean Distance
    print('Question1-2\nTF-IDF Weighting (Raw TF in course PPT) + Euclidean Distance:\n')
    eucans = vectorSpace.getQ1answer(query,filenames, 10,'euc')



    #Q2
    print('Question2\nUsing Relevance Feedback Answer:\n')
    feedbackdoc = [" ".join(documents[cosans[0]])]
    feedbackquery = vectorSpace.getQ2query(query, feedbackdoc)
    vectorSpace.getQ1answer(feedbackquery,filenames, 10,'cos')


    

    
    #Q3
    #讀檔
    documents_chi = []
    files_chi = []
    for file in os.listdir("./ChineseNews"):
        if file.endswith(".txt"):
            filename_chi = os.path.join("./ChineseNews", file)
            files_chi.append(file[:-4])
            with open(filename_chi, encoding="utf-8") as f:
                lines = f.readlines()
                doc = ' '.join(lines)
                doc1 = doc.replace("\n", "")
                documents_chi.append(doc1)

    query3 = [args.query2]
    #做TF Weighting+Cosine Similarity
    chi_vectorSpace_tf = chi_VectorSpace(documents_chi, 'tf')
    chi_vectorSpace_tf.getQ3answer(query3, files_chi,10)
    #做TF-IDF Weighting+Cosine Similarity
    chi_vectorSpace_tfidf = chi_VectorSpace(documents_chi, 'tf-idf')
    chi_vectorSpace_tfidf.getQ3answer(query3, files_chi,10)
    



    #Q4
    #讀檔
    smalldata = []
    smalldatanames = []
    for file in os.listdir('smaller_dataset/collections'):
        if file.endswith(".txt"):
            filename = os.path.join('smaller_dataset/collections', file)
            smalldatanames.append(file[:-4])
            with open(filename, encoding="utf-8") as f:
                lines = f.readlines()
                doc = ' '.join(lines)
                doc1 = doc.replace("\n", "")
                smalldata.append(doc)
    
    query3 = []
    for qu in os.listdir('smaller_dataset/queries'):
        if file.endswith(".txt"):
            quname = os.path.join('smaller_dataset/queries', qu)
            with open(quname, encoding="utf-8") as q:
                que = q.read()
                #que1 = ' '.join(que)
                #que2 = que1.replace("\n", "")
                query3.append(que)
    #print(query[0])
    #讀取已標記資料
    rel = []
    fin_rel = []
    with open('smaller_dataset/rel.tsv', encoding='utf-8') as r:
        tsv = csv.reader(r, delimiter='\t' )
        for line in tsv:
            rel.append(line)
    i=0
    for i in range(len(rel)):
        a = rel[i][1].replace('[','').replace(',','').replace(']','')
        b = a.split()
        fin_rel.append(b)
    
    #每筆query和smalldata做TF-IDF Weighting+Cosine Similarity
    #排序後的資料去和標記過的資料做RECALL,MAP及MRR
    retri = VectorSpace(smalldata)
    recall = 0
    map = 0
    mrr = 0
    h = 0 
    while h<76 :
        r = retri.getQ4answer(query3[h],smalldatanames, 10,'cos', h)
        recall =  recall + r[0]
        map = map + r[1]
        mrr = mrr + r[2]
        h += 1
    
    recall_ans = round(recall/76 , 6)
    recall_map = round(map/76 , 6)
    recall_mrr = round(mrr/76 , 6)
    print('Question4\ntfidf retrieve...\n')
    print('--------------------------------------')
    print('tdidf    RECALL@10    ', recall_ans)
    print('tdidf    MAP@10       ', recall_map)
    print('tdidf    MRR@10       ', recall_mrr)

