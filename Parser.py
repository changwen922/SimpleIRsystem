#http://tartarus.org/~martin/PorterStemmer/python.txt

from PorterStemmer import PorterStemmer


class Parser:

	#A processor for removing the commoner morphological and inflexional endings from words in English
	stemmer=None

	stopwords=[]
	ChineseStop=[]
	def __init__(self,):
		self.stemmer = PorterStemmer()

		#English stopwords from ftp://ftp.cs.cornell.edu/pub/smart/english.stop
		self.stopwords = open('EnglishStopwords.txt').read().split()
		with open('Stopwords.txt', encoding="utf-8") as f:
			stop =f.readlines()
			stop1 = ' '.join(stop)
			self.ChineseStop = stop1.replace("\n", "").split()


	def clean(self, string):
		""" remove any nasty grammar tokens from string """
		string = string.replace(".","")
		string = string.replace("\s+"," ")
		string = string.replace("?","")
		string = string.replace(",","")
		string = string.lower()
		return string
		'''
		data = np.char.replace(data,".","")
		data = np.char.replace(data,"\s+"," ")
		data = np.char.replace(data,",", "")
		data = np.char.replace(data,"(", "")
		data = np.char.replace(data,")", "")
		data = np.char.replace(data,":", "")
		data = np.char.replace(data,"#", "")
		data = np.char.replace(data,"'", "")
		data = np.char.replace(data,"``", "")
		data = np.char.replace(data,"$", "")
		data = np.char.lower(data)
		return data
		'''

	def removeStopWords(self,list):
		""" Remove common words which have no search value """
		return [word for word in list if word not in self.stopwords ]


	def tokenise(self, string):
		""" break string up into tokens and stem words """
		string = self.clean(string)
		words = string.split(" ")
		
		return [self.stemmer.stem(word,0,len(word)-1) for word in words]

	def chi_removeStopWords(self,list):
		""" Remove common words which have no search value """
		return [word for word in list if word not in self.ChineseStop ]

