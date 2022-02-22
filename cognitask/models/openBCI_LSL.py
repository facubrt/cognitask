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
import threading

from PyQt5.QtCore import QObject
import cognitask.utils.openBCI_LSL.streamerlsl as streamerlsl

class OpenBCI_LSL(QObject):
  
  def __init__(self, puerto, comando):
    self.estado_datos = 'No datos'
    self.estado_placa = 'No iniciada'
    
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
    self.iniciar()
    
  def iniciar(self):  
    self.lsl.begin()
    estado_placa = self.estado_placa
    while estado_placa == 'Funcionando':
      # while
      estado_placa = self.estado_placa
  
  def comenzar(self):
    self.estado = 'Running'
    #self.lsl.start_streaming()
    # start streaming in a separate thread so we could always send commands in here
    boardThread = threading.Thread(target=self.lsl.board.start_streaming,args=(self.lsl.send,-1))
    boardThread.daemon = True # will stop on exit
    try:
      boardThread.start()
      print("Streaming data...")
    except:
      raise
    rec = True

  def observar_estado(self):
    estado = self.estado
    while estado == 'Running':
      boardThread = threading.Thread(target=self.lsl.board.start_streaming,args=(self.lsl.send,-1))
      boardThread.daemon = True # will stop on exit
      try:
        boardThread.start()
        print("Streaming data...")
      except:
        raise
      rec = True
      estado = self.estado
    #self.suspender()

  def suspender(self):
    self.estado = 'Suspender'
    self.lsl.stop_streaming()


  def enviarComando(self, comando):
    self.lsl.sendCommand(comando)

    
