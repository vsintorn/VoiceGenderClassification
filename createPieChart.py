import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from numpy import genfromtxt
import urllib.request
import json
import os
import ssl
import csv
import uuid
import csv
from tabulate import tabulate
#from sklearn.metrics import confusion_matrix

import pandas as pd

def CompareMLandSolution(arrayML, arraySolution):
    Tmale = 0
    Tfem = 0
    Ffem = 0
    Fmale = 0
    if(len(arrayML)!=len(arraySolution)):
        print ("Arrays are not the same length"+str(len(arrayML))+" "+str(len(arraySolution)))
        return
    arrayLength=len(arrayML)
    correctAnswer = 0
    for i in range(arrayLength):
       # print(arrayML[i] + ' ' + arraySolution[i]) 
        if ((arrayML[i]==arraySolution[i])):
            correctAnswer = correctAnswer + 1
            if (arrayML[i] == 'female'):
                Tfem = Tfem +1
            else:
                Tmale = Tmale+1
        else:
            if (arrayML[i] == 'female'):
                Ffem = Ffem +1
            else : 
                Fmale = Fmale +1  

    confusionMatrix = [[Tfem, Ffem], [Fmale, Tmale]]
    return(correctAnswer/arrayLength, confusionMatrix)


def CreatePieChart(arrayML):

    maleStats = arrayML.count('male')
    femaleStats = arrayML.count('female')

    data = [maleStats, femaleStats]
    gender = ['Male '+str(maleStats*100/len(arrayML))+'%', 'Female '+str(femaleStats*100/len(arrayML))+'%']

    fig = plt.figure(figsize =(10, 7))
    plt.pie(data, labels = gender)

    plt.show()


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here

def runML(fileName, modelURL):
    df = pd.read_csv(fileName, delimiter=',', dtype = str)
    dataval = df.to_json(orient='records')
    data = json.loads(dataval)

    #print (dataval)
    data = {"data" : data}


    body = str.encode(json.dumps(data))

    url = modelURL #newreal
    api_key = '' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
      
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))


    
    result = result.decode("utf-8").replace('"',"")
    result = result.split(',')
    resultarray = []
    for res in result:

        resultarray.append(res.split(':'))

    del resultarray[0][0]
    flatlist = list(matplotlib.cbook.flatten(resultarray))
    newlist=[]
    i=1
    for gender in flatlist:
        s = ''.join(ch for ch in gender if ch.isalnum())
        #print(str(i) + " " + s)
        i = i+1

        newlist.append(s)
    
    return(newlist)



def testModels(fileCsv, solutionCsv = None):
    #ta in csv av en inspelning
    #Kör den med alla modeller
    # Få en arrayML med prediktioner från alla modeller
    # Jämför dessa prediktioner med facit, få ut ANTAL kvinnliga/manliga prediktioner om det inte finns facit. 
    # displaya en tabell? eller en csv fil? men alla modeller, och deras acuracy samt confusion matrix 


    model20sekWsilenceURL = 'http://3a16fd3c-dfbc-4918-8f29-d0bb9c426ddf.northeurope.azurecontainer.io/score'
    model20sekNOsilenceURL = 'http://d41dcb84-62f8-43d1-a46a-02f40fb79324.northeurope.azurecontainer.io/score'
    model10sekNOsilenceURL = 'http://57ce19b0-2b8d-4687-a39a-8279cd57273f.northeurope.azurecontainer.io/score'
    model15sekNOsilenceURL = 'http://35645446-4db7-4cdf-97e7-576c2d7590f3.northeurope.azurecontainer.io/score'

    prediction20sekWsilence = runML(fileCsv, model20sekWsilenceURL)
    prediction20sekNOsilence = runML(fileCsv, model20sekNOsilenceURL)
    prediction10sekNOsilence = runML(fileCsv, model10sekNOsilenceURL)
    prediction15sekNOsilence = runML(fileCsv, model15sekNOsilenceURL)


    if solutionCsv != None: 
        solution = pd.read_csv(solutionCsv, delimiter=',', header = None)
        solution=list(matplotlib.cbook.flatten(solution.transpose().values))
        accuracy20W, confusion20W = CompareMLandSolution(prediction20sekWsilence, solution)
        accuracy20NO, confusion20NO = CompareMLandSolution(prediction20sekNOsilence, solution)
        accuracy10, confusion10NO = CompareMLandSolution(prediction10sekNOsilence, solution)
        accuracy15, confusion15NO = CompareMLandSolution(prediction15sekNOsilence, solution)
        resultRow= [ fileCsv, accuracy20W, accuracy20NO, accuracy10 ,accuracy15, confusion20W, confusion20NO, confusion10NO, confusion15NO]
         

    else :
        accuracy20W = prediction20sekWsilence.count('female')/len(prediction20sekWsilence)
        accuracy20NO= prediction20sekNOsilence.count('female')/len(prediction20sekNOsilence)
        accuracy10= prediction10sekNOsilence.count('female')/len(prediction10sekNOsilence)
        accuracy15=  prediction15sekNOsilence.count('female')/len(prediction15sekNOsilence)
        resultRow= [ fileCsv, accuracy20W, accuracy20NO, accuracy10 ,accuracy15]




    


    resultCsv = open('resultModelTest.csv', 'a')
    csvWriter = csv.writer(resultCsv)
    csvWriter.writerow(resultRow)
    resultCsv.close()
    







def mainPieChart(fileName):
  arrayML = runML(fileName, 'http://35645446-4db7-4cdf-97e7-576c2d7590f3.northeurope.azurecontainer.io/score')
  #arraySolution = pd.read_csv(f'poddelipoddfacit.csv', delimiter=',', header = None)
  #arraySolution=list(matplotlib.cbook.flatten(arraySolution.transpose().values))
  #print(arraySolution)
  #result = CompareMLandSolution(arrayML, arraySolution)
  #print(result)
  CreatePieChart(arraySolution)

#testModels('Testdata\Sigge Eklund Jag har känt mycket avund.wavconverted.wavNon-Silenced.csv', 'Testdata\Sigge Eklund Jag har känt mycket avund.wavconverted.wavNon-Silenced_facit.csv')
#mainPieChart('61 Det gäller ett saldo redigerad.wavconverted.wavNon-Silenced.csv')