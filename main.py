from naoqi import ALProxy
from naoqi import ALModule
import time


class SpeechModule(ALModule):
    def __init__(self, param):
        ALModule.__init__(self, param)
        self.volume = 0
        self.v = ALProxy("ALAudioDevice")
        self.tts = ALProxy("ALTextToSpeech")
        #self.tts.setLanguage('French')
        #self.tts.setParameter("pitchShift", 1.0)
        #self.tts.setParameter("speed", 3.0)
        #self.tts.setParameter("doubleVoiceLevel", 3.0)
        #self.tts.setParameter("doubleVoiceTimeShift", 0.5)


        self.v.setOutputVolume(100)
        print self.v.getOutputVolume()

    def speech(self, text):
        print "will say ", text
        self.tts.setParameter("pitchShift", 1.0)
        self.tts.say(text)
        time.sleep(1)
