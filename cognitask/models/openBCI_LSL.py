#!/usr/bin/python
'''
  openbci_lsl.py
  ---------------

  This is the main module for establishing an OpenBCI stream through the Lab Streaming Layer (LSL).

  Lab streaming layer is a networking system for real time streaming, recording, and analysis of time-series 
  data. LSL can be used to connect OpenBCI to applications that can record, analyze, and manipulate the data, 
  such as Matlab, NeuroPype, BCILAB, and others.

  To run the program as a GUI application, enter `python openbci_lsl.py`. 

  To run the program as a command line interface, enter `python openbci_lsl.py [port] --stream`. The port argument
  is optional, since the program automatically detects the OpenBCI port. However, if this functionality fails, the 
  port must be specified as an argument.

  For more information, see the readme on the Github repo:

  https://github.com/gabrielibagon/OpenBCI_LSL

'''

import sys

from PyQt5.QtCore import QObject
import cognitask.utils.openBCI_LSL.streamerlsl as streamerlsl

class OpenBCI_LSL(QObject):
  
  def __init__(self, puerto, comando):
    if puerto == 'None':
      self.lsl = streamerlsl.StreamerLSL(GUI=False)
    else:
      try:
        if comando != '--stream':
          print ("Command '%s' not recognized" % comando)
          return
      except IndexError:
        print("Command '%s' not recognized" % puerto)
        return
      self.port = puerto
      self.lsl = streamerlsl.StreamerLSL(port=self.port,GUI=False)
    self.lsl.create_lsl()
    
  def iniciar(self):  
    self.lsl.begin()

  def enviarComando(self, comando):
    self.lsl.sendCommand(comando)

    
