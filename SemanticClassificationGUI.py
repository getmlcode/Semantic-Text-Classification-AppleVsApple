from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import requests

mainWindow = Tk()
class dataWeave_GUI:
    def __init__(self,master):
        appTitle = 'Semantics Assignment : Siddharth Shakya'
        master.title(appTitle)
        master.minsize(100, 50)

        #Setting Up Input-Text-Box

        self.inputTextFrame = Frame(master,highlightbackground="red", 
                                    width=100, height=50, 
                                    highlightthickness=1).\
                                    grid(row=0, column=0, padx=2, pady=2)

        self.inputTextBox = tk.Text(self.inputTextFrame, relief=SUNKEN)
        self.inputTextBox.grid(row=0, column=0)

        self.clearInput = ttk.Button(self.inputTextFrame, 
                                     text='Clear Input Text', 
                                     command=self.clearInputTextBox).\
                                     grid(row=1, column=0, sticky=W, padx=2, pady=2)


        #Setting Up Output Text Box

        self.userCommandsFrame = Frame(master, highlightbackground="blue", 
                                       width=100, height=50, 
                                       highlightthickness=1).\
                                       grid(row=0, column=1, sticky=E, padx=2, pady=2)

        self.outputTextBox = tk.Text(self.userCommandsFrame, relief=SUNKEN, state=DISABLED)
        self.outputTextBox.grid(row=0, column=1)

        self.clearOutput = ttk.Button(self.userCommandsFrame, 
                                      text='Clear Output Text', 
                                      command=self.clearOutputTextBox).\
                                      grid(row=1, column=1, sticky=W, padx=2, pady=2)

        self.inferTextSemantics = ttk.Button(self.userCommandsFrame, 
                                             text='Infer Semantics', 
                                             command=self.inferSemantics)
        self.inferTextSemantics.grid(row=2, column=1, sticky=W, padx=2, pady=2)

        self.serverIpEntry = tk.Entry(self.userCommandsFrame, relief=SUNKEN)
        self.serverIpEntry.grid(row=1, column=1)

        self.serverIpLabel = tk.Label(self.userCommandsFrame, text="IP and Port Address\n 127.0.0.1 : 5000")
        self.serverIpLabel.grid(row=2, column=1)

        #Quit Button
        self.quitButton = ttk.Button(self.userCommandsFrame, 
                                     text='Close', 
                                     command=master.destroy).\
                                     grid(row=3, column=1, sticky=W, padx=2, pady=2)

    # Functions
    def inferSemantics(self):
        
        inputText = self.inputTextBox.get("1.0", END)
        # Enable editing of Output Text Box
        self.outputTextBox.config(state="normal")

        # length of input text from texbox is 1 even if we don't write something in it !!
        if len(inputText) > 1:
            # Disable changes in Input Text Box while inferencing
            self.inputTextBox.config(state="disabled")
            if len(self.serverIpEntry.get()) ==0:
                self.outputTextBox.insert(tk.INSERT,'Please Provide Server IP Address\n')
                self.outputTextBox.config(state="disabled")
                return
            else:
                self.semanticApiEndPoint = 'http://'+self.serverIpEntry.get()+'/semantics'

            try:
                textSemantics = self.getTextSemantics(inputText)
                self.outputTextBox.insert(tk.INSERT, "Server Response \n")

                ServerResult = "\n".join(semantic for semantic in textSemantics)

                self.outputTextBox.insert(tk.INSERT, 'Semantics : \n'+ str(ServerResult)+"\n\n")
            except requests.exceptions.RequestException as exception:
                self.outputTextBox.insert(tk.INSERT, 'Server Exception : \n\n'+ str(exception)+"\n\n")
            except Exception as exception:
                self.outputTextBox.insert(tk.INSERT, 'Exception : \n\n'+ str(exception)+"\n\n")

            # Restore state of Input Text Box to normal after inference
            self.inputTextBox.config(state="normal")
            self.outputTextBox.config(state="disabled")
        else:
            self.outputTextBox.insert(tk.INSERT, "Input Text Must Be Non Empty\n")
            self.outputTextBox.config(state="disabled")
        return
    
    def clearInputTextBox(self):

        self.inputTextBox.delete(1.0, END)
        return

    def clearOutputTextBox(self):
        self.outputTextBox.config(state="normal")
        self.outputTextBox.delete(1.0, END)
        self.outputTextBox.config(state="disabled")
        return

    def getTextSemantics(self, inputText):

        clientReq = {'sampleText':inputText}

        try:
            serverResponse = requests.post(self.semanticApiEndPoint, json = clientReq)
            serverResponseJosn = serverResponse.json()

            if serverResponseJosn['status'] == 'OK':
                semantics = serverResponseJosn['textSemantics']
            elif serverResponse['status'] == 400:
                semantics = serverResponseJosn['message']
            else:
                semantic = serverResponse
            
            return semantics

        except requests.exceptions.RequestException as reqException:
            raise reqException

      
dataWeave = dataWeave_GUI(mainWindow)
mainWindow.mainloop()