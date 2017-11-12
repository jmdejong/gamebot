

import time
import sys
import queue
import threading


class IrcSender:
    
    
    def __init__(self, connection=None):
        
        self.msgBuffer = queue.Queue()
        self.busy = False
        
        self.maxlen = 450
        self.delay = 0.5
        
        self.connection = connection
    
    
    def setConnection(self, connection):
        self.connection = connection
        self._startProcessing()
    
    def send(self, chan, text):
        
        while len(text):
            self.msgBuffer.put((chan, text[:self.maxlen]))
            text = text[self.maxlen:]
        
        self._startProcessing()
    
    def _startProcessing(self):
        if not self.busy and self.connection and not self.msgBuffer.empty():
            self.busy = True
            threading.Thread(target=self._processBuffer()).start()
    
    def _processBuffer(self):
        while not self.msgBuffer.empty():
            chan, text = self.msgBuffer.get_nowait()
            self._send(chan, text)
            time.sleep(self.delay)
        self.busy = False
    
    
    def _send(self, chan, text):
        try:
            self.connection.privmsg(chan, text)
        except Exception as err:
            print("sending message {} to channel {} failed: {}".format(text, chan, err))
        finally:
            sys.stdout.flush()
    

