from sklearn.feature_extraction.text import TfidfVectorizer,TfidfTransformer,CountVectorizer
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix,classification_report
from nltk.corpus import stopwords
import pickle
import os


class newModelNameSemantics:
    def __init__(self,liveModelDir):
        self.liveModelDir = liveModelDir
        self.stopList = list(stopwords.words('english'))
        self.spclCharList  = ['#','^','!','(',')','`','~','%','/','\\' ,'{','}',']','[','.',',',':',';','"','-','°','@','–']

    def cleanTextSamples(self,textSamples):

        return

    def getTextVectorizer(self, vocabFileName):
        return
        

    def loadSemanticsModel(self, modelFileName):

        return

    def getLabelToTextDictionary(self, dictFileName):

        return

    def getSemantics(self, textSamples):

        return

