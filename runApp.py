
import rpy2.robjects as robjects
import os
import subprocess
import taBortTystnad.soundprocess1 as sp
import createPieChart as cpc
#import taBortTystnad.silenceremove1 as sr

def runApplication (nameWav):
  # Defining the R script and loading the instance in Python
  r = robjects.r
  r['source']('meeting2csv.R')



  #nameWav = convertToWav_function_r('Verapratar10min.mp3')
  silenceRemovedPath = sp.soundProcessMain(f'{nameWav}')
  #print(silenceRemovedPath)
  # Loading the functions we have defined in R.
  meeting2csv_function_r = robjects.globalenv['meeting2csv']
  #Invoking the R function and getting the result
  namecsv = meeting2csv_function_r(silenceRemovedPath)
  namecsv=''.join(namecsv)
  #TEST namecsv = 'VeraPratar10min.csv'
  cpc.mainPieChart(namecsv)
  print(namecsv)
runApplication('Poddelipodd.wav')