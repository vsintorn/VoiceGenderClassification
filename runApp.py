
import rpy2.robjects as robjects

import removeSilence.soundprocess1 as sp
import createPieChart as cpc
#import taBortTystnad.silenceremove1 as sr

def runApplication (nameWav):
  # Defining the R script and loading the instance in Python
  r = robjects.r
  r['source']('meeting2csv.R')

  #Remove silence from audio 
  silenceRemovedPath = sp.soundProcessMain(f'{nameWav}')

  # Loading the functions we have defined in R.
  meeting2csv_function_r = robjects.globalenv['meeting2csv']
  #Invoking the R function and getting the result
  # extract features from sound to a CSV file
  namecsv = meeting2csv_function_r(silenceRemovedPath)
  namecsv=''.join(namecsv)
  
  #predict gender and print out a pie chart of the result
  cpc.mainPieChart(namecsv)
 
runApplication('Poddelipodd.wav')