from pathlib import Path
import os
import argparse
import json

class SemanticModel:
    def __init__(self, liveModelDir, trainDataDir, saveModelDir):
        self.liveModelDir       = liveModelDir
        self.trainDataDir       = trainDataDir
        self.saveModelDir       = saveModelDir
        print(liveModelDir, '\n', trainDataDir, '\n', saveModelDir)
    
    def selectModel(self, modelName):
        self.modelName = modelName

        # Select which model to train depending on modelName
        # Model's folder with implementation should be present in 
        # ./Models directory

        if self.modelName == 'svm':
            from Models.svm.SVM import svmSemantics
            self.MODEL = svmSemantics(self.liveModelDir, self.trainDataDir, self.saveModelDir)
        elif self.modelName == 'lr':
            from Models.LogisticRegression.LogisticRegression import logRegSemantics
            self.MODEL = logRegSemantics(self.liveModelDir, self.trainDataDir, self.saveModelDir)
        else:
            raise ValueError('Unknown Model Name : '+modelName)

    def cleanData(self, trainFileName ):

        return self.MODEL.cleanData(trainFileName)
    
    def train(self, trainConfig ):

        return self.MODEL.trainModel(trainConfig)

    def testModel(self):

        return self.MODEL.testModel()

    def saveModel(self, modelName, labelToTextDict):

        return self.MODEL.saveModel(modelName, labelToTextDict)

    def makeModelLive(self):

        return self.MODEL.makeModelLive()




if __name__=="__main__":

    # Note :- 
        # ----------------------------------------------------------------------------------------------------
        # From command line provide directory path relative to current working directory : DataWeaveAssignment
        # DataWeaveAssignment is considered root directory for this project
        # Model specific configuration is read from DataWeaveConfig.JOSN file kept in current working directory


    # Path() Creates valid paths for the current platform
    # Setup command line options with default values if not provided
    # Using Path object we can extend paths just by using forward slash ( / )

    curWorkDir   = Path(os.getcwd())

    parser = argparse.ArgumentParser()
    parser.add_argument('--liveModelDir', type=str, 
                        default = "Models/svm/LiveModel", 
                        required=False, help = 'Path Of Live Model Directory Relative To DataWeaveAssignment')

    parser.add_argument('--trainDataDir', type=str, 
                        default = "TrainData", 
                        required=False, help = 'Path Of Train Data Directory Relative To DataWeaveAssignment')

    parser.add_argument('--saveModelDir', type=str, 
                        default = "Models/svm/SavedModels", 
                        required=False, help = 'Path Of Saved Model Directory Relative To DataWeaveAssignment')

    parser.add_argument('--trainFileName', type=str, 
                        default = "TrainData.txt", 
                        required=False, help = 'Name of text file containing labled paragraphs')

    parser.add_argument('--modelName', type=str, 
                        default = "svm", 
                        required=False, help = 'Name Of Model To Use :\n\t [1] svm : SVM, [2] lr : Logistic Regression')

    args = parser.parse_args()

    # liveModelDir is the directory from where server loads learned model for inference
    liveModelDir   = curWorkDir / args.liveModelDir
    trainDataDir   = curWorkDir / args.trainDataDir
    saveModelDir   = curWorkDir / args.saveModelDir
    modelName      = args.modelName
    trainFileName  = args.trainFileName
    
    semanticsModel = SemanticModel( str(liveModelDir), str(trainDataDir), str(saveModelDir))
    
    continueTraining = 1

    while continueTraining:
        try:
            # Read Config file based on modelName argument
            with open(os.path.join(os.getcwd(),'Models','Config.json')) as config_file:
                ConfigFile = json.load(config_file)
            modelConfig = ConfigFile[modelName]

            semanticsModel.selectModel(modelName)
            semanticsModel.cleanData(trainFileName)

            # Trains using cross validation and hyper parameters read from condfig file
            # Uses skLearn Grid Search for turing hyper parameters
            # returns the best model from a set of models for hyper-parameter
            # and also the best hyper parameters
            semanticsModel.train(modelConfig["train"])

            # Returns ture label, prediction, accuracy and F1-Score
            _, _, accuracy, F1  = semanticsModel.testModel()

            print('F1 Score : ', F1)
            print('Accuracy : ', accuracy)

            currentModelName = modelConfig["modelName"]
            labelToTextDict  = modelConfig["labelToTextDict"]
            semanticsModel.saveModel(currentModelName, labelToTextDict)

            choice = int(input("Do you want to make this model live : "))

            if choice == 1:
                semanticsModel.makeModelLive()

            continueTraining = int(input("Do you want to continue training : "))

        except ValueError as e:
            print (e)

        except KeyError as e:
            print('Model Configuration Not Present')
            exit(0)
        except IOError as e:
            print(e)
            exit(0)
        except Exception as e:
            print (e)