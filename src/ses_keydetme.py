import sounddevice
from scipy.io.wavfile import write

def ses():
    fs= 15000
    second = 60
    record_voice = sounddevice.rec( int ( second * fs ) , samplerate = fs , channels = 2)
    sounddevice.wait()
    write("output/out.wav",fs,record_voice)
    