from pydub import AudioSegment
import os
import silenceremove as sr


for filename in os.listdir(r'maleSpace'):
    #print(filename)
    sound = AudioSegment.from_file(f'maleSpace/{filename}')
    #print("----------Before Conversion--------")
    #print("Frame Rate", sound.frame_rate)
    #print("Channel", sound.channels)
    #print("Sample Width",sound.sample_width)
    # Change Frame Rate
    sound = sound.set_frame_rate(48000)
      # Change Channel
    sound = sound.set_channels(1)
      # Change Sample Width
    sound = sound.set_sample_width(2)
      # Export the Audio to get the changed contentsound.export("convertedrate.wav", format ="wav")
    sound.export(f"converted/{filename}converted.wav", format ="wav")

for filename in os.listdir(r'converted'):
  silencedFilePath = sr.silenceRemoveFunc(2, f"converted/{filename}")
    #os.system("py silenceremove.py 3 " + f'converted/{filename}')
