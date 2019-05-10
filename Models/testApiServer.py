#quick test script for rest API

import requests
import json

company = 'If this seems a bit like déjà vu, you’ll recall that Apple just held an event to unveil two new'+\
          ' iPhone models – the 5c and 5s – back on September 10'
fruit = 'I eA@t Appl%l fruIt D@i!Ly déjà'

clientInput = fruit+'\n\n'+company
dictToSend = {'sampleText':clientInput}
res = requests.post('http://localhost:5000/semantics', json=dictToSend)

print( 'response from server: \n',res.text)

serverResponse = res.json() #This is dictionary

if serverResponse['status'] == 'OK':
    print('Input Text Semantics : ',serverResponse['textSemantics'])
elif serverResponse['status'] == 400:
    print('Error : ',serverResponse['message'])