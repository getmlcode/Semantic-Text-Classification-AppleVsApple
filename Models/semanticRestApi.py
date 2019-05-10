from flask import Flask, render_template, request, url_for, jsonify
from DataCollection import addSampleTextandResponseToDatabase
#from svm.InferSvmSemantics import svmSemantics
from sklearn.feature_extraction.text import TfidfVectorizer,TfidfTransformer,CountVectorizer
import threading
import os
import argparse
import json

from InferSemantics import SemanticModel


parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, 
                    default = "svm", 
                    required=False, help = 'Name Of Model To Use :\n\t 1. svm:\tSVM\n2. lr:\tLogistic Regression')

args = parser.parse_args()

model = args.model
try:
    with open(os.path.join(os.getcwd(),'Models','Config.json')) as config_file:
        ConfigFile = json.load(config_file)
    modelConfig = ConfigFile[model]
    modelName = modelConfig["liveModelName"]
except KeyError as e:
    print('Model Configuration Not Present')
    exit(0)
except IOError as e:
    print(e)
    exit(0)

liveModelDir = os.path.join(os.getcwd(),'Models',model,'LiveModel')
print(liveModelDir)

sem = SemanticModel(liveModelDir,model)
transformer = TfidfTransformer()
textVectorizer = sem.getTextVectorizer(modelName)

semanticsModel = sem.loadSemanticsModel(modelName)
labelToText = sem.getLabelToTextDictionary(modelName)

print('Model Being Used For Inference : ',modelName,'\n\n')



def prepareSampleTextsFromClientInput(clientInput):

    inputSampleTexts = sem.cleanTextSamples(clientInput.split('\n\n'))


    return inputSampleTexts


def inferSemantics(clientInput):

    cleanedSampleText = prepareSampleTextsFromClientInput(clientInput)

    if len(cleanedSampleText) > 0:
        
        vectorizedSample = transformer.fit_transform(textVectorizer.fit_transform(cleanedSampleText))
        textSemantics = semanticsModel.predict(vectorizedSample)

        keys = list(labelToText.keys())

        textSemantics = [labelToText[keys[0]] if semantic == int(keys[0]) 
                         else labelToText[keys[1]] for semantic in textSemantics]

        serverResponse = {'textSemantics':textSemantics, 'status':'OK'}

        # Perform database updation in a background thread to improve response time 
        # for user
        databaseThread = threading.Thread( target = addSampleTextandResponseToDatabase, 
                                          args = (cleanedSampleText, textSemantics) )
        databaseThread.start()

        return jsonify(serverResponse)
    else:
        serverResponse = {'message':'Empty Sample Text', 'status':400}
        return jsonify(serverResponse)


app = Flask(__name__)

@app.route('/semantics', methods=['POST'])
def getSemantics():
    print('Model Being Used For Inference: ',modelName)
    clinetReq = request.get_json(force=True)
    # force=True, above, is necessary if another developer 
    # forgot to set the MIME type to 'application/json'

    sampleText = clinetReq['sampleText']
    #print ('Clinet Sample Text :', sampleText)

    serverResponseJson = inferSemantics(sampleText.strip('\n\t'))
    
    return serverResponseJson

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host= '0.0.0.0',debug=True)