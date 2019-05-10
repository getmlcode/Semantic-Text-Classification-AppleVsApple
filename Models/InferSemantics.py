from sklearn.feature_extraction.text import TfidfVectorizer,TfidfTransformer,CountVectorizer
from pathlib import Path
import os
import argparse
import json

class SemanticModel:
    def __init__(self, modelDir, model):
        self.modelDir       = modelDir
        self.model          = model
        
        if self.model == 'svm':
            from svm.InferSvmSemantics import svmSemantics
            self.INFERENCE_MODEL = svmSemantics(self.modelDir)
        elif self.model == 'lr':
            from LogisticRegression.InferLrSemantics import logRegSemantics
            self.INFERENCE_MODEL = logRegSemantics(self.modelDir)
        else:
            raise ValueError('Unknown Model : '+model)

    def cleanTextSamples(self,textSamples):
        return self.INFERENCE_MODEL.cleanTextSamples(textSamples)
    
    def getTextVectorizer(self, modelName):
        return self.INFERENCE_MODEL.getTextVectorizer(modelName)

    def loadSemanticsModel(self, modelFileName):
        return self.INFERENCE_MODEL.loadSemanticsModel(modelFileName)

    def getLabelToTextDictionary(self, dictFileName):
        return self.INFERENCE_MODEL.getLabelToTextDictionary(dictFileName)

    def getSemantics(self, textSamples):
        return self.INFERENCE_MODEL.getLabelToTextDictionary(textSamples)

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, 
                        default = "svm", 
                        required=False, help = 'Name Of Model To Use :\n\t 1. svm:\tSVM\n2. lr:\tLogistic Regression')

    args = parser.parse_args()
    model = args.model

    modelDir = os.path.join(os.getcwd(),'DataWeave',model,'LiveModel')

    try:
        infer = SemanticModel(modelDir, model)
    except ValueError as e:
        print(e)
        exit(0)

    try:
        with open(os.path.join(os.getcwd(),'DataWeave','DataWeaveConfig.json')) as config_file:
            ConfigFile = json.load(config_file)
        modelConfig = ConfigFile[model]
        modelName = modelConfig["modelName"]
    except KeyError as e:
        print('Model Configuration Not Present')
        exit(0)
    except IOError as e:
        print(e)
        exit(0)

    samples = ['APP#Le LaUN#ches I(phone','I e@at appLe Fr7UIT D@aily']

    cleanedSampleText = infer.cleanTextSamples(samples)

    transformer = TfidfTransformer()
    textVectorizer = infer.getTextVectorizer(modelName)

    semanticsModel = infer.loadSemanticsModel(modelName)
    labelToText = infer.getLabelToTextDictionary(modelName)

    vectorizedSample = transformer.fit_transform(textVectorizer.fit_transform(cleanedSampleText))
    textSemantics = semanticsModel.predict(vectorizedSample)

    k = list(labelToText.keys())

    textSemantics = [labelToText[k[0]] if semantic == int(k[0]) else labelToText[k[1]] for semantic in textSemantics]

    print(textSemantics)
    