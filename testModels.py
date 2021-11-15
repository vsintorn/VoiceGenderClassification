
import pandas as pd
import csv
import createPieChart as cpc
import matplotlib

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
    
    #compare the prediction with the corect answer
    for i in range(arrayLength):
        
        if ((arrayML[i]==arraySolution[i])):
            correctAnswer = correctAnswer + 1
            if (arrayML[i] == 'female'):
                Tfem = Tfem +1
            else:
                Tmale = Tmale +1
        else:
            if (arrayML[i] == 'female'):
                Ffem = Ffem +1
            else : 
                Fmale = Fmale +1  

    confusionMatrix = [[Tfem, Ffem], [Fmale, Tmale]]
    return(correctAnswer/arrayLength, confusionMatrix)

def testModels(fileCsv, solutionCsv = None):
    
    # Define the APi handle for the diferend models
    model20sekWsilenceURL = 'http://3a16fd3c-dfbc-4918-8f29-d0bb9c426ddf.northeurope.azurecontainer.io/score'
    model20sekNOsilenceURL = 'http://d41dcb84-62f8-43d1-a46a-02f40fb79324.northeurope.azurecontainer.io/score'
    model15sekNOsilenceURL = 'http://35645446-4db7-4cdf-97e7-576c2d7590f3.northeurope.azurecontainer.io/score'
    model10sekNOsilenceURL = 'http://57ce19b0-2b8d-4687-a39a-8279cd57273f.northeurope.azurecontainer.io/score'


    #Make predictions with the diferent models
    prediction20sekWsilence = cpc.runML(fileCsv, model20sekWsilenceURL)
    prediction20sekNOsilence = cpc.runML(fileCsv, model20sekNOsilenceURL)
    prediction10sekNOsilence = cpc.runML(fileCsv, model10sekNOsilenceURL)
    prediction15sekNOsilence = cpc.runML(fileCsv, model15sekNOsilenceURL)

    #Compare the predicted result with the solution and store the values
    if solutionCsv != None: 
        solution = pd.read_csv(solutionCsv, delimiter=',', header = None)
        solution=list(matplotlib.cbook.flatten(solution.transpose().values))
        accuracy20W, confusion20W = CompareMLandSolution(prediction20sekWsilence, solution)
        accuracy20NO, confusion20NO = CompareMLandSolution(prediction20sekNOsilence, solution)
        accuracy10, confusion10NO = CompareMLandSolution(prediction10sekNOsilence, solution)
        accuracy15, confusion15NO = CompareMLandSolution(prediction15sekNOsilence, solution)
        resultRow= [ fileCsv, accuracy20W, accuracy20NO, accuracy10 ,accuracy15, confusion20W, confusion20NO, confusion10NO, confusion15NO]
         
    #if no solution exists for this file, cound number of female predicted. 
    else :
        accuracy20W = prediction20sekWsilence.count('female')/len(prediction20sekWsilence)
        accuracy20NO= prediction20sekNOsilence.count('female')/len(prediction20sekNOsilence)
        accuracy10= prediction10sekNOsilence.count('female')/len(prediction10sekNOsilence)
        accuracy15=  prediction15sekNOsilence.count('female')/len(prediction15sekNOsilence)
        resultRow= [ fileCsv, accuracy20W, accuracy20NO, accuracy10 ,accuracy15]

    #Save the results to a csv for further analysis 
    resultCsv = open('resultModelTest.csv', 'a')
    csvWriter = csv.writer(resultCsv)
    csvWriter.writerow(resultRow)
    resultCsv.close()
    

# For a fast comparision
# compare just one model and print result, (nothing will be stored in a csv)
def fastCompare(fileName, solutionName):
  arrayML = cpc.runML(fileName, 'http://35645446-4db7-4cdf-97e7-576c2d7590f3.northeurope.azurecontainer.io/score')
  arraySolution = pd.read_csv(solutionName, delimiter=',', header = None)
  arraySolution=list(matplotlib.cbook.flatten(arraySolution.transpose().values))
  result = CompareMLandSolution(arrayML, arraySolution)
  print(result)


