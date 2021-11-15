fixSpace <- function(folderName, outputFolder){
  SOUND_LENGTH <- 10
  list <- list.files(folderName, '\\.wav')
  i <- 1
  for (fileName in list) {
    setwd(folderName)
    soundName <- paste(i,".wav", sep = "")
    newSound <- tuneR::readWave(filename = fileName)
    setwd('..')
    setwd(outputFolder)
    tuneR::writeWave(newSound, filename=soundName, extensible=FALSE)
    setwd('..')
    i = i+1
  }
}

fixSpace('femaleWav', 'femaleSpace')
fixSpace('maleWav', 'maleSpace')
