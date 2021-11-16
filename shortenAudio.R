shortenAudio <- function(folderName, outputFolder){
  SOUND_LENGTH <- 15
  list <- list.files(folderName, '\\.wav')
  for (fileName in list) {
    setwd(folderName)
    newSound <- tuneR::readWave(filename = fileName, from = 0, to = SOUND_LENGTH, unit = "seconds")
    setwd('..')
    setwd(outputFolder)
    tuneR::writeWave(newSound, filename=fileName, extensible=FALSE)
    setwd('..')
  }
}