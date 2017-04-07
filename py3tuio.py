#!/usr/bin/env python3

from liblo import *
import time
import os

"""
py3tuio is a very basic implementation of a TUIO 1.x client written in Python 3 using pyliblo.
It is restricted to 2D surfaces and does not distinguish between different servers.
"""

class TuioClient(ServerThread):
    """
    the TuioClient processes TUIO/OSC messages and gives access 
    to corresponding lists of TuioObjects
    """
    def __init__(self, port):
        ServerThread.__init__(self, port)
        self.tuio2DCursors = []
        self.tuio2DObjects = []
        self.tuio2DBlobs = []
        self._aliveObjectIds = set([])
        self._tuioObjectsNew = []
        self._tuioObjectsOld = []
        self.fseq = 0
       
    @make_method(None, None)
    def handleObjectMessage(self, path, args, types, src):
       """process the incoming TUIO/OSC messages"""
       messageType = args.pop(0)
       if messageType == "alive":
           self._aliveObjectIds = []
           for sessionId in args:
               self._aliveObjectIds.append(sessionId)
       elif messageType == "set":
           tuioObject = None
           if (path == "/tuio/2Dcur"):
               tuioObject = Tuio2DCursor(args)
               self._tuioObjectsOld = self.tuio2DCursors
           elif (path == "/tuio/2Dobj"):
               tuioObject = Tuio2DObject(args)
               self._tuioObjectsOld = self.tuio2DObjects
           elif (path == "/tuio/2Dblb"):
               tuioObject = Tuio2DBlob(args)
               self._tuioObjectsOld = self.tuio2DBlobs
           if (tuioObject):
               self._tuioObjectsNew.append(tuioObject)
               self._aliveObjectIds.remove(tuioObject.sessionId)
       elif messageType == "fseq":
           if ((args[0] == -1) | (self.fseq < args[0])):
               self.fseq = args[0]
               # add all objects which didn't change but are still alive
               for o in self._tuioObjectsOld:
                   if (o.sessionId in self._aliveObjectIds):
                       self._tuioObjectsNew.append(o)
               if (path == "/tuio/2Dcur"):
                   self.tuio2DCursors = self._tuioObjectsNew
               elif (path == "/tuio/2Dobj"):
                   self.tuio2DObjects = self._tuioObjectsNew
               elif (path == "/tuio/2Dblb"):
                   self.tuio2DBlob = self._tuioObjectsNew
           self._tuioObjectsNew = []

class TuioObject():
    """this represents a TUIO object"""
    def __init__(self, args, argsLength):
        if (len(args) != argsLength):
            raise ValueError("TUIO Message: wrong number of arguments")

class Tuio2DCursor(TuioObject):
    """this represents a TUIO 2D cursor"""
    def __init__(self, args):
        super().__init__(args, 6)
        self.sessionId, self.x, self.y, self.xVelocity, self.yVelocity, self.acceleration = args[0:6]
            
class Tuio2DObject(TuioObject):
    """this represents a TUIO 2D object"""
    def __init__(self, args):
        super().__init__(args, 10)
        self.sessionId, self.markerId, self.x, self.y, self.angle, self.xVelocity, self.yVelocity, self.rotationSpeed, self.acceleration, self.rotationAcceleration = args[0:10]
        
class Tuio2DBlob(TuioObject):
    """this represents a TUIO 2D blob"""
    def __init__(self, args):
        super().__init__(args, 12)
        self.sessionId, self.x, self.y, self.angle, self.width, self.height, self.area, self.xVelocity, self.yVelocity, self.rotationSpeed, self.acceleration, self.rotationAcceleration = args[0:12]
    
def demo():
    try:
        client = TuioClient(3333)
    except ServerError as err:
        sys.exit(str(err))
    client.start()
    while (True):
        time.sleep(0.1)
        try:
            os.system('cls' if os.name=='nt' else 'clear') # clear the screen
            for o in client.tuio2DCursors:
                print ("2D cursor   id:{:2}   x: {:.6f}   y: {:.6f}".format(o.sessionId, o.x, o.y))
            for o in client.tuio2DObjects:
                print ("2D object   id:{:2}   x: {:.6f}   y: {:.6f}".format(o.sessionId, o.x, o.y))
            for o in client.tuio2DBlobs:
                print ("2D blob     id:{:2}   x: {:.6f}   y: {:.6f}".format(o.sessionId, o.x, o.y))
        except:
            client.stop()
            raise

if __name__ == '__main__':
    demo()