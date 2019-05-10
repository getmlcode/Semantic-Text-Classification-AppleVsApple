import pandas as pd
import os

class svmSemantics:
    def __init__(self, liveModelDir, trainDataDir, saveModelDir):
        self.liveModelDir     = liveModelDir
        self.trainDataDir     = trainDataDir
        self.saveModelDir     = saveModelDir

        print('SVM Model Directories :\n',liveModelDir, '\n', trainDataDir, '\n', saveModelDir)

    def cleanData(self, trainFileName):

        try:
            trainDataText = open( os.path.join(self.trainDataDir, trainFileName), 'r' )

            self.trainDataframe = pd.DataFrame( columns=['paragraph', 'label'] )
            #trainDataText.readline()
            for line in trainDataText.readlines():
                line = line.rstrip('\n').split('\t')
                l = 1 if line[1] == 'company' else 0
                self.trainDataframe = self.trainDataframe.append( {'paragraph':line[0],'label' :l}, ignore_index=True )
            trainDataText.close()
        except IOError as e:
            print( e )
            exit(0)

        return self.trainDataframe

    def trainModel(self, trainConfig):

        nGram           = trainConfig["ngram"]
        maxFeatures     = trainConfig["maxFeatures"]
        testSetFraction = trainConfig["testSetFraction"]
        tuneParam       = trainConfig["hyperParams"]
        K               = trainConfig["folds"]
        score           = trainConfig["score"]

        # Returns trained instance of model and dictionary of tuned parameters
        # Importing libs here as the user doesn't expect delay during object creation 
        # but delay during training is expected

        from sklearn.svm import SVC
        from sklearn.feature_extraction.text import TfidfVectorizer
        #from sklearn.feature_extraction.text import TfidfTransformer
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.model_selection import train_test_split
        from sklearn.model_selection import GridSearchCV

        trainData = self.trainDataframe['paragraph']
        label = self.trainDataframe['label'].values.astype('int')

        self.vectorizer = TfidfVectorizer("english", ngram_range = (1,nGram), max_features = maxFeatures)
        X = self.vectorizer.fit_transform(trainData)
        X_train, self.X_test, Y_train, self.Y_test = train_test_split(X, label, stratify=label, 
                                                                      test_size=testSetFraction)

        self.semanticClassifier = GridSearchCV(SVC(), tuneParam, cv=K, scoring = score)
        self.semanticClassifier.fit(X_train, Y_train)

        self.bestParams = self.semanticClassifier.best_params_ 
        self.semanticClassifier = self.semanticClassifier.best_estimator_
        
        return self.semanticClassifier, self.bestParams

    def testModel(self):
        from sklearn.metrics import accuracy_score, f1_score
        self.prediction = self.semanticClassifier.predict(self.X_test)

        self.accuracy = accuracy_score(self.Y_test, self.prediction)
        self.f1 = f1_score(self.Y_test, self.prediction)

        return self.Y_test, self.prediction, self.accuracy, self.f1

    def saveModel(self, modelName, labelToTextDict):
        import pickle
        import os
        self.labelToTextDict = labelToTextDict
        try:
            if not os.path.exists(self.saveModelDir):
                os.makedirs(self.saveModelDir)

            # Append model F1 score to its namde and then save
            self.modelName = modelName+'_'+str(self.f1).replace('.','_')
            vocabFile = os.path.join(self.saveModelDir, self.modelName+'_Vocab.pkl')
            modelFile = os.path.join(self.saveModelDir, self.modelName+'_Model.pkl')
            labelToTextDictFile = os.path.join(self.saveModelDir, self.modelName+'_LabelToText.pkl')

            pickle.dump(self.vectorizer.vocabulary_, open(vocabFile,"wb"))
            pickle.dump(self.semanticClassifier, open(modelFile,"wb"))
            pickle.dump(self.labelToTextDict, open(labelToTextDictFile,"wb"))
        
        except IOError as e:
            print( e )
            exit(0)

    def makeModelLive(self):
        import pickle

        try:
            if not os.path.exists(self.liveModelDir):
                os.makedirs(self.liveModelDir)

            modelName = self.modelName.split('_')[0]

            with open(os.path.join(self.liveModelDir,modelName+'_F1Score.txt'),'w') as file:
                file.write(str(self.f1))

            vocabFile = os.path.join(self.liveModelDir, modelName+'_Vocab.pkl')
            modelFile = os.path.join(self.liveModelDir, modelName+'_Model.pkl')
            labelToTextDictFile = os.path.join(self.liveModelDir, modelName+'_LabelToText.pkl')

            pickle.dump(self.vectorizer.vocabulary_, open(vocabFile,"wb"))
            pickle.dump(self.semanticClassifier, open(modelFile,"wb"))
            pickle.dump(self.labelToTextDict, open(labelToTextDictFile,"wb"))
        
        except IOError as e:
            print( e )
            exit(0)

if __name__=="__main__":
    liveModelDir = os.getcwd()
    trainDataDir = os.getcwd()+'\\TrainData'
    saveModelDir = os.getcwd()
    svmTextSemantics = TrainSvmSemantics(liveModelDir, trainDataDir, os.getcwd())
    labelToTextDict = {1:'company',0:'fruit'}

    data = svmTextSemantics.cleanData('TrainData.txt')
    print(data)

    hyperParams = [{'kernel': ['rbf'],'gamma': [1e-3, 1e-4],'C': [1, 10, 100, 1000]},\
                   {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
 
    # Read parameters from config file
    

    svmTextSemantics.trainModel(nGram, 800, .4, hyperParams, 5, 'f1')
    #trueLabel, prediction, accuracy, F1  = svmTextSemantics.testModel()
    _, _, accuracy, F1  = svmTextSemantics.testModel()

    print('F1 Score : ',F1)
    print('Accuracy : ',accuracy)

    svmTextSemantics.saveModel('svmSem',labelToTextDict)