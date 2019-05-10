from sklearn.feature_extraction.text import TfidfVectorizer,TfidfTransformer,CountVectorizer
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix,classification_report
from nltk.corpus import stopwords
import pickle
import os


class svmSemantics:
    def __init__(self,liveModelDir):
        self.liveModelDir = liveModelDir
        self.stopList = list(stopwords.words('english'))
        self.spclCharList  = ['#','^','!','(',')','`','~','%','/','\\' ,'{','}',']','[','.',',',':',';','"','-','°','@','–']

    def cleanTextSamples(self,textSamples):

        cleanedSamples = []

        for text in textSamples:
            for ch in self.spclCharList:
                text = text.replace(ch,'')
            text = ''.join([i for i in text if not i.isdigit()])
            text = text.lower().strip().split()
            text = list(filter(lambda x: x != '', text))
            text = [word for word in text if word not in self.stopList]
            text = ' '.join(str(w) for w in text)
            cleanedSamples.append(text)
        return cleanedSamples

    def getTextVectorizer(self, vocabFileName):
        vocabFile = os.path.join(self.liveModelDir,vocabFileName+'_Vocab.pkl')

        try:
            vocab = CountVectorizer(decode_error="replace", vocabulary=pickle.load(open(vocabFile, "rb")))
        except IOError as e:
            print(e)
            exit(0)
        return vocab
        

    def loadSemanticsModel(self, modelFileName):
        modelFile = os.path.join(self.liveModelDir,modelFileName+'_Model.pkl')

        try: 
            model = pickle.load(open(modelFile, 'rb'))
        except IOError as e:
            print(e)
            exit(0)

        return model

    def getLabelToTextDictionary(self, dictFileName):
        dictFile = os.path.join(self.liveModelDir,dictFileName+'_LabelToText.pkl')

        try: 
            LabelToTextDictionary = pickle.load(open(dictFile, 'rb'))
        except IOError as e:
            print(e)
            exit(0)

        return LabelToTextDictionary

    def getSemantics(self, textSamples):
        transformer = TfidfTransformer()

        cleanedTextSamples = self.cleanTextSamples(textSamples)

        textVectorizer = self.getTextVectorizer('simpleSvm')
        vectorizedSamples = transformer.fit_transform(textVectorizer.fit_transform(cleanedTextSamples))

        svmSemanticsModel = self.loadSemanticsModel('simpleSvm')

        predictions = svmSemanticsModel.predict(vectorizedSamples)

        return predictions


if __name__=='__main__':
    sem = svmSemantics('.\\')
    samples = ['APP#Le LaUN#ches I(phone','I e@at appLe Fr7UIT D@aily']
    
    # In one call
    textSamplesSemantics = sem.getSemantics(samples) 
    labelToText = sem.getLabelToTextDictionary('simpleSvm')
    k=list(labelToText.keys())

    textSamplesSemantics = [labelToText[k[0]] if semantic == int(k[0]) 
                            else labelToText[k[1]] for semantic in textSamplesSemantics]


    print(samples)
    print(sem.cleanTextSamples(samples))
    print(textSamplesSemantics)

    # In step by step

    transformer = TfidfTransformer()
    cleanedTextSamples = sem.cleanTextSamples(samples)

    textVectorizer = sem.getTextVectorizer('simpleSvm')
    vectorizedSamples = transformer.fit_transform(textVectorizer.fit_transform(cleanedTextSamples))
    
    svmSemanticsModel = sem.loadSemanticsModel('simpleSvm')
    textSemantics = svmSemanticsModel.predict(vectorizedSamples)

    textSemantics = [labelToText[k[0]] if semantic == int(k[0]) else labelToText[k[1]] for semantic in textSemantics]


    print(textSemantics)
