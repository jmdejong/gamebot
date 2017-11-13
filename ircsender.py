

import time
import sys
import queue
import threading
import textwrap


class IrcSender:
    
    """
    The tilde.town IRC server only accepts messages of at most 512 bytes,
    and will disconnect anyone who sends more than 2 messages per second for a longer time.
    This class ensures that all sent text messages satisfy these constraints
    """
    
    def __init__(self, connection=None):
        
        self.msgBuffer = queue.Queue()
        
        self.maxlen = 450
        self.delay = 0.5
        
        self.connection = connection
        
        self.startProcessing()
    
    
    def setConnection(self, connection):
        self.connection = connection
    
    def send(self, chan, text):
        """ put the message in the sending queue. This is the safe send """
        lines = textwrap.wrap(text, self.maxlen)
        for line in lines:
            self.msgBuffer.put((chan, line))
        
    
    def startProcessing(self):
        self.processing = True
        threading.Thread(target=self._processBuffer).start()
    
    def stopProcessing(self):
        self.processing = False
        self.msgBuffer.put(None)
    
    
    
    # The next functions are executed on the processing thread
    
    def _processBuffer(self):
        while self.processing:
            msg = self.msgBuffer.get()
            if msg:
                chan, text = msg
                self._send(chan, text)
                time.sleep(self.delay)
    
    
    def _send(self, chan, text):
        try:
            self.connection.privmsg(chan, text)
        except Exception as err:
            print("sending message {} to channel {} failed: {}".format(text, chan, err))
        finally:
            sys.stdout.flush()

