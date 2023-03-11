import glob
import math
import os
from pprint import pprint

import jieba
import numpy as np
from numpy.linalg import norm
from textblob import TextBlob as tb

import util
from Parser import Parser
from tfidf import *


class chi_VectorSpace:
    
    documentVectors = []
    vectorKeywordIndex = []
    parser=None
    
    def __init__(self, documents=[], mode = 'tf'):
        self.documentVectors=[]
        self.parser = Parser()
        self.BlobList = self.getBlobList(documents)
        self.mode = mode
        if(len(documents)>0):
            self.build(documents)
    
    def getBlobList(self, documents): 
        bloblist = []
        for doc in documents:
            wordList = self.parser.tokenise(doc)
            wordList = self.parser.removeStopWords(wordList)
            bloblist.append(tb(" ".join(wordList)))
        return bloblist
            
    def build(self,documents):
        self.vectorKeywordIndex = self.getVectorKeywordIndex(documents)
        self.documentVectors = [self.makeVector(document, self.mode) for document in documents]

    def is_chinese(self, string):
        for word in string:
            if u'\u4e00' <= word <= u'\u9fff':
                return True
        return False
    
    def getVectorKeywordIndex(self, documentList):
        """ create the keyword associated to the position of the elements within the document vectors """
        en_doc = []
        ch_doc = []
        #Mapped documents into a single word string	
        for doc in documentList:
            if self.is_chinese(doc) == False:
                en_doc.append(doc)
            else:
                ch_doc.append(doc)
        
        #處理英文資料
        vocabularyString= " ".join(en_doc)
        vocabularyList = self.parser.tokenise(vocabularyString) 
        vocabularyList = self.parser.removeStopWords(vocabularyList) 
        
        #處理中文資料
        ch_vocabularyString = " ".join(ch_doc)
        ch_vocabularyList = jieba.lcut_for_search(ch_vocabularyString) 
        ch_vocabularyList = self.parser.chi_removeStopWords(ch_vocabularyList)

        #mix
        vocabularyList.extend(ch_vocabularyList)
        
        uniqueVocabularyList = util.removeDuplicates(vocabularyList)
        
        
        vectorIndex={}
        offset=0
        #Associate a position with the keywords which maps to the dimension on the vector used to represent this word
        for word in uniqueVocabularyList:
            vectorIndex[word]=offset
            offset+=1
        #print(vectorIndex)
        return vectorIndex  #(keyword:position)


    def makeVector(self, wordString, mode):
        
        #Initialise vector with 0's
        vector = [0] * len(self.vectorKeywordIndex)
        #分成中英資料處理
        if self.is_chinese(wordString) == False: 
            wordList = self.parser.tokenise(wordString)
            wordList = self.parser.removeStopWords(wordList)
            tbString = tb(" ".join(wordList))
        else:                                    
            wordList = jieba.lcut_for_search(wordString) 
            wordList = self.parser.chi_removeStopWords(wordList)
            tbString = tb(" ".join(wordList))
        if mode == 'tf':
            for word in list(set(wordList)):
                if word in self.vectorKeywordIndex:
                    vector[self.vectorKeywordIndex[word]] = tf(word, tbString)
            return vector 

        if mode == 'tf-idf':
            for word in list(set(wordList)):
                if word in self.vectorKeywordIndex:
                    vector[self.vectorKeywordIndex[word]] =  tfidf(word, tbString , self.BlobList) 
            return vector
               
    def buildQueryVector(self, termList):
        """ convert query string into a term vector """
        query = self.makeVector(" ".join(termList), self.mode)
        return query

    
    def search(self,searchList):
        """ search for documents that match based on a list of terms """
        if type(searchList[0]) == str:
            queryVector = self.buildQueryVector(searchList)
        else:
            queryVector = searchList
        ratings = [util.cosine(queryVector, documentVector) for documentVector in self.documentVectors]
        #ratings.sort(reverse=True)
        return ratings
        
    def getQ3answer(self,searchlist, files,n):
        answer3 = self.search(searchlist)
        if self.mode == 'tf':
            print('Question3-1\nTerm Frequency (TF) Weighting + Cosine Similarity\n')
        elif self.mode == 'tf-idf':
            print('Question3-2\nTF-IDF Weighting + Cosine Similarity\n')
        print( 'NewsID' ,'         ','score')
        print('-----------------------------')
        for i in np.flip(np.argsort(answer3))[:n]:
            print(files[i],'     ' ,round(answer3[i], 6))
        return np.flip(np.argsort(answer3))[:n]
            

if __name__ == '__main__':
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

    query = ["烏克蘭 大選"]

    vectorSpace_tf = chi_VectorSpace(documents_chi, 'tf')
    vectorSpace_tf.getQ3answer(query, files_chi,10)

    vectorSpace_tfidf = chi_VectorSpace(documents_chi, 'tf-idf')
    vectorSpace_tfidf.getQ3answer(query, files_chi,10) 