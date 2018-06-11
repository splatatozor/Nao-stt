# -*- encoding: UTF-8 -*-

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

NAO_IP = "192.168.1.238"


# Global variable to store the HumanVoice module instance
HumanVoice = None
memory = None
vocabulary = ["hello", "hi", "goodbye", "red"]

class HumanVoiceModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
        self.speechReco = ALProxy("ALSpeechRecognition")
        self.speechReco.setVocabulary(vocabulary, True)

        # Subscribe to the FaceDetected event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("WordRecognized",
            "HumanVoice",
            "onVoiceDetected")

    def onVoiceDetected(self, *_args):
        """ This will be called each time a face is
        detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("WordRecognized",
            "HumanVoice")

        # DO SOMETHING

        # Subscribe again to the event
        memory.subscribeToEvent("WordRecognized",
                                "HumanVoice",
                                "onVoiceDetected")
			
def main():
    """ Main entry point

    """
    parser = OptionParser()
    parser.add_option("--pip",
        help="Parent broker port. The IP address or your robot",
        dest="pip")
    parser.add_option("--pport",
        help="Parent broker port. The port NAOqi is listening to",
        dest="pport",
        type="int")
    parser.set_defaults(
        pip=NAO_IP,
        pport=9559)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port


    # Warning: HumanGreeter must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global HumanVoice
    HumanVoice = HumanVoiceModule("HumanVoice")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()