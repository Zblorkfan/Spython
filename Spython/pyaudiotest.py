# import required libraries
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
def sound() : 

     
    # Sampling frequency
    freq = 44400
     
    # Recording duration in seconds
    duration = 15
     
    # to record audio from
    # sound-device into a Numpy

    recording = sd.rec(int(duration * freq), samplerate = freq, channels = 2)
     
    # Wait for the audio to complete
    sd.wait()
     
    write("recording0.wav", freq, recording)
     
