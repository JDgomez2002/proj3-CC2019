# Teoria de computacion CC2019
# Gonzalo Santizo 
# Jose Daniel Gomez

import copy
import yaml

class Colors:
  CLEAR = '\033[0m'
  RED = '\033[91m'
  GREEN = '\033[92m'
  BLUE = '\033[94m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

class Tape(object):
  blankSymbol = " "
  def __init__(self, stringTape = "", blank=" "):
    self.__tape = dict((enumerate(stringTape)))
    Tape.blankSymbol = blank

  def __str__(self):
    s = ""
    minimumUsedIndex = min(self.__tape.keys()) 
    maximumUsedIndex = max(self.__tape.keys())
    for i in range(minimumUsedIndex, maximumUsedIndex+1):
      s += self.__tape[i]
    return s

  def __getitem__(self,index):
    if index in self.__tape:
      return self.__tape[index]
    else:
      return Tape.blankSymbol

  def __setitem__(self, pos, char):
    self.__tape[pos] = char

class TuringMachine(object):

  def __init__(
    self,
    tapes = list[str],
    blankSymbol = " ",
    initialState = "",
    finalStates = None,
    transitionFunction = None,
    acceptedStates = None
  ):
    self.__init = initialState
    self.tapes = tapes
    self.__curr = 0
    self.__blankSymbol = blankSymbol
    self.__tape = Tape(tapes[self.__curr],self.__blankSymbol)
    self.__headPosition = 0
    self.__currentState = initialState
    self.__immediate_description = None
    self.__acceptedStates = acceptedStates
    if transitionFunction == None:
      self.__transitionFunction = {}
    else:
      self.__transitionFunction = transitionFunction
    if finalStates == None:
      self.__finalStates = set()
    else:
      self.__finalStates = set(finalStates)
  
  def nextStringAvailable(self):
    self.__curr += 1
    if self.__curr < len(self.tapes):
      self.__tape = Tape(self.tapes[self.__curr],self.__blankSymbol)
      self.__headPosition = 0
      self.__currentState = self.__init
      self.__immediate_description = None
      return True
    else:
      return False

  def getTape(self): 
    return str(self.__tape)