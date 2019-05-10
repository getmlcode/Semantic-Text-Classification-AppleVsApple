import os

class nemModelNameSemantics:
    def __init__(self, liveModelDir, trainDataDir, saveModelDir):
        self.liveModelDir       = liveModelDir
        self.trainDataDir       = trainDataDir
        self.saveModelDir       = saveModelDir

        print('ModelName Directories :\n',liveModelDir, '\n', trainDataDir, '\n', saveModelDir)
    
    def cleanData(self, trainFileName):

        print('yet to code data cleaing for this model')
        pass
    
    def trainModel(self, trainConfig):

        print('yet to code training for this model')

        return -1

    def testModel(self):
        print('yet to code testing for this model')

        return 0,0,0,0

    def saveModel(self):
        print('yet to code saving for this model')
        return -1

    def makeModelLive(self):
        print('yet to code for this model')

        return -1

if __name__=="__main__":
    print()